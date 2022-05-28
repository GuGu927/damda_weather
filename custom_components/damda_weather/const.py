"""Constants for the Damda Weather integration."""
import math
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    # LENGTH_METERS,
    TEMP_CELSIUS,
    SPEED_METERS_PER_SECOND,
    PERCENTAGE,
    LENGTH_CENTIMETERS,
    LENGTH_MILLIMETERS,
    CONCENTRATION_PARTS_PER_MILLION,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)


VERSION = "1.4.2"
BRAND = "Damda"
NAME = "Damda Weather"
NAME_KOR = "담다날씨"
DOMAIN = "damda_weather"
MODEL = "damda_weather"
MANUFACTURER = "data.go.kr"
API_NAME = "dw_api"
PLATFORMS = [SENSOR_DOMAIN, WEATHER_DOMAIN]

DEVICE_DOMAIN = "domain"
DEVICE_ENTITY = "entity"
DEVICE_UPDATE = "update"
DEVICE_REG = "register"
DEVICE_TRY = "try"
DEFAULT_AVAILABLE = "available"

DEVICE_ICON = "icon"
DEVICE_CLASS = "device_class"
DEVICE_UNIT = "unit_of_measurement"
DEVICE_ATTR = "attributes"
DEVICE_STATE = "state"
DEVICE_UNIQUE = "unique_id"
DEVICE_ID = "entity_id"
DEVICE_NAME = "entity_name"

CONF_API = "api_key"
CONF_X = "grid_x"
CONF_Y = "grid_y"
CONF_S = "air_station"
CONF_R = "reg_id"


ITEM_X = "nx"
ITEM_Y = "ny"
ITEM_CATEGORY = "category"
ITEM_OVALUE = "obsrValue"
ITEM_FVALUE = "fcstValue"
ITEM_BTIME = "baseTime"
ITEM_BDATE = "baseDate"
ITEM_FTIME = "fcstTime"
ITEM_FDATE = "fcstDate"

CAST_TYPE = "type"
CAST_CODE = "code"
CAST_DTIME = "date_time"
CAST_BDATE = "base_date"
CAST_BTIME = "base_time"
CAST_FDATE = "cast_date"
CAST_FTIME = "cast_time"
CAST_VALUE = "cast_value"

W_DT = "datetime"
W_COND = "condition"
W_TEMP = "temperature"
W_HUMI = "humidity"
W_FCST = "forecast"
W_FCST_H = "forecast_hourly"
W_FCST_D = "forecast_daily"
W_O3 = "o3_value"
W_WS = "wind_speed"
W_WD = "wind_bearing"
W_SKY = "sky"
W_PCP = "precipitation"
W_PTY = "precipitation_type"
W_POP = "precipitation_probability"
W_LIST = [W_COND, W_HUMI, W_TEMP, W_O3, W_WD, W_WS, W_FCST, W_PCP, W_PTY, W_POP, W_SKY]

KMA_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/{}?serviceKey={}&nx={}&ny={}&base_date={}&base_time={}&numOfRows=1000&pageNo=1&dataType=json"
KMA_MID_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/{}?serviceKey={}&regId={}&tmFc={}{}&numOfRows=1000&pageNo=1&dataType=json"
AIRKOREA_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName={}&dataTerm=daily&pageNo=1&numOfRows=100&returnType=json&serviceKey={}&ver=1.0"
CAST_R = "getUltraSrtNcst"
CAST_F = "getUltraSrtFcst"
CAST_V = "getVilageFcst"
CAST_A = "getMsrstnAcctoRltmMesureDnsty"
CAST_ML = "getMidLandFcst"
CAST_MT = "getMidTa"
CAST = {
    CAST_R: "초단기실황",
    CAST_F: "초단기예보",
    CAST_V: "단기예보",
    CAST_A: "대기오염정보",
    CAST_ML: "중기예보",
    CAST_MT: "중기예보",
}
CAST_EN = {
    CAST_R: "realtime",
    CAST_F: "forecast",
    CAST_V: "village",
    CAST_A: "airkorea",
    CAST_ML: "midterm",
    CAST_MT: "midterm",
}

CONDITION_MAP = {
    "맑음": "sunny",
    "구름많음": "partlycloudy",
    "흐림": "cloudy",
    "비": "rainy",
    "비/눈": "snowy-rainy",
    "눈": "snowy",
    "소나기": "pouring",
    "빗방울": "rainy",
    "빗방울눈날림": "snowy-rainy",
    "눈날림": "snowy",
    "구름많고 비": "rainy",
    "구름많고 눈": "snowy",
    "구름많고 비/눈": "snowy-rainy",
    "구름많고 소나기": "pouring",
    "흐리고 비": "rainy",
    "흐리고 눈": "snowy",
    "흐리고 비/눈": "snowy-rainy",
    "흐리고 소나기": "pouring",
}

CODE_SKY = {"1": "맑음", "3": "구름많음", "4": "흐림"}
CODE_SKY_REV = {value: key for key, value in CODE_SKY.items()}
ICON_SKY = {
    "1": "mdi:weather-sunny",
    "3": "mdi:weather-partly-cloudy",
    "4": "mdi:weather-cloudy",
}
ICON_SKY_MID = {
    "맑음": "mdi:weather-sunny",
    "구름많음": "mdi:weather-cloudy",
    "구름많고 비": "mdi:weather-rainy",
    "구름많고 눈": "mdi:weather-snowy",
    "구름많고 비/눈": "mdi:weather-snowy-rainy",
    "구름많고 소나기": "mdi:weather-pouring",
    "흐리고": "mdi:weather-partly-cloudy",
    "흐리고 비": "mdi:weather-rainy",
    "흐리고 눈": "mdi:weather-snowy",
    "흐리고 비/눈": "mdi:weather-snowy-rainy",
    "흐리고 소나기": "mdi:weather-pouring",
}
ICON_SKY_MID_VALUE = {
    "맑음": 1,
    "구름많음": 2,
    "구름많고 비": 3,
    "구름많고 눈": 4,
    "구름많고 비/눈": 5,
    "구름많고 소나기": 6,
    "흐리고": 2.5,
    "흐리고 비": 3.5,
    "흐리고 눈": 4.5,
    "흐리고 비/눈": 5.5,
    "흐리고 소나기": 6.5,
}
CODE_PTY = {
    "0": "없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "4": "소나기",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림",
}
CODE_PTY_REV = {value: key for key, value in CODE_PTY.items()}
ICON_PTY = {
    "0": "mdi:close-circle",
    "1": "mdi:weather-rainy",
    "2": "mdi:weather-snowy-rainy",
    "3": "mdi:weather-snowy",
    "4": "mdi:weather-pouring",
    "5": "mdi:weather-partly-rainy",
    "6": "mdi:weather-partly-snowy-rainy",
    "7": "mdi:weather-partly-snowy",
}
WIND_DIR = [
    "북",
    "북북동",
    "북동",
    "동북동",
    "동",
    "동남동",
    "남동",
    "남남동",
    "남",
    "남남서",
    "남서",
    "서남서",
    "서",
    "서북서",
    "북서",
    "북북서",
    "북",
]
GRADE_VALUE = {"1": "좋음", "2": "보통", "3": "나쁨", "4": "매우나쁨"}
GRADE_ICON = {
    "1": "mdi:numeric-1-box",
    "2": "mdi:numeric-2-box",
    "3": "mdi:numeric-3-box",
    "4": "mdi:numeric-4-box",
}


def conv_wind(deg):
    """Convert wind degree to 16."""
    pos = math.floor((int(deg) + 22.5 * 0.5) / 22.5)
    try:
        return WIND_DIR[pos], ""
    except Exception:
        return deg, ""


def icon_rainfall(value):
    """Return icon of rainfall value.

    1mm < value : mdi:xxx

    1mm < value : mdi:xxx

    1mm < value : mdi:xxx

    """
    if value == "30~50mm":
        return "mdi:weather-rainy"
    elif value in ["50mm 이상", "50mm이상"]:
        return "mdi:weather-pouring"
    elif str(value) in ["없음", "강수없음", "0.0", "0", "1mm 미만", "1mm미만"]:
        return "mdi:close-circle"
    else:
        return "mdi:weather-partly-rainy"


def icon_snowfall(value):
    """Return icon of snowfall value.

    1mm < value : mdi:xxx

    1mm < value : mdi:xxx

    1mm < value : mdi:xxx

    """
    if value in ["5 cm 이상", "5cm이상"]:
        return "mdi:weather-snowy-heavy"
    elif str(value) in ["없음", "적설없음", "0.0", "0", "1 cm 미만", "1cm미만"]:
        return "mdi:close-circle"
    else:
        return "mdi:weather-partly-snowy"


taMin = [
    "최저기온",
    TEMP_CELSIUS,
    SENSOR_DOMAIN,
    "mdi:thermometer-chevron-down",
    SensorDeviceClass.TEMPERATURE,
]
taMax = [
    "최고기온",
    TEMP_CELSIUS,
    SENSOR_DOMAIN,
    "mdi:thermometer-chevron-up",
    SensorDeviceClass.TEMPERATURE,
]
rnSt = [
    "강수확률",
    PERCENTAGE,
    SENSOR_DOMAIN,
    "mdi:water-percent",
    SensorDeviceClass.HUMIDITY,
]
wf = ["하늘상태", None, SENSOR_DOMAIN, ICON_SKY_MID, None]
CATEGORY_CODE = {
    "POP": [
        "precipitation_probability",
        "강수확률",
        PERCENTAGE,
        SENSOR_DOMAIN,
        "mdi:water-percent",
        SensorDeviceClass.HUMIDITY,
    ],
    "PTY": [
        "precipitation_type",
        "강수형태",
        CODE_PTY,
        SENSOR_DOMAIN,
        ICON_PTY,
        None,
    ],
    "PCP": [
        "precipitation",
        "강수량",
        LENGTH_MILLIMETERS,
        SENSOR_DOMAIN,
        icon_rainfall,
        None,
    ],
    "REH": [
        "humidity",
        "습도",
        PERCENTAGE,
        SENSOR_DOMAIN,
        "mdi:water-percent",
        SensorDeviceClass.HUMIDITY,
    ],
    "SNO": ["snow", "적설", LENGTH_CENTIMETERS, SENSOR_DOMAIN, icon_snowfall, None],
    "SKY": ["sky", "하늘상태", CODE_SKY, SENSOR_DOMAIN, ICON_SKY, None],
    "TMP": [
        "temperature",
        "기온",
        TEMP_CELSIUS,
        SENSOR_DOMAIN,
        "mdi:thermometer",
        SensorDeviceClass.TEMPERATURE,
    ],
    "TMN": [
        "temperature_min",
        "최저기온",
        TEMP_CELSIUS,
        SENSOR_DOMAIN,
        "mdi:thermometer-chevron-down",
        SensorDeviceClass.TEMPERATURE,
    ],
    "TMX": [
        "temperature_max",
        "최고기온",
        TEMP_CELSIUS,
        SENSOR_DOMAIN,
        "mdi:thermometer-chevron-up",
        SensorDeviceClass.TEMPERATURE,
    ],
    # "UUU": ["wind_ew", "풍속(동서)", SPEED_METERS_PER_SECOND],
    # "VVV": ["wind_sn", "풍속(남북)", SPEED_METERS_PER_SECOND],
    # "WAV": ["wave", "파고", LENGTH_METERS, SENSOR_DOMAIN, "mdi:waves", None],
    "VEC": ["wind_bearing", "풍향", conv_wind, SENSOR_DOMAIN, "mdi:weather-windy", None],
    "WSD": [
        "wind_speed",
        "풍속",
        SPEED_METERS_PER_SECOND,
        SENSOR_DOMAIN,
        "mdi:weather-windy",
        None,
    ],
    "T1H": [
        "temperature",
        "기온",
        TEMP_CELSIUS,
        SENSOR_DOMAIN,
        "mdi:thermometer",
        SensorDeviceClass.TEMPERATURE,
    ],
    "RN1": [
        "precipitation",
        "강수량",
        LENGTH_MILLIMETERS,
        SENSOR_DOMAIN,
        icon_rainfall,
        None,
    ],
    # "LGT": ["lighting", "낙뢰", "KA/㎢", SENSOR_DOMAIN, "mdi:weather-lightning", ""],
    "taMin3": ["temperature_min_3"] + taMin,
    "taMax3": ["temperature_max_3"] + taMax,
    "taMin4": ["temperature_min_4"] + taMin,
    "taMax4": ["temperature_max_4"] + taMax,
    "taMin5": ["temperature_min_5"] + taMin,
    "taMax5": ["temperature_max_5"] + taMax,
    "taMin6": ["temperature_min_6"] + taMin,
    "taMax6": ["temperature_max_6"] + taMax,
    "taMin7": ["temperature_min_7"] + taMin,
    "taMax7": ["temperature_max_7"] + taMax,
    "rnSt3Am": ["precipitation_probability_3_am"] + rnSt,
    "rnSt3Pm": ["precipitation_probability_3_pm"] + rnSt,
    "rnSt4Am": ["precipitation_probability_4_am"] + rnSt,
    "rnSt4Pm": ["precipitation_probability_4_pm"] + rnSt,
    "rnSt5Am": ["precipitation_probability_5_am"] + rnSt,
    "rnSt5Pm": ["precipitation_probability_5_pm"] + rnSt,
    "rnSt6Am": ["precipitation_probability_6_am"] + rnSt,
    "rnSt6Pm": ["precipitation_probability_6_pm"] + rnSt,
    "rnSt7Am": ["precipitation_probability_7_am"] + rnSt,
    "rnSt7Pm": ["precipitation_probability_7_pm"] + rnSt,
    "wf3Am": ["sky_3_am"] + wf,
    "wf3Pm": ["sky_3_pm"] + wf,
    "wf4Am": ["sky_4_am"] + wf,
    "wf4Pm": ["sky_4_pm"] + wf,
    "wf5Am": ["sky_5_am"] + wf,
    "wf5Pm": ["sky_5_pm"] + wf,
    "wf6Am": ["sky_6_am"] + wf,
    "wf6Pm": ["sky_6_pm"] + wf,
    "wf7Am": ["sky_7_am"] + wf,
    "wf7Pm": ["sky_7_pm"] + wf,
}


AIRKOREA_ITEM = {
    "so2Value": [
        "so2_value",
        "아황산가스 농도",
        CONCENTRATION_PARTS_PER_MILLION,
        SENSOR_DOMAIN,
        "mdi:alpha-s-circle",
        None,
    ],
    "coValue": [
        "co_value",
        "일산화탄소 농도",
        CONCENTRATION_PARTS_PER_MILLION,
        SENSOR_DOMAIN,
        "mdi:molecule-co",
        SensorDeviceClass.CO,
    ],
    "o3Value": [
        "o3_value",
        "오존 농도",
        CONCENTRATION_PARTS_PER_MILLION,
        SENSOR_DOMAIN,
        "mdi:alpha-o-circle",
        SensorDeviceClass.OZONE,
    ],
    "no2Value": [
        "no2_value",
        "이산화질소 농도",
        CONCENTRATION_PARTS_PER_MILLION,
        SENSOR_DOMAIN,
        "mdi:alpha-n-circle",
        SensorDeviceClass.NITROGEN_DIOXIDE,
    ],
    "pm10Value": [
        "pm10_value",
        "미세먼지 농도",
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        SENSOR_DOMAIN,
        "mdi:blur",
        SensorDeviceClass.PM10,
    ],
    "pm25Value": [
        "pm25_value",
        "초미세먼지 농도",
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        SENSOR_DOMAIN,
        "mdi:blur",
        SensorDeviceClass.PM25,
    ],
    "khaiValue": ["khai_value", "통합대기환경수치", None, SENSOR_DOMAIN, "mdi:earth", None],
    "so2Grade": ["so2_grade", "아황산가스 지수", GRADE_VALUE, SENSOR_DOMAIN, GRADE_ICON, None],
    "coGrade": ["co_grade", "일산화탄소 지수", GRADE_VALUE, SENSOR_DOMAIN, GRADE_ICON, None],
    "o3Grade": ["o3_grade", "오존 지수", GRADE_VALUE, SENSOR_DOMAIN, GRADE_ICON, None],
    "no2Grade": ["no2_grade", "이산화질소 지수", GRADE_VALUE, SENSOR_DOMAIN, GRADE_ICON, None],
    "pm10Grade": [
        "pm10_grade",
        "미세먼지 지수",
        GRADE_VALUE,
        SENSOR_DOMAIN,
        GRADE_ICON,
        None,
    ],
    "pm25Grade": [
        "pm25_grade",
        "초미세먼지 지수",
        GRADE_VALUE,
        SENSOR_DOMAIN,
        GRADE_ICON,
        None,
    ],
    "khaiGrade": [
        "khai_grade",
        "통합대기환경지수",
        GRADE_VALUE,
        SENSOR_DOMAIN,
        GRADE_ICON,
        None,
    ],
}


ERROR_CODE = {
    "01": "어플리케이션 에러",
    "02": "데이터베이스 에러",
    "03": "데이터없음 에러",
    "04": "HTTP 에러",
    "05": "서비스 연결실패 에러",
    "10": "잘못된 요청 파라메터 에러",
    "11": "필수요청 파라메터가 없음",
    "12": "해당 오픈 API서비스가 없거나 폐기됨",
    "20": "서비스 접근거부",
    "21": "일시적으로 사용할 수 없는 서비스키",
    "22": "서비스 요청제한횟수 초과 에러",
    "30": "등록되지 않은 서비스키",
    "31": "기한만료된 서비스키",
    "32": "등록되지 않은 IP",
    "33": "서명되지 않은 호출",
    "34": "등록되지 않은 호출",
    "99": "기타 에러",
}


def int_between(min_int, max_int):
    """Return an integer between 'min_int' and 'max_int'."""
    return vol.All(vol.Coerce(int), vol.Range(min=min_int, max=max_int))


def float_between(min_float, max_float):
    """Return an float between 'min_float' and 'max_float'."""
    return vol.All(vol.Coerce(float), vol.Range(min=min_float, max=max_float))


OPT_MONITORING = "monitoring"
OPTION_MONITOR = [(OPT_MONITORING, False, cv.boolean)]
OPTION_DEFAULT = [
    (CONF_API, "API key from data.go.kr", cv.string),
    (CONF_S, "Air station name.", cv.string),
    (CONF_X, "KMA grid X", cv.positive_int),
    (CONF_Y, "KMA grid Y", cv.positive_int),
    (CONF_R, "", cv.string),
]
OPTION_LIST = OPTION_DEFAULT + OPTION_MONITOR
