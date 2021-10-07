"""Device class."""
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback

from .const import (
    CAST_TYPE,
    DEVICE_ATTR,
    DEVICE_ENTITY,
    DEVICE_ID,
    DEVICE_NAME,
    DOMAIN,
    DEVICE_UNIQUE,
    DEVICE_REG,
    NAME,
)

import logging

_LOGGER = logging.getLogger(__name__)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{NAME}] {val}")
    elif flag == 1:
        _LOGGER.info(f"[{NAME}] {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{NAME}] {val}")
    elif flag == 3:
        _LOGGER.error(f"[{NAME}] {val}")


class DWeatherBase:
    """Base class."""

    def __init__(self, device, api):
        """Init device class."""
        self._device = device
        self.api = api
        self.register = self._device[DEVICE_REG]
        self.device_available = True

    @property
    def unique_id(self) -> str:
        """Get unique ID."""
        return self._device[DEVICE_UNIQUE]

    @property
    def cast_type(self) -> str:
        """Get Cast Type."""
        return (
            self._device.get(DEVICE_ENTITY, {DEVICE_ATTR: {CAST_TYPE: ""}})
            .get(DEVICE_ATTR)
            .get(CAST_TYPE)
        )

    @property
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "connections": {
                (
                    self.api.location,
                    self.unique_id,
                )
            },
            "identifiers": {(DOMAIN, f"{self.api.location}_{self.cast_type}")},
            "manufacturer": f"{self.api.brand}",
            "model": f"{self.api.brand}_{self.api.version}",
            "name": f"{self.api.name} {self.api.location} {self.cast_type}",
            "sw_version": self.api.version,
            "via_device": (DOMAIN, self.api.location),
        }


class DWeatherDevice(DWeatherBase, Entity):
    """Defines a Pad Device entity."""

    TYPE = ""

    def __init__(self, device, api):
        """Initialize the instance."""
        super().__init__(device, api)
        self.api.set_entity(self.TYPE, self.unique_id, True)

    @property
    def entity_registry_enabled_default(self):
        """entity_registry_enabled_default."""
        return True

    async def async_added_to_hass(self):
        """Subscribe to device events."""
        self.register(self.unique_id, self.update_from_api)
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        """Disconnect device object when removed."""
        self.api.set_entity(self.TYPE, self.unique_id, False)
        self.register(self.unique_id)

    @callback
    def async_update_callback(self):
        """Update the device's state."""
        self.async_write_ha_state()

    @callback
    def update_from_api(self, avb):
        """Update the device's state."""
        self.device_available = avb
        self.async_update_callback()

    @property
    def available(self):
        """Return True if device is available."""
        if self.device_available is not True:
            return False
        return True

    @property
    def name(self) -> str:
        """Return the name of the device."""
        target = DEVICE_ID
        if not self.api.get_data(self.unique_id):
            self.api.set_data(self.unique_id, True)
        else:
            target = DEVICE_NAME
        return self.api.get_state(self.unique_id, target)

    @property
    def should_poll(self) -> bool:
        """No polling needed for this device."""
        return False

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        attr = self.api.get_state(self.unique_id, DEVICE_ATTR)
        return attr
