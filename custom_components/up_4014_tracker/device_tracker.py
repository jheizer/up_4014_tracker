"""Support for UP 4014 Big Boy Tracker."""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UP4014Coordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the UP 4014 Big Boy Tracker platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([UP4014TrackerEntity(coordinator)], True)

class UP4014TrackerEntity(CoordinatorEntity, TrackerEntity):
    """Representation of a UP 4014 Big Boy Tracker."""

    def __init__(self, coordinator: UP4014Coordinator) -> None:
        """Initialize the tracker."""
        super().__init__(coordinator)
        self._attr_unique_id = "up_4014_big_boy"
        self._attr_name = "UP 4014 Big Boy"

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        try:
            equipment = ET.fromstring(self.coordinator.data).find('equipment')
            return float(equipment.find('gpsLat').text)
        except (AttributeError, ValueError, TypeError):
            return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        try:
            equipment = ET.fromstring(self.coordinator.data).find('equipment')
            return float(equipment.find('gpsLon').text)
        except (AttributeError, ValueError, TypeError):
            return None

    @property
    def location_name(self) -> str | None:
        """Return a location name for the current location of the device."""
        try:
            equipment = ET.fromstring(self.coordinator.data).find('equipment')
            city = equipment.find('city').text
            state = equipment.find('state').text
            return f"{city}, {state}"
        except AttributeError:
            return None

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes of the device."""
        try:
            equipment = ET.fromstring(self.coordinator.data).find('equipment')
            return {
                "id": equipment.find('id').text,
                "updated": equipment.find('updated').text,
                "fuel": int(equipment.find('fuel').text),
                "speed": int(equipment.find('speed').text),
                "heading": int(equipment.find('heading').text)
            }
        except (AttributeError, ValueError):
            return {}