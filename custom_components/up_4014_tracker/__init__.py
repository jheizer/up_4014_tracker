"""The UP 4014 Big Boy Tracker integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .coordinator import UP4014Coordinator

PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER]

from .coordinator import UP4014Coordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up UP 4014 Big Boy Tracker from a config entry."""
    refresh_interval = entry.data.get("refresh_interval", DEFAULT_SCAN_INTERVAL)
    coordinator = UP4014Coordinator(hass, refresh_interval)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok