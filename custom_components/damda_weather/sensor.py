"""Damda Weather's sensor entity."""
from homeassistant.core import callback

from .const import (
    SENSOR_DOMAIN,
    DEVICE_CLASS,
    DEVICE_ICON,
    DEVICE_UNIQUE,
    DEVICE_UNIT,
    NAME,
)
from .dweather_device import DWeatherDevice
from .api_dweather import get_api
import logging

_LOGGER = logging.getLogger(__name__)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{NAME}] Sensor > {val}")
    elif flag == 1:
        _LOGGER.info(f"[{NAME}] Sensor > {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{NAME}] Sensor > {val}")
    elif flag == 3:
        _LOGGER.error(f"[{NAME}] Sensor > {val}")


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor for Damda Waether component."""

    @callback
    def async_add_entity(devices=[]):
        """Add sensor from api_dweather."""
        entities = []
        api = get_api(hass, config_entry)
        if api:
            try:
                if len(devices) == 0:
                    devices = api.sensors()
            except Exception:
                devices = []
            for device in devices:
                if DEVICE_UNIQUE not in device:
                    continue
                if not api.search_entity(SENSOR_DOMAIN, device[DEVICE_UNIQUE]):
                    entities.append(DWeatherSensor(device, api))

        if entities:
            async_add_entities(entities)

    api = get_api(hass, config_entry)
    if api:
        api.load(SENSOR_DOMAIN, async_add_entity)

    async_add_entity()


class DWeatherSensor(DWeatherDevice):
    """Representation of a DamdaWeather sensor."""

    TYPE = SENSOR_DOMAIN

    @property
    def state(self):
        """Return the state of the sensor."""
        state = self.api.get_state(self.unique_id)
        if state is not None:
            return state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        value = self.api.get_state(self.unique_id, DEVICE_ICON)
        if value == "":
            return None
        return value

    @property
    def device_class(self):
        """Return the class of the sensor."""
        value = self.api.get_state(self.unique_id, DEVICE_CLASS)
        if value == "":
            return None
        return value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this sensor."""
        value = self.api.get_state(self.unique_id, DEVICE_UNIT)
        return value

    @property
    def state_class(self):
        """Type of this sensor state."""
        return "measurement"
