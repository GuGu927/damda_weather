from __future__ import annotations

from urllib.parse import quote_plus, unquote
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import CONF_R, DOMAIN, CONF_API, CONF_S, CONF_X, CONF_Y, OPTION_LIST

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_API): str,
        vol.Required(CONF_S): str,
        vol.Required(CONF_X): cv.positive_int,
        vol.Required(CONF_Y): cv.positive_int,
        vol.Optional(CONF_R): str,
    }
)


def make_unique(i):
    """unique_id 문자열 생성."""
    return f"{i[CONF_API]}_{i[CONF_S]}_{i[CONF_X]}_{i[CONF_Y]}"


def check_key(i):
    """API 키 인코딩 정규화(필요 시 quote_plus 적용)."""
    i_key = i[CONF_API].strip()
    k_dec = unquote(i_key)
    if i_key == k_dec:
        i[CONF_API] = quote_plus(i_key)
    return i


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Damda Weather."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """최초 설정 플로우."""
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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """옵션 플로우 생성(HA 2025.12+ 호환: config_entry를 handler에 넘기지 않음)."""
        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Damda Weather."""

    async def async_step_init(self, user_input=None):
        """옵션 플로우 엔트리 포인트(항상 init부터 시작)."""
        conf = self.config_entry  # HA가 자동 주입 :contentReference[oaicite:1]{index=1}

        if conf.source == config_entries.SOURCE_IMPORT:
            # data_schema=None은 버전에 따라 문제될 수 있어 빈 스키마로 표시
            return self.async_show_form(step_id="init", data_schema=vol.Schema({}))

        if user_input is not None:
            return self.async_create_entry(data=user_input)

        options_schema = {}
        data_list = [CONF_API, CONF_S, CONF_X, CONF_Y, CONF_R]
        data_opt = [CONF_R]

        for name, default, validation in OPTION_LIST:
            to_default = conf.options.get(name, default)
            if name in data_list and conf.options.get(name, default) == default:
                to_default = conf.data.get(name, default)

            key = (
                vol.Optional(name, default=to_default)
                if name in data_opt
                else vol.Required(name, default=to_default)
            )
            options_schema[key] = validation

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(options_schema),
        )
