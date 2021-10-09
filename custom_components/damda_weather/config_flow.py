"""Config flow for Damda Weather integration."""
from __future__ import annotations
from urllib.parse import quote_plus, unquote
from homeassistant.const import CONF_NAME
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_API, CONF_S, CONF_X, CONF_Y

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_API): str,
        vol.Required(CONF_S): str,
        vol.Required(CONF_X): vol.Coerce(int),
        vol.Required(CONF_Y): vol.Coerce(int),
    }
)


def make_unique(i):
    """Make unique_id."""
    return f"{i[CONF_API]}_{i[CONF_S]}_{i[CONF_X]}_{i[CONF_Y]}"


def check_key(i):
    """Check input data is valid and return data."""
    i_key = i[CONF_API].strip()
    k_dec = unquote(i_key)
    if i_key == k_dec:
        i[CONF_API] = quote_plus(i_key)
    return i


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Damda Weather."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            user_input = check_key(user_input)
            await self.async_set_unique_id(make_unique(user_input))
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
