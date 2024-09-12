"""Coordinator for UP 4014 Big Boy Tracker."""
from datetime import timedelta
import logging

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL, URL

_LOGGER = logging.getLogger(__name__)

class UP4014Coordinator(DataUpdateCoordinator):
    """Class to manage fetching UP 4014 data."""

    def __init__(self, hass: HomeAssistant, refresh_interval: int) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=refresh_interval),
        )
        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        """Fetch data from UP website."""
        try:
            async with self.session.get(URL) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error communicating with API: {response.status}")
                return await response.text()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err