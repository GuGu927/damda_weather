"""The Damda Weather integration."""
from __future__ import annotations

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from .api_dweather import DamdaWeatherAPI as API

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, NAME, BRAND, API_NAME

_LOGGER = logging.getLogger(__name__)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{BRAND}] {val}")
    elif flag == 1:
        _LOGGER.info(f"[{BRAND}] {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{BRAND}] {val}")
    elif flag == 3:
        _LOGGER.error(f"[{BRAND}] {val}")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Damda Weather from a config entry."""
    log(1, f"{NAME} Initialize")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(API_NAME, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    api = API(hass, entry, len(hass.data[DOMAIN][API_NAME]) + 1)
    hass.data[DOMAIN][API_NAME][entry.entry_id] = api
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    if hass.is_running:
        hass.async_add_job(api.update, True)
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, api.update)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        hass.data[DOMAIN][API_NAME].pop(entry.entry_id)
    log(1, f"{NAME} Unload {unload_ok}")

    return unload_ok
