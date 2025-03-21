"""API for KMA weather and AirKorea from 'data.go.kr'."""
from math import sqrt
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
import logging
import requests
import re
import json
import xmltodict
import time

from types import FunctionType
from datetime import datetime, timedelta, timezone

from .const import (
    AIRKOREA_ITEM,
    AIRKOREA_URL,
    API_NAME,
    BRAND,
    CAST,
    CAST_A,
    CAST_BDATE,
    CAST_CODE,
    CAST_DTIME,
    CAST_EN,
    CAST_F,
    CAST_FDATE,
    CAST_ML,
    CAST_MT,
    CAST_R,
    CAST_TYPE,
    CAST_V,
    CAST_VALUE,
    CATEGORY_CODE,
    CODE_PTY_REV,
    CODE_SKY_REV,
    CONDITION_MAP,
    CONF_API,
    CONF_R,
    CONF_S,
    CONF_X,
    CONF_Y,
    DEVICE_ATTR,
    DEVICE_CLASS,
    DEVICE_DOMAIN,
    DEVICE_ENTITY,
    DEVICE_ICON,
    DEVICE_ID,
    DEVICE_NAME,
    DEVICE_REG,
    DEVICE_STATE,
    DEVICE_UNIQUE,
    DEVICE_UNIT,
    DEVICE_UPDATE,
    DOMAIN,
    ERROR_CODE,
    ICON_SKY_MID_VALUE,
    ITEM_BDATE,
    ITEM_BTIME,
    ITEM_CATEGORY,
    ITEM_FDATE,
    ITEM_FTIME,
    ITEM_FVALUE,
    ITEM_OVALUE,
    KMA_MID_URL,
    KMA_URL,
    MANUFACTURER,
    MODEL,
    NAME,
    NAME_KOR,
    OPT_MONITORING,
    VERSION,
    SENSOR_DOMAIN,
    W_COND,
    W_DT,
    W_FCST,
    W_FCST_D,
    W_FCST_H,
    W_HUMI,
    W_LIST,
    W_PCP,
    W_POP,
    W_PTY,
    W_SKY,
    W_TEMP,
    W_WS,
    WEATHER_DOMAIN,
)

_LOGGER = logging.getLogger(__name__)
ZONE = timezone(timedelta(hours=9))

DEBUG = False
DATE_NAME = {"0": "오늘", "1": "내일", "2": "모레"}


@callback
def get_api(hass, entry):
    """Return gateway with a matching entry_id."""
    return hass.data[DOMAIN][API_NAME].get(entry.entry_id)


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


def isfloat(value):
    """Determine string is float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def isnumber(value):
    """Determine string is number."""
    return (
        value is not None
        and isinstance(value, (str, int, float))
        and (
            isinstance(value, str)
            and (value.isnumeric() or value.isdigit())
            or isfloat(value)
        )
    )


def to_second(fmt, f, b):
    """Diff time to seconds."""
    return int((datetime.strptime(f, fmt) - datetime.strptime(b, fmt)).total_seconds())


def merge_dicts(a, b):
    """Merge dict."""
    c = a.copy()
    c.update(b)
    return c


def calc_windchill(t, v):
    """Calculate Apparent temperature."""
    t = float(t)
    v = float(v)
    # JAG/TI 모델을 토대로한 새로운 최적의 모델
    wc = round(
        13.12 + 0.6215 * t - 11.37 * pow(v, 0.16) + 0.3965 * t * pow(v, 0.16),
        1,
    )
    # JAG/TI 모델
    # wc = round(
    #     13.127 + 0.6215 * t - 13.947 * pow(v, 0.16) + 0.486 * t * pow(v, 0.16),
    #     1,
    # )
    return wc


def calc_heatindex(t, h):
    """Calculate Heat index."""
    f = (t * 9 / 5) + 32
    hi = (
        -42.379
        + 2.04901523 * f
        + 10.14333127 * h
        - 0.22475541 * f * h
        - 6.83783 * pow(10, -3) * pow(f, 2)
        - 5.481717 * pow(10, -2) * pow(h, 2)
        + 1.22874 * pow(10, -3) * pow(f, 2) * h
        + 8.5282 * pow(10, -4) * f * pow(h, 2)
        - 1.99 * pow(10, -6) * pow(f, 2) * pow(h, 2)
    )
    if h < 13 and f > 80 and f < 112:
        hi += ((13 - h) / 4) * sqrt((17 - abs(f - 95)) / 17)
    elif h > 85 and f > 80 and f < 87:
        hi += ((h - 85) / 10) * ((87 - f) / 5)
    elif f < 80:
        hi = 0.5 * (f + 61 + ((f - 68) * 1.2) + (h * 0.094))
    return round(5 / 9 * (hi - 32), 1)


def getCastTime(cast):
    """getUltraSrtNcst:초단기실황조회, getUltraSrtFcst:초단기예보조회, getVilageFcst:단기예보조회."""
    utc = datetime.now(timezone.utc)
    kst = utc.astimezone(ZONE)
    now = kst
    now_h1 = now - timedelta(hours=1)
    now_d1 = now - timedelta(days=1)
    now_hm = int(now.strftime("%H%M"))
    now_m = int(now.strftime("%M"))
    now_h = int(now.strftime("%H"))
    now_h1_h = int(now_h1.strftime("%H"))
    dt = []
    try:
        if cast == CAST_A:
            cast_time = now_h1_h if now_m <= 15 else now_h
            cast_date = now_d1 if now_hm <= 15 else now
            base_time = "{0:02d}00".format(cast_time)
            base_date = cast_date.strftime("%Y%m%d")
            base_time2 = "{0:02d}:00".format(cast_time)
            base_date2 = cast_date.strftime("%Y-%m-%d")
            dt.append([base_date, base_time, base_date2, base_time2])
        elif cast == CAST_R:
            cast_time = now_h1_h if now_m <= 40 else now_h
            cast_date = now_d1 if now_hm <= 40 else now
            base_time = "{0:02d}00".format(cast_time)
            base_date = cast_date.strftime("%Y%m%d")
            base_time2 = "{0:02d}:00".format(cast_time)
            base_date2 = cast_date.strftime("%Y-%m-%d")
            dt.append([base_date, base_time, base_date2, base_time2])
        elif cast == CAST_F:
            cast_time = now_h1_h if now_m <= 45 else now_h
            cast_date = now_d1 if now_hm <= 45 else now
            base_time = "{0:02d}30".format(cast_time)
            base_date = cast_date.strftime("%Y%m%d")
            base_time2 = "{0:02d}:30".format(cast_time)
            base_date2 = cast_date.strftime("%Y-%m-%d")
            dt.append([base_date, base_time, base_date2, base_time2])
        elif cast == CAST_V:
            if now_hm < 2300:
                base_time = "2300"
                base_date = now_d1.strftime("%Y%m%d")
                base_time2 = "23:00"
                base_date2 = now_d1.strftime("%Y-%m-%d")
                dt.append([base_date, base_time, base_date2, base_time2])
            # else:
            for i in range(2, 24):
                compare = int("{0:02d}10".format(i))
                base_time = "{0:02d}00".format(i)
                base_date = now.strftime("%Y%m%d")
                base_time2 = "{0:02d}:00".format(i)
                base_date2 = now.strftime("%Y-%m-%d")
                if now_hm > compare and (i + 1) % 3 == 0:
                    dt.append([base_date, base_time, base_date2, base_time2])
        elif cast in [CAST_MT, CAST_ML]:
            if now_hm >= 630 and now_hm < 1830:
                base_time = "0600"
                base_date = now.strftime("%Y%m%d")
                base_time2 = "06:00"
                base_date2 = now.strftime("%Y-%m-%d")
                dt.append([base_date, base_time, base_date2, base_time2])
            elif now_hm >= 1830:
                base_time = "1800"
                base_date = now.strftime("%Y%m%d")
                base_time2 = "18:00"
                base_date2 = now.strftime("%Y-%m-%d")
                dt.append([base_date, base_time, base_date2, base_time2])
            elif now_hm < 630:
                base_time = "1800"
                base_date = now_d1.strftime("%Y%m%d")
                base_time2 = "18:00"
                base_date2 = now_d1.strftime("%Y-%m-%d")
                dt.append([base_date, base_time, base_date2, base_time2])

    except Exception as ex:
        log(3, f"getCastTime > {cast} > {ex}")
    return dt


def getAirItem(item, target, default=None):
    """Get latest target from item."""
    for c_ori in item:
        c = c_ori.copy()
        v = c.get(target)
        if v and v != "-":
            return v
    return default


def convKMAcondition(table):
    """Convert table condition code to condition msg."""
    sky = table.get(W_SKY, "exceptional")
    pty = table.get(W_PTY, "없음")
    condition = sky if pty == "없음" else pty
    return CONDITION_MAP.get(condition, condition)


def convKMAitems(target, c, code, value, unit, device_icon):
    """Convert value, unit, device_icon."""
    try:
        if isinstance(device_icon, dict):
            device_icon = device_icon.get(str(value), "")
        elif isinstance(device_icon, FunctionType):
            device_icon = device_icon(value)
    except Exception as ex:
        log(3, f"[{target}] Parse device icon error > {ex} > {device_icon} > {c}")
    if code in ["PCP", "RN1", "SNO"] and value in [
        "없음",
        "강수없음",
        "0.5cm",
        "1mm 미만",
        "1.0mm 미만",
        "1mm미만",
        "1.0mm미만",
        "1cm 미만",
        "1.0cm 미만",
        "1cm미만",
        "1.0cm미만",
        "적설없음",
    ]:
        value = "0"
    try:
        if isinstance(unit, dict):
            value = unit.get(str(value), value)
            unit = ""
        elif isinstance(unit, FunctionType):
            value, unit = unit(value)
    except Exception as ex:
        log(3, f"[{target}] Parse unit error > {ex} > {unit} > {c}")
    try:
        if isnumber(value):
            value = (
                int(float(value))
                if (
                    code in ["REH", "POP", "TMP", "TMN", "TMX"]
                    or (target == CAST_F and code in ["T1H"])
                )
                else float(value)
            )
            if isfloat(value) and float(value) < -900:
                value = None
        elif isinstance(value, str):
            if "mm" in value or "cm" in value:
                value = value[0 : len(value) - 2]
                if isnumber(value):
                    value = float(value)
                else:
                    unit = ""
            elif "mm " in value or "cm " in value:
                value = value[0 : len(value) - 3]
                if isnumber(value):
                    value = float(value)
                else:
                    unit = ""
            else:
                unit = None
    except Exception as ex:
        log(3, f"[{target}] Parse value error > {ex} > {value} > {c}")
    return value, unit, device_icon


class DamdaWeatherAPI:
    """DamdaWeather API."""

    def __init__(self, hass, entry, count):
        """Initialize the Weather API."""
        self.hass = hass
        self.entry = entry
        self.count = count
        self.device = {}  # unique_id: device
        self.entities = {
            SENSOR_DOMAIN: {},
            WEATHER_DOMAIN: {},
        }  # unique_id: True/False
        self.loaded = {SENSOR_DOMAIN: False, WEATHER_DOMAIN: False}
        self.result = {}
        self.weather = {W_FCST_D: {}, W_FCST_H: {}}
        self.listeners = []
        self.last_data = {}
        self.last_update = {}
        self.try_update = {}
        self.try_target = {}
        self.temperature = None
        self.wind_speed = None
        self.humidity = None
        self._start = False
        self._last_error = 0
        self.log(1, "Loading API")

    @property
    def api_key(self) -> str:
        """Return the API key."""
        return self.entry.options.get(CONF_API, self.entry.data.get(CONF_API))

    @property
    def grid_x(self) -> str:
        """Return the API key."""
        return self.entry.options.get(CONF_X, self.entry.data.get(CONF_X))

    @property
    def grid_y(self) -> str:
        """Return the API key."""
        return self.entry.options.get(CONF_Y, self.entry.data.get(CONF_Y))

    @property
    def reg_id(self) -> str:
        """Return the reg id."""
        return self.entry.options.get(CONF_R, self.entry.data.get(CONF_R, "")).strip()

    @property
    def station(self) -> str:
        """Return the air station."""
        return self.entry.options.get(CONF_S, self.entry.data.get(CONF_S))

    @property
    def location(self) -> str:
        """Return the user defined name."""
        return self.entry.options.get(CONF_NAME, self.entry.data.get(CONF_NAME))

    def load(self, domain, async_add_entity):
        """Component loaded."""
        self.loaded[domain] = True
        self.listeners.append(
            async_dispatcher_connect(
                self.hass, self.async_signal_new_device(domain), async_add_entity
            )
        )
        if self.complete and not self._start:
            self._start = True
        self.log(1, f"Component loaded [{self.location}] -> {domain}")

    @property
    def complete(self):
        """Component loaded."""
        for v in self.loaded.values():
            if not v:
                return False
        return True

    def log(self, level, msg, isMonitor=False):
        """Log."""
        if not isMonitor or (isMonitor and self.get_option(OPT_MONITORING, False)):
            log(level, f"[{self.location}] {msg}")

    def set_data(self, key, value):
        """Set entry data."""
        self.hass.config_entries.async_update_entry(
            entry=self.entry, data={**self.entry.data, key: value}
        )
        return value

    def get_data(self, key, default=False):
        """Get entry data."""
        return self.entry.data.get(key, default)

    def get_option(self, name, default=False):
        """Get entry option."""
        return self.entry.options.get(name, default)

    @property
    def manufacturer(self) -> str:
        """Get manufacturer."""
        return MANUFACTURER

    @property
    def version(self) -> str:
        """Get version."""
        return VERSION

    @property
    def brand(self) -> str:
        """Get brand."""
        return BRAND

    @property
    def name(self) -> str:
        """Get name."""
        return NAME_KOR

    @property
    def model(self) -> str:
        """Get model."""
        return MODEL

    def async_signal_new_device(self, device_type) -> str:
        """Damda Weather specific event to signal new device."""
        new_device = {
            SENSOR_DOMAIN: "dweather_new_sensor",
            WEATHER_DOMAIN: "dweather_new_weather",
        }
        return f"{new_device[device_type]}_{self.location}"

    def async_add_device(self, device=None, force: bool = False) -> None:
        """Handle event of new device creation in dweather."""

        if device is None or not isinstance(device, dict):
            return
        args = []
        unique_id = device.get(DEVICE_UNIQUE, None)
        domain = device.get(DEVICE_DOMAIN)
        if (
            self.search_entity(domain, unique_id)
            or not self.loaded.get(domain, False)
            or unique_id in self.hass.data[DOMAIN]
        ):
            return

        args.append([device])

        async_dispatcher_send(self.hass, self.async_signal_new_device(domain), *args)

    def sensors(self):
        """Get sensors."""
        target = SENSOR_DOMAIN
        return self.get_entities(target)

    def weathers(self):
        """Get weathers."""
        target = WEATHER_DOMAIN
        return self.get_entities(target)

    def init_device(self, unique_id, domain, device=None):
        """Init device."""
        init_info = {
            DEVICE_DOMAIN: domain,
            DEVICE_REG: self.register_update_state,
            DEVICE_UPDATE: None,
            DEVICE_UNIQUE: unique_id,
            DEVICE_ENTITY: device,
        }
        if domain in self.entities:
            self.entities[domain].setdefault(unique_id, False)
        if unique_id not in self.device:
            self.log(0, f"Initialize device > {domain} > {unique_id}")
        return self.device.setdefault(unique_id, init_info)

    def search_device(self, unique_id):
        """Search self.device."""
        return self.device.get(unique_id)

    def search_entity(self, domain, unique_id):
        """Search self.entities domain unique_id."""
        return self.entities.get(domain, {}).get(unique_id, False)

    def registered(self, unique_id):
        """Check unique_id is registered."""
        device = self.search_device(unique_id)
        return device.get(unique_id).get(DEVICE_UPDATE) is not None if device else False

    def get_entities(self, domain):
        """Get self.device from self.entites domain."""
        entities = []
        entity_list = self.entities.get(domain, {})
        for id in entity_list.keys():
            device = self.search_device(id)
            if device:
                entities.append(device)
            else:
                entities.append(self.init_device(id, domain))
        return entities

    def set_entity(self, domain, unique_id, state=False):
        """Set self.entities domain unique_id True/False."""
        if domain not in self.entities:
            self.log(1, f"set_entity > {domain} not exist.")
            pass
        if unique_id not in self.entities[domain]:
            self.log(1, f"set_entity > {domain} > {unique_id} not exist.")
            pass
        if state:
            self.entities[domain][unique_id] = state
            self.hass.data[DOMAIN][self.entry.entry_id][unique_id] = state
        else:
            self.entities[domain].pop(unique_id)
            self.hass.data[DOMAIN][self.entry.entry_id].pop(unique_id)

    def get_state(self, unique_id, target=DEVICE_STATE):
        """Get device state."""
        device = self.search_device(unique_id)
        return device.get(DEVICE_ENTITY).get(target, None) if device else None

    def set_device(self, unique_id, entity):
        """Set device entity."""
        device = self.search_device(unique_id)
        if device:
            try:
                self.device[unique_id][DEVICE_ENTITY].update(entity)
            except Exception as ex:
                self.log(3, f"Set entity error > {unique_id} > {entity} > {ex}")

    def register_update_state(self, unique_id, cb=None):
        """Register device update function to update entity state."""
        device = self.search_device(unique_id)
        if device:
            if (device.get(DEVICE_UPDATE) is None and cb is not None) or (
                device.get(DEVICE_UPDATE) is not None and cb is None
            ):
                msg = f"{'Register' if cb is not None else 'Unregister'} device of [{self.location}] => {unique_id}"
                self.log(0, msg)
                self.device[unique_id][DEVICE_UPDATE] = cb

    def update_entity(self, unique_id, entity, available=True):
        """Update device state."""
        device = self.search_device(unique_id)
        if not device:
            return
        self.device[unique_id][DEVICE_ENTITY].update(entity)
        if device.get(DEVICE_UPDATE) is not None:
            device.get(DEVICE_UPDATE)(available)
        else:
            self.async_add_device(device)

    def make_entity(
        self, attr, icon, device_class, domain, state, unit, unique_id, entity_id, name
    ):
        """Make entity."""
        entity = {
            DEVICE_ATTR: {
                CONF_X: self.grid_x,
                CONF_Y: self.grid_y,
                CONF_S: self.station,
                CONF_NAME: self.location,
            },
            DEVICE_DOMAIN: domain,
            DEVICE_STATE: state,
            DEVICE_UNIQUE: unique_id,
            DEVICE_ID: entity_id,
            DEVICE_NAME: name,
        }
        if attr is not None:
            entity[DEVICE_ATTR].update(attr)
        if unit is not None:
            entity[DEVICE_UNIT] = unit
        if icon is not None:
            entity[DEVICE_ICON] = icon
        if device_class is not None:
            entity[DEVICE_CLASS] = device_class
        if state is None:
            entity.pop(DEVICE_STATE)
        return entity

    def set_weather(self, target, dt):  # noqa: C901
        """Set self.weather data."""
        dif_date = dt[0]
        now_dt = dt[1]
        forecast_h_dt = dt[2]
        forecast_h_time = dt[3]
        forecast_d_time = dt[4]
        code = dt[5]
        entity_id = dt[6]
        cast_time_hour = dt[7]
        entity = dt[8]
        device_icon = dt[9]
        device_class = dt[10]
        domain = dt[11]
        value = dt[12]
        unit = dt[13]
        self.weather[W_FCST_H].setdefault(forecast_h_time, {})
        self.weather[W_FCST_D].setdefault(forecast_d_time, {})

        if entity == W_WS:
            value = round(value * 3.6, 1)
        try:
            if target == CAST_R and entity in W_LIST:
                self.weather[entity] = value
                table = {
                    DEVICE_ICON: device_icon,
                    DEVICE_CLASS: device_class,
                    DEVICE_DOMAIN: domain,
                    DEVICE_STATE: value,
                    DEVICE_UNIT: unit,
                }
                if entity == W_TEMP:
                    self.temperature = table
                elif entity == W_WS:
                    self.wind_speed = table
                elif entity == W_HUMI:
                    self.humidity = table
            elif target == CAST_F:
                for e in ["_sky_1"]:
                    if e in entity_id:
                        self.weather[W_SKY] = value
                if forecast_h_dt > now_dt:
                    self.weather[W_FCST_H][forecast_h_time].update({entity: value})
            elif target in [CAST_ML, CAST_MT, CAST_V]:
                d_data = self.weather[W_FCST_D][forecast_d_time].copy()
                if code in ["TMN", "TMX"]:
                    entity = "temperature"
                if entity == "temperature":
                    max_v = d_data.get("temperature", -900)
                    min_v = d_data.get("templow", 900)
                    if code in ["TMN", "TMX"]:
                        self.weather[W_FCST_D][forecast_d_time][
                            "temperature" if code == "TMX" else "templow"
                        ] = value
                    if value > max_v:
                        self.weather[W_FCST_D][forecast_d_time]["temperature"] = value
                    if value < min_v:
                        self.weather[W_FCST_D][forecast_d_time]["templow"] = value
                elif entity in ["precipitation", "snow"]:
                    ov = float(
                        (
                            d_data.get(entity, 0)
                            if not (
                                int(cast_time_hour) == 0 or int(cast_time_hour) == 24
                            )
                            else 0
                        )
                    )
                    if value in ["30.0~50.0", "50.0mm "]:
                        value = 50
                    elif value == "0.5cm":
                        value = 5
                    self.weather[W_FCST_D][forecast_d_time][entity] = ov + value
                elif entity == W_POP:
                    ov = d_data.get(entity, 0)
                    if value >= ov:
                        self.weather[W_FCST_D][forecast_d_time][entity] = value
                elif entity in [W_SKY, W_PTY] and target in [CAST_V]:
                    default = "맑음" if entity == W_SKY else "없음"
                    code = CODE_SKY_REV if entity == W_SKY else CODE_PTY_REV
                    ovalue_code = int(code.get(d_data.get(entity, default), 0))
                    value_code = int(code.get(value, 0))
                    if value_code >= ovalue_code:
                        self.weather[W_FCST_D][forecast_d_time][entity] = value
                elif entity in [W_SKY, W_PTY] and target in [CAST_ML, CAST_MT]:
                    default = "맑음" if entity == W_SKY else "없음"
                    code = ICON_SKY_MID_VALUE
                    ovalue_code = int(code.get(d_data.get(entity, default), 0))
                    value_code = int(code.get(value, 0))
                    if value_code >= ovalue_code:
                        self.weather[W_FCST_D][forecast_d_time][entity] = value
                else:
                    self.weather[W_FCST_D][forecast_d_time].update({entity: value})
                if (
                    code not in ["TMN", "TMX"]
                    and (
                        dif_date > 0
                        and forecast_h_dt > now_dt
                        and forecast_h_dt - now_dt > timedelta(seconds=3600 * 8)
                        and int(cast_time_hour) % 3 == 0
                    )
                    or (
                        forecast_h_dt > now_dt
                        and forecast_h_dt - now_dt <= timedelta(seconds=3600 * 8)
                    )
                ):
                    self.weather[W_FCST_H][forecast_h_time].update({entity: value})
        except Exception as ex:
            self.log(3, f"Error at set_weather > {ex} > {target} > {dt}")

    def parse(self, url, result):
        """Parse result as url."""
        target = ""
        if CAST_R in url:
            target = CAST_R
        elif CAST_F in url:
            target = CAST_F
        elif CAST_V in url:
            target = CAST_V
        elif CAST_A in url:
            target = CAST_A
        elif CAST_ML in url:
            target = CAST_ML
        elif CAST_MT in url:
            target = CAST_MT
        if target in [CAST_R, CAST_F, CAST_V]:
            return self.parse_kma(target, result, url)
        elif target in [CAST_A]:
            return self.parse_air(target, result, url)
        elif target in [CAST_ML, CAST_MT]:
            return self.parse_kma_mid(target, result, url)
        return

    def parse_air(self, target, result, url):
        """Parse AirKorea data."""
        data = {}
        r_res = result.get("response", {})
        r_header = r_res.get("header", {})
        r_code = r_header.get("resultCode", "99")
        r_msg = r_header.get("resultMsg", "")
        r_total = 0
        try:
            if ERROR_CODE.get(r_code, None) is None:
                r_body = r_res.get("body", {})
                r_item = r_body.get("items", [])
                r_total = r_body.get("totalCount", 0)
                if len(r_item) > 0:
                    c = r_item[0].copy()
                    for vname, vlist in AIRKOREA_ITEM.items():
                        entity = vlist[0]
                        name = vlist[1]
                        unit = vlist[2]
                        domain = vlist[3]
                        device_icon = vlist[4]
                        device_class = vlist[5]
                        value = getAirItem(r_item, vname)
                        dtfmt = "%Y-%m-%d %H:%M"
                        data_time = getAirItem(r_item, "dataTime", "-")
                        if "24:00" in data_time:
                            data_time = (
                                datetime.strptime(data_time[0:10] + " 00:00", dtfmt)
                                + timedelta(days=1)
                            ).strftime(dtfmt)
                        data_time = datetime.strptime(data_time, dtfmt).replace(
                            tzinfo=ZONE
                        )
                        if data_time != "-":
                            self.last_update[target] = data_time.isoformat()
                        attr = {
                            CAST_TYPE: CAST[target],
                            CAST_DTIME: data_time.strftime(dtfmt),
                            CAST_VALUE: value,
                        }
                        try:
                            if isinstance(device_icon, dict):
                                device_icon = device_icon.get(str(value), "")
                            elif isinstance(device_icon, FunctionType):
                                device_icon = device_icon(value)
                        except Exception as ex:
                            self.log(
                                3,
                                f"[{target}] Parse device icon error > {ex} > {device_icon} > {c}",
                            )
                        try:
                            if isinstance(unit, dict):
                                value = unit.get(str(value), value)
                                unit = None
                            elif isinstance(unit, FunctionType):
                                attr[CAST_CODE] = value
                                value, unit = unit(value)
                        except Exception as ex:
                            self.log(
                                3, f"[{target}] Parse unit error > {ex} > {unit} > {c}"
                            )
                        try:
                            if value == "-":
                                pass
                            elif isnumber(value):
                                value = float(value)
                                unit = ""
                            elif value is None:
                                value = "-"
                        except Exception as ex:
                            self.log(
                                3,
                                f"[{target}] Parse value error > {ex} > {value} > {c}",
                            )
                        if entity in ["khai_value", "pm10_value", "pm25_value"]:
                            value = int(value) if value != "-" else "-"
                        unique_id = f"dw{self.count}_airkorea_{self.station}_{self.grid_x}_{self.grid_y}_{entity}"
                        entity_id = f"dw{self.count}_airkorea_{entity}"
                        device_name = f"{self.location} {name}"
                        data[unique_id] = self.make_entity(
                            attr,
                            device_icon,
                            device_class,
                            domain,
                            value,
                            unit,
                            unique_id,
                            entity_id,
                            device_name,
                        )
                        if entity in W_LIST:
                            self.weather[entity] = value

            else:
                self.last_update[target] = [r_code, r_msg, url]
                self.log(
                    2,
                    f"target parse_air [{target}] > {ERROR_CODE.get(r_code, r_code)} > {r_msg}[{r_code}] > {url} > {result}",
                )
        except Exception as ex:
            self.log(3, f"target parse_air [{target}] > {url} > {ex}")
        self.log(1, f"{target} -> total:{r_total} > data:{len(data)}", True)
        return data

    def parse_kma(self, target, result, url):
        """Parse KMA data."""
        utc = datetime.now(timezone.utc)
        kst = utc.astimezone(ZONE)
        data = {}
        r_res = result.get("response", {})
        r_header = r_res.get("header", {})
        r_code = r_header.get("resultCode", "99")
        r_msg = r_header.get("resultMsg", "")
        r_total = 0
        try:
            if ERROR_CODE.get(r_code, None) is None:
                if "NO DATA" in result:
                    pass
                r_body = r_res.get("body", {})
                r_item = r_body.get("items", {}).get("item", [])
                r_total = r_body.get("totalCount", 0)
                for c in r_item:
                    do_not_add = False
                    code = c.get(ITEM_CATEGORY)
                    category = CATEGORY_CODE.get(code)
                    if not category:
                        continue
                    entity, name, unit, domain, device_icon, device_class = (
                        category[0],
                        category[1],
                        category[2],
                        category[3],
                        category[4],
                        category[5],
                    )
                    value, o_value = c.get(ITEM_OVALUE, c.get(ITEM_FVALUE, "-")), c.get(
                        ITEM_OVALUE, c.get(ITEM_FVALUE, "-")
                    )

                    base_date, base_time = (
                        c.get(ITEM_BDATE) or 0,
                        c.get(ITEM_BTIME) or 0,
                    )
                    cast_date, cast_time = (
                        c.get(ITEM_FDATE) or base_date,
                        c.get(ITEM_FTIME) or base_time,
                    )
                    cast_time_hour = cast_time[0:2]
                    dif_date = 0
                    base_dt, cast_dt = base_date + base_time, cast_date + cast_time
                    dt = datetime.strptime(base_dt, "%Y%m%d%H%M").replace(tzinfo=ZONE)
                    fmt = "%Y-%m-%d %H:%M"
                    init_time = datetime(2000, 1, 1, tzinfo=ZONE)
                    last_update = self.last_update.get(target, init_time)
                    dt_last = None
                    if isinstance(last_update, str):
                        dt_last = datetime.fromisoformat(last_update).replace(
                            tzinfo=ZONE
                        )
                    else:
                        dt_last = init_time
                    if dt > dt_last:
                        self.last_update[target] = dt.isoformat()
                    now_dt = kst
                    now = now_dt.strftime("%Y%m%d")
                    if dt.replace(hour=0, minute=0) < now_dt.replace(hour=0, minute=0):
                        base_date = now
                    header = f"dw{self.count}_{CAST_EN[target]}"
                    tail = f" 현재 {cast_time_hour}시"
                    unique = f"{self.station}_{self.grid_x}_{self.grid_y}_{entity}"
                    entity_id = f"{header}_{entity}"
                    unique_id = f"{header}_{unique}"
                    if target == CAST_F:
                        dif_date = to_second("%Y%m%d%H%M", cast_dt, base_dt)
                        dif_date = int((dif_date + 1800) / 3600)
                        dif_date2 = to_second("%Y%m%d", cast_date, now)
                        dif_date2 = int(dif_date2 / 3600 / 24)
                        tail = f" {DATE_NAME.get(str(dif_date2), '')} {cast_time_hour}시"
                        entity_id = f"{header}_{entity}_{dif_date}"
                        unique_id = f"{header}_{unique}_{dif_date}"
                    elif target == CAST_V:
                        dif_date = to_second("%Y%m%d", cast_date, base_date)
                        dif_date = int(dif_date / 3600 / 24)
                        dif_date2 = to_second("%Y%m%d", cast_date, now)
                        dif_date2 = int(dif_date2 / 3600 / 24)
                        if dif_date2 > 0 and int(cast_time_hour) == 0:
                            dif_date2 -= 1
                            cast_time_hour = "24"
                        if (
                            # (
                            #     dif_date == 0
                            #     and int(cast_time_hour) < 24
                            #     and code not in ["TMX", "TMN"]
                            # ) or
                            int(cast_time_hour) % 3 > 0
                            or (dif_date2 == 3 and int(cast_time_hour) > 0)
                            or dif_date2 > 3
                        ):
                            do_not_add = True
                        if code not in ["TMX", "TMN"]:
                            tail = f" {DATE_NAME.get(str(dif_date2), '')} {cast_time_hour}시"
                            entity_id = f"{header}_{entity}_{dif_date}_{cast_time}"
                            unique_id = f"{header}_{unique}_{dif_date}_{cast_time}"
                        else:
                            tail = f" {DATE_NAME.get(str(dif_date2), '')}"
                            entity_id = f"{header}_{entity}_{dif_date}"
                            unique_id = f"{header}_{unique}_{dif_date}"
                    device_name = f"{self.location} {name}{tail}"

                    value, unit, device_icon = convKMAitems(
                        target, c, code, value, unit, device_icon
                    )
                    if not do_not_add:
                        data.setdefault(unique_id, {})
                        dtfmt = "%Y-%m-%d %H:%M"
                        attr = {
                            CAST_TYPE: CAST[target],
                            CAST_BDATE: datetime.strptime(
                                base_dt, "%Y%m%d%H%M"
                            ).strftime(dtfmt),
                            CAST_FDATE: datetime.strptime(
                                cast_dt, "%Y%m%d%H%M"
                            ).strftime(dtfmt),
                            CAST_CODE: code,
                            CAST_VALUE: o_value,
                        }
                        data[unique_id] = self.make_entity(
                            attr,
                            device_icon,
                            device_class,
                            domain,
                            value,
                            unit,
                            unique_id,
                            entity_id,
                            device_name,
                        )

                    if value is None:
                        continue
                    forecast_h_dt = datetime.strptime(cast_dt, "%Y%m%d%H%M").replace(
                        tzinfo=ZONE
                    )
                    forecast_h_time = forecast_h_dt.isoformat()
                    forecast_d_dt = forecast_h_dt.replace(hour=0, minute=0)
                    forecast_d_time = forecast_d_dt.isoformat()
                    weather_table = [
                        dif_date,
                        now_dt,
                        forecast_h_dt,
                        forecast_h_time,
                        forecast_d_time,
                        code,
                        entity_id,
                        cast_time_hour,
                        entity,
                        device_icon,
                        device_class,
                        domain,
                        value,
                        unit,
                    ]
                    self.set_weather(target, weather_table)
            else:
                self.last_update[target] = [r_code, r_msg, url]
                self.log(
                    2,
                    f"target parse_kma [{target}] > {ERROR_CODE.get(r_code, r_code)} > {r_msg}[{r_code}] > {url} > {result}",
                )
        except Exception as ex:
            self.log(3, f"target parse_kma [{target}] > {url} > {ex}")
        self.log(1, f"{target} -> total:{r_total} > data:{len(data)}", True)
        return data

    def parse_kma_mid(self, target, result, url):
        """Parse KMA midterm data."""
        utc = datetime.now(timezone.utc)
        kst = utc.astimezone(ZONE)
        now = kst
        data = {}
        r_res = result.get("response", {})
        r_header = r_res.get("header", {})
        r_code = r_header.get("resultCode", "99")
        r_msg = r_header.get("resultMsg", "")
        r_total = 0
        try:
            if ERROR_CODE.get(r_code, None) is None:
                if "NO DATA" in result:
                    pass
                r_body = r_res.get("body", {})
                r_item = r_body.get("items", {}).get("item", [])
                r_total = r_body.get("totalCount", 0)
                base_date = self.try_target.get(target, now.isoformat())
                base_dt = datetime.fromisoformat(base_date).replace(tzinfo=ZONE)
                self.last_update[target] = base_date
                for code, value in r_item[0].items():
                    category = CATEGORY_CODE.get(code)
                    if not category:
                        continue
                    entity, name, unit, domain, device_icon, device_class = (
                        category[0],
                        category[1],
                        category[2],
                        category[3],
                        category[4],
                        category[5],
                    )
                    device_icon = (
                        device_icon.get(value, value)
                        if isinstance(device_icon, dict)
                        else device_icon
                    )
                    header = f"dw{self.count}_{CAST_EN[target]}"
                    dif_date = [int(s) for s in re.findall(r"\d+", code)][0]
                    target_date = datetime.strftime(
                        base_dt + timedelta(days=dif_date), "%m/%d"
                    )
                    cast_dt = base_dt + timedelta(days=dif_date)
                    tail = target_date
                    if "_am" in entity or "_pm" in entity:
                        tail = f"{tail} {'오전' if '_am' in entity else '오후'}"
                    device_name = f"{self.location} {name} {tail}"
                    unique = f"{self.station}_{self.grid_x}_{self.grid_y}_{entity}"
                    entity_id = f"{header}_{entity}"
                    unique_id = f"{header}_{unique}"
                    target_entity = entity
                    for e in [W_POP, W_SKY, W_TEMP]:
                        if e in entity:
                            target_entity = e

                    data.setdefault(unique_id, {})
                    dtfmt = "%Y-%m-%d %H:%M"
                    attr = {
                        CAST_TYPE: CAST[target],
                        CAST_BDATE: base_dt.strftime(dtfmt),
                        CAST_FDATE: cast_dt.strftime(dtfmt),
                        CAST_CODE: code,
                        CAST_VALUE: value,
                    }
                    data[unique_id] = self.make_entity(
                        attr,
                        device_icon,
                        device_class,
                        domain,
                        value,
                        unit,
                        unique_id,
                        entity_id,
                        device_name,
                    )
                    forecast_h_dt = cast_dt
                    forecast_h_time = forecast_h_dt.isoformat()
                    forecast_d_dt = forecast_h_dt.replace(hour=0, minute=0)
                    forecast_d_time = forecast_d_dt.isoformat()
                    weather_table = [
                        dif_date,
                        now,
                        forecast_h_dt,
                        forecast_h_time,
                        forecast_d_time,
                        code,
                        entity_id,
                        "00",
                        target_entity,
                        device_icon,
                        device_class,
                        domain,
                        value,
                        unit,
                    ]
                    self.set_weather(target, weather_table)
            else:
                self.last_update[target] = [r_code, r_msg, url]
                self.log(
                    2,
                    f"target parse_kma_mid [{target}] > {ERROR_CODE.get(r_code, r_code)} > {r_msg}[{r_code}] > {url} > {result}",
                )
        except Exception as ex:
            self.log(3, f"target parse_kma_mid [{target}] > {url} > {ex}")
        self.log(1, f"{target} -> total:{r_total} > data:{len(data)}", True)
        return data

    def getCastURL(self, cast):
        """CAST_R:초단기실황, CAST_F:초단기예보, CAST_V:단기예보.

        CAST_ML:중기육상, CAST_MT:중기기온.
        """
        utc = datetime.now(timezone.utc)
        kst = utc.astimezone(ZONE)
        now = kst
        valid = False
        url = []
        base = getCastTime(cast)
        update_base = base[len(base) - 1]
        update_time = f"{update_base[2]} {update_base[3]}"
        fmt = "%Y-%m-%d %H:%M"
        init_time = datetime(2000, 1, 1).strftime(fmt)
        last_update = self.last_update.get(cast, init_time)
        if not isinstance(last_update, str):
            last_update = init_time
        last_try = self.try_update.get(cast, init_time)

        dt_update = datetime.strptime(update_time, fmt).replace(tzinfo=ZONE)
        dt_last = datetime.fromisoformat(last_update).replace(tzinfo=ZONE)
        dt_try = datetime.strptime(last_try, fmt).replace(tzinfo=ZONE)
        if init_time == dt_last.strftime(fmt) or dt_update > dt_last:
            valid = True
        if cast in [CAST_R, CAST_F] and now - dt_try > timedelta(minutes=10):
            valid = True
        if valid:
            if init_time != dt_last.strftime(fmt):
                msg = f"getCastURL > {CAST[cast]} > {valid} > target:{update_time} / before:{dt_last.strftime(fmt)} / now:{now.strftime(fmt)}"
                self.log(1, msg, True)
            else:
                msg = f"getCastURL > {CAST[cast]} > {valid} > target:{update_time} / now:{now.strftime(fmt)}"
                self.log(1, msg, True)
            self.try_update[cast] = now.strftime(fmt)
            self.try_target[cast] = dt_update.isoformat()
            if cast in [CAST_A]:
                url.append(AIRKOREA_URL.format(self.station, self.api_key))
            elif cast in [CAST_R, CAST_F, CAST_V]:
                for b in base:
                    url.append(
                        KMA_URL.format(
                            cast, self.api_key, self.grid_x, self.grid_y, b[0], b[1]
                        )
                    )
            elif (
                cast in [CAST_MT, CAST_ML]
                and self.reg_id is not None
                and self.reg_id not in [""]
            ):
                reg_id = self.reg_id
                if cast == CAST_ML:
                    reg_id = (
                        (reg_id[0:3] + "00000")
                        if reg_id[2] in ["B", "G"]
                        else (reg_id[0:4] + "0000")
                    )
                for b in base:
                    url.append(
                        KMA_MID_URL.format(cast, self.api_key, reg_id, b[0], b[1])
                    )
        return url

    def pretty_print(self, items):
        """Print items."""
        s0 = [0, 0]
        try:
            for v in items.values():
                s1 = []
                s1.append(len(v.get(DEVICE_ATTR).get(CAST_TYPE)))
                s1.append(len(v.get(DEVICE_ID)))
                for i, l in enumerate(s0):
                    if s1[i] > l:
                        s0[i] = s1[i]
            for v in items.values():
                s1 = []
                s1.append(len(v.get(DEVICE_ATTR).get(CAST_TYPE)))
                s1.append(len(v.get(DEVICE_ID)))
                s2 = [s0[0] - s1[0], s0[1] - s1[1]]
                msg = f"{v.get(DEVICE_ATTR).get(CAST_TYPE)}{' '*s2[0]} > {v.get(DEVICE_ATTR).get(CAST_FDATE,'')} > {v.get(DEVICE_ID)}{' '*s2[1]} > {v.get(DEVICE_STATE)}{v.get(DEVICE_UNIT,'')}"
                self.log(0, msg)
        except Exception as ex:
            self.log(0, f"pretty_print > {ex} > {items}")

    async def get_target(self, target, target_list):
        """Get target data from target_list."""
        data = {}
        utc = datetime.now(timezone.utc)
        kst = utc.astimezone(ZONE)
        now = kst

        async def getDataFromUrl(url):
            """Get data."""
            response = await self.hass.async_add_executor_job(requests.get, url)
            try:
                r_parse = response.json()
            except Exception:
                r_xml = response.content
                r_parse = json.loads(json.dumps(xmltodict.parse(r_xml)))
            open_api_response = r_parse.get("OpenAPI_ServiceResponse")
            if open_api_response:
                msg_header = open_api_response.get("cmmMsgHeader", {})
                err_msg = msg_header.get("errMsg", "-")
                auth_msg = msg_header.get("returnAuthMsg", "-")
                reason_code = msg_header.get("returnReasonCode", "-")
                self.log(
                    0,
                    f"OpenAPI_ServiceResponse > {err_msg} > {auth_msg} > {reason_code} > {url}",
                )
                return
            r_data = self.parse(url, r_parse)
            for unique_id, v in r_data.items():
                data.setdefault(unique_id, {})
                data[unique_id] = v.copy()

        try:
            task_list = []
            for target_name in target_list:
                cast_url = self.getCastURL(target_name)
                for t in self.weather[W_FCST_D].copy().keys():
                    if isinstance(t, str):
                        dt = datetime.fromisoformat(t).replace(tzinfo=ZONE)
                        if dt < now and now - dt >= timedelta(days=1):
                            self.weather[W_FCST_D].pop(t)
                for t in self.weather[W_FCST_H].copy().keys():
                    if isinstance(t, str):
                        dt = datetime.fromisoformat(t).replace(tzinfo=ZONE)
                        if dt < now and now - dt >= timedelta(hours=1):
                            self.weather[W_FCST_H].pop(t)
                for url in cast_url:
                    task_list.append(self.hass.async_create_task(getDataFromUrl(url)))
                for t in task_list:
                    await t
                if len(data) > 0:
                    self.last_data.setdefault(target_name, {})
                    self.last_data[target_name].update(data)
            if DEBUG:
                self.pretty_print(data)
        except Exception as ex:
            self.log(3, f"Error at get_target > [{target}] > {ex}")
        return data

    async def get_kma(self):
        """Get KMA data."""
        return await self.get_target("KMA", [CAST_R, CAST_F, CAST_V, CAST_MT, CAST_ML])

    async def get_airkorea(self):
        """Get AirKorea data."""
        return await self.get_target("AIR", [CAST_A])

    async def update(self, event):
        """Update data from KMA and AirKorea."""
        if time.time() - self._last_error > 10 * 60:
            try:
                air = await self.get_airkorea()
                kma = await self.get_kma()
                self.result.update(merge_dicts(kma, air))
            except Exception as ex:
                self.log(3, f"Error at update > {ex}")
                self._last_error = time.time()
                return
        else:
            return

        for cast_target, update_time_list in self.last_update.items():
            name = CAST.get(cast_target, cast_target)
            name_en = CAST_EN.get(cast_target, cast_target)
            unique_id = f"dw{self.count}_{name_en}_updatetime"
            update_time = None
            update_time_attr = {CAST_CODE: name, CAST_TYPE: "업데이트"}
            update_time_name = f"담다날씨 {self.location} {name}"
            if (
                isinstance(update_time_list, list) and len(update_time_list) == 3
            ):  # [r_code, r_msg, url]
                update_time = update_time_list[1]
                update_time_attr["error_code"] = update_time_list[0]
                update_time_attr["error_url"] = update_time_list[2]
            else:
                try:
                    # 2022년 6월 10일 10:00:00
                    update_time = datetime.fromisoformat(update_time_list).replace(
                        tzinfo=ZONE
                    )
                except Exception:
                    update_time_attr["error"] = update_time_list
            self.result[unique_id] = self.make_entity(
                update_time_attr,
                "mdi:clock-outline",
                SensorDeviceClass.TIMESTAMP,
                SENSOR_DOMAIN,
                update_time,
                # datetime.fromisoformat(update_time).replace(tzinfo=ZONE),
                None,
                unique_id,
                unique_id,
                update_time_name,
            )

        if len(self.result) == 0:
            self.result = self.get_data("weather_data", self.result)
        if len(self.result) == 0:
            self.result = self.get_data("weather_data", self.result)
            return

        state_weather = {
            W_COND: convKMAcondition(self.weather),
            W_FCST_D: [],
            W_FCST_H: [],
        }
        for k, v in self.weather.items():
            if k in W_LIST:
                state_weather[k] = v
            if k in [W_FCST_H, W_FCST_D]:
                for dt, ft in v.items():
                    if len(ft) > 0:
                        ft.update({W_DT: dt, W_COND: convKMAcondition(ft)})
                        ft.update({W_PCP: ft.get(W_PCP, 0) + ft.get("snow", 0)})
                        state_weather[k].append(ft)
        if len(state_weather[W_FCST_D]) > 0:
            state_weather[W_FCST_D] = sorted(
                state_weather[W_FCST_D], key=lambda dt: dt[W_DT]
            )
        if len(state_weather[W_FCST_H]) > 0:
            state_weather[W_FCST_H] = sorted(
                state_weather[W_FCST_H], key=lambda dt: dt[W_DT]
            )

        attr_weather = {CAST_TYPE: "초단기실황"}
        unique_weather = f"damda_weather{self.count}"
        name_weather = f"담다날씨 {self.location}"
        self.result[unique_weather] = self.make_entity(
            attr_weather,
            None,
            None,
            WEATHER_DOMAIN,
            state_weather,
            None,
            unique_weather,
            unique_weather,
            name_weather,
        )

        # unique_weather2 = f"damda_weather{self.count}"
        # name_weather2 = f"담다날씨 {self.location}"
        # self.result[unique_weather2] = self.make_entity(
        #     attr_weather,
        #     None,
        #     None,
        #     WEATHER_DOMAIN,
        #     state_weather_daily,
        #     None,
        #     unique_weather2,
        #     unique_weather2,
        #     name_weather2,
        # )

        attr_apt = {CAST_TYPE: "초단기실황"}
        unique_apt = f"dw{self.count}_realtime_apparent_temperature"
        name_apt = f"{self.location} 체감온도"
        if isinstance(self.temperature, dict) and isinstance(self.wind_speed, dict):
            now_t = self.temperature[DEVICE_STATE]
            now_ws = self.wind_speed[DEVICE_STATE]
            value_apt = calc_windchill(now_t, now_ws)
            self.result[unique_apt] = self.make_entity(
                attr_apt,
                self.temperature[DEVICE_ICON],
                self.temperature[DEVICE_CLASS],
                self.temperature[DEVICE_DOMAIN],
                value_apt,
                self.temperature[DEVICE_UNIT],
                unique_apt,
                unique_apt,
                name_apt,
            )

        attr_hi = {CAST_TYPE: "초단기실황"}
        unique_hi = f"dw{self.count}_realtime_heat_index"
        name_hi = f"{self.location} 열지수"
        if isinstance(self.temperature, dict) and isinstance(self.humidity, dict):
            now_t = self.temperature[DEVICE_STATE]
            now_h = self.humidity[DEVICE_STATE]
            value_hi = calc_heatindex(now_t, now_h)
            self.result[unique_hi] = self.make_entity(
                attr_hi,
                self.temperature[DEVICE_ICON],
                self.temperature[DEVICE_CLASS],
                self.temperature[DEVICE_DOMAIN],
                value_hi,
                self.temperature[DEVICE_UNIT],
                unique_hi,
                unique_hi,
                name_hi,
            )

        self.result = self.set_data("weather_data", self.result)
        for unique_id, entity in self.result.items():
            target_domain = entity.get(DEVICE_DOMAIN)
            if not target_domain:
                self.log(0, f"Device domain does not exist > {unique_id} > {entity}")
                continue
            self.init_device(unique_id, target_domain, entity)
            self.update_entity(unique_id, entity)
