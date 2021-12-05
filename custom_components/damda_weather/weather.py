"""Damda Weather's weather entity."""
from datetime import timedelta
from homeassistant.core import callback
from homeassistant.components.weather import WeatherEntity

from .const import (
    WEATHER_DOMAIN,
    DEVICE_UNIQUE,
    NAME,
    TEMP_CELSIUS,
    W_COND,
    W_FCST,
    W_HUMI,
    W_O3,
    W_TEMP,
    W_WD,
    W_WS,
)
from .dweather_device import DWeatherDevice
from .api_dweather import get_api
import logging

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{NAME}] Weather > {val}")
    elif flag == 1:
        _LOGGER.info(f"[{NAME}] Weather > {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{NAME}] Weather > {val}")
    elif flag == 3:
        _LOGGER.error(f"[{NAME}] Weather > {val}")


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Weather for Damda Weather component."""

    @callback
    def async_add_entity(devices=[]):
        """Add Weather from api_dweather."""
        entities = []
        api = get_api(hass, config_entry)
        if api:
            try:
                if len(devices) == 0:
                    devices = api.weathers()
            except Exception:
                devices = []
            for device in devices:
                if DEVICE_UNIQUE not in device:
                    continue
                if not api.search_entity(WEATHER_DOMAIN, device[DEVICE_UNIQUE]):
                    entities.append(DWeatherMain(device, api))

        if entities:
            async_add_entities(entities)

    api = get_api(hass, config_entry)
    if api:
        api.load(WEATHER_DOMAIN, async_add_entity)

    async_add_entity()


class DWeatherMain(DWeatherDevice, WeatherEntity):
    """Representation of a DamdaWeather weather."""

    TYPE = WEATHER_DOMAIN

    @property
    def status(self):
        """Return status of weather."""
        return self.api.get_state(self.unique_id)

    @property
    def temperature(self):
        """Return the temperature."""
        try:
            return float(self.status.get(W_TEMP))
        except Exception:
            return

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self):
        """Return the humidity."""
        try:
            return float(self.status.get(W_HUMI))
        except Exception:
            return

    @property
    def wind_speed(self):
        """Return the wind speed."""
        try:
            return float(self.status.get(W_WS))
        except Exception:
            return

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return self.status.get(W_WD)

    @property
    def condition(self):
        """Return the weather condition."""
        return self.status.get(W_COND)

    @property
    def ozone(self):
        """Return the weather ozone."""
        try:
            return float(self.status.get(W_O3))
        except Exception:
            return

    @property
    def attribution(self):
        """Return the attribution."""
        return f"담다날씨 [{self.api.location}] - Weather forecast from KMA and AIRKOREA."

    @property
    def forecast(self):
        """Return the forecast."""
        return self.status.get(W_FCST, {})

    @property
    def should_poll(self) -> bool:
        """Verify poll."""
        return "hourly" in self.unique_id

    async def async_update(self):
        """Update current conditions."""
        await self.api.update(True)
