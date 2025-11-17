"""YoLink DataUpdateCoordinator."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
import logging
from typing import Any

from yolink.client_request import ClientRequest
from yolink.device import YoLinkDevice
from yolink.exception import YoLinkAuthFailError, YoLinkClientError
from yolink.model import BRDP

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import ATTR_DEVICE_STATE, ATTR_LORA_INFO, DOMAIN, YOLINK_OFFLINE_TIME

_LOGGER = logging.getLogger(__name__)


class YoLinkCoordinator(DataUpdateCoordinator[dict]):
    """YoLink DataUpdateCoordinator."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        device: YoLinkDevice,
        paired_device: YoLinkDevice | None = None,
    ) -> None:
        """Init YoLink DataUpdateCoordinator.

        fetch state every 30 minutes base on yolink device heartbeat interval
        data is None before the first successful update, but we need to use
        data at first update
        """
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )
        self.device = device
        self.paired_device = paired_device
        self.dev_online = True
        self.dev_net_type = None

    def _process_device_state(self, device_state: dict) -> dict:
        """Process device state to extract nested fields for easier sensor access."""
        if device_state is None:
            return {}

        # Extract flowRate from nested state for water meters
        if (state_obj := device_state.get("state")) is not None and isinstance(state_obj, dict):
            if (flow_rate := state_obj.get("flowRate")) is not None:
                device_state["flow_rate"] = flow_rate

        # Extract recent usage amount for water meters
        if (recent_usage := device_state.get("recentUsage")) is not None and isinstance(recent_usage, dict):
            if (amount := recent_usage.get("amount")) is not None:
                device_state["recent_usage_amount"] = amount

        return device_state

    def async_set_updated_data(self, data: dict) -> None:
        """Manually update data, notify listeners, and process nested fields.

        This is called when MQTT messages arrive with real-time device state updates.
        We need to process the data to extract nested fields before setting it.
        """
        processed_data = self._process_device_state(data)
        super().async_set_updated_data(processed_data)

    async def _async_update_data(self) -> dict:
        """Fetch device state."""
        try:
            async with asyncio.timeout(10):
                device_state_resp = await self.device.fetch_state()
                device_state = device_state_resp.data.get(ATTR_DEVICE_STATE)
                device_reporttime = device_state_resp.data.get("reportAt")
                if device_reporttime is not None:
                    rpt_time_delta = (
                        datetime.now(tz=UTC).replace(tzinfo=None)
                        - datetime.strptime(device_reporttime, "%Y-%m-%dT%H:%M:%S.%fZ")
                    ).total_seconds()
                    self.dev_online = rpt_time_delta < YOLINK_OFFLINE_TIME
                if self.paired_device is not None and device_state is not None:
                    paried_device_state_resp = await self.paired_device.fetch_state()
                    paried_device_state = paried_device_state_resp.data.get(
                        ATTR_DEVICE_STATE
                    )
                    if (
                        paried_device_state is not None
                        and ATTR_DEVICE_STATE in paried_device_state
                    ):
                        device_state[ATTR_DEVICE_STATE] = paried_device_state[
                            ATTR_DEVICE_STATE
                        ]
        except YoLinkAuthFailError as yl_auth_err:
            raise ConfigEntryAuthFailed from yl_auth_err
        except YoLinkClientError as yl_client_err:
            _LOGGER.error(
                "Failed to obtain device status, device: %s, error: %s ",
                self.device.device_id,
                yl_client_err,
            )
            raise UpdateFailed from yl_client_err
        if device_state is not None:
            dev_lora_info = device_state.get(ATTR_LORA_INFO)
            if dev_lora_info is not None:
                self.dev_net_type = dev_lora_info.get("devNetType")
            return self._process_device_state(device_state)
        return {}

    async def call_device(self, request: ClientRequest) -> dict[str, Any]:
        """Call device api."""
        try:
            # call_device will check result, fail by raise YoLinkClientError
            resp: BRDP = await self.device.call_device(request)
        except YoLinkAuthFailError as yl_auth_err:
            self.config_entry.async_start_reauth(self.hass)
            raise HomeAssistantError(yl_auth_err) from yl_auth_err
        except YoLinkClientError as yl_client_err:
            raise HomeAssistantError(yl_client_err) from yl_client_err
        else:
            return resp.data
