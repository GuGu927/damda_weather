# 담다 날씨

Damda Weather Component

![HACS][hacs-shield]
![Version v1.4][version-shield]

문의 : 네이버 [HomeAssistant카페](https://cafe.naver.com/koreassistant)

## 담다 날씨가 도움이 되셨나요?

<a href="https://qr.kakaopay.com/281006011000098177846177" target="_blank"><img src="https://github.com/GuGu927/damda_pad/blob/main/images/kakao.png" alt="KaKao"></a>

카카오페이 : https://qr.kakaopay.com/281006011000098177846177

<a href="https://paypal.me/rangee927" target="_blank"><img src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_150x38.png" alt="PayPal"></a>

## 버전 기록정보

| 버전   | 날짜       | 내용                                                                                                                                    |
| ------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| v1.0.0 | 2021.10.07 | 게시                                                                                                                                    |
| v1.1.0 | 2021.10.08 | 일/시간별 weather 로 분리                                                                                                               |
| v1.1.1 | 2021.10.09 | weather 풍속 단위에 대응(m/s에서 km/h로 적용)                                                                                           |
| v1.2.0 | 2021.10.10 | 풍속 반올림 표기<br>오늘 최저/최고기온 추가                                                                                             |
| v1.2.1 | 2021.10.10 | weather 일별 강수확률,강수량,날씨상태 수정<br>weather 최저/최고기온 관련 오류 수정                                                      |
| v1.2.2 | 2021.10.10 | weather 시간별 표시항목 수정                                                                                                            |
| v1.2.3 | 2021.10.11 | weather 시간별, 일별 강수량 수정                                                                                                        |
| v1.2.4 | 2021.10.15 | 업데이트시간 센서의 device class 지정<br>센서 표시단위 수정<br>재부팅 후 값 표시되게끔 개선<br>기타 버그 수정                           |
| v1.2.5 | 2021.11.11 | 업데이트 시도 관련 버그 수정<br> 재부팅 후 값 표기관련 버그 수정<br>API변경에 따른 대응<br>기타 버그 수정                               |
| v1.2.6 | 2021.12.05 | HA시작 속도에 영향을 주지 않도록 수정<br>중기예보 추가`(설정법은 아래를 참고하세요.)`<br>옵션:업데이트 시간 기록 추가<br>기타 버그 수정 |
| v1.2.7 | 2021.12.06 | 업데이트 시간 구성요소의 entity_id, unqiue_id 변경(sensor.xxx_xxx`_updatetime`)                                                         |
| v1.3.0 | 2021.12.06 | api호출 방식 변경 및 부분 변경                                                                                                          |
| v1.3.2 | 2021.12.08 | 서울, 인천, 경기도, 제주도 중기예보 오류 수정 및 단기예보 업데이트시간 관련 오류 수정                                                   |
| v1.3.3 | 2021.12.11 | 히스토리 그래프 관련 수정                                                                                                               |
| v1.3.4 | 2021.12.12 | 중기예보 아이콘 오류 수정<br>2021.12 버전 업데이트 대응                                                                                 |
| v1.3.5 | 2021.12.15 | 2021.12 버전 업데이트 대응2                                                                                                             |
| v1.3.6 | 2021.12.18 | 적설량 관련 오류 수정                                                                                                                   |
| v1.3.7 | 2021.12.23 | 통계그래프 가능하게끔 수정                                                                                                              |
| v1.3.8 | 2022.01.04 | 체감온도 계산식 변경<br>오류 수정                                                                                                       |
| v1.3.9 | 2022.03.07 | 2022.3 업데이트 대응(sensor 의 datetime/time deprecated 관련)                                                                           |
| v1.4.0 | 2022.03.23 | sensor 오류 수정                                                                                                                        |
| v1.4.1 | 2022.05.12 | 업데이트 오류 시 멈추는 현상 수정                                                                                                       |
| v1.4.2 | 2022.05.28 | SO2 추가                                                                                                                                |
| v1.4.3 | 2022.06.08 | 오류 수정                                                                                                                               |
| v1.4.4 | 2022.06.09 | 오류 수정                                                                                                                               |
| v1.4.5 | 2022.06.11 | interval 및 오류 수정                                                                                                                   |
| v1.4.6 | 2022.06.22 | 아이콘 표시 오류 수정                                                                                                                   |
| v1.4.7 | 2022.09.05 | 강수량 표기 오류 수정                                                                                                                   |
| v1.4.8 | 2022.11.06 | datetime 오류 수정                                                                                                                      |
| v1.4.9 | 2022.11.09 | native 관련 대응                                                                                                                        |
| v1.5.0 | 2022.12.02 | 오픈API 오류 대비를 위한 임시방편 적용                                                                                                  |
| v1.5.1 | 2023.04.11 | deprecated 대응                                                                                                                         |
| v1.5.2 | 2024.01.11 | deprecated 대응                                                                                                                         |
| v1.5.3 | 2025.01.04 | deprecated 대응                                                                                                                         |
| v1.5.4 | 2025.03.06 | 적설량 단위 대응                                                                                                                        |

<br/>

## 준비물

- HomeAssistant `최신버전`(**2021.12.0 이상**)
- HomeAssistant OS, Core, Container 등 아무런 상관이 없습니다.

<br/>

## 사용자 구성요소를 HA에 설치하는 방법

### HACS

- HACS > Integrations > 우측상단 메뉴 > `Custom repositories` 선택
- `Add custom repository URL`에 `https://github.com/GuGu927/damda_weather` 입력
- Category는 `Integration` 선택 후 `ADD` 클릭
- HACS > Integrations 에서 `Damda Weather` 찾아서 설치
- HomeAssistant 재시작

<br/>

### 수동설치

- `https://github.com/GuGu927/damda_waether` 페이지에서 `Code/Download ZIP` 을 눌러 파일을 다운로드, 내부의 `damda_weather` 폴더 확인
- HomeAssistant 설정폴더인 `/config` 내부에 `custom_components` 폴더를 생성(이미 있으면 다음 단계)<br/>설정폴더는 `configuration.yaml` 파일이 있는 폴더를 의미합니다.<br>
- `/config/custom_components`에 위에서 다운받은 `damda_weather` 폴더를 넣기<br>
- HomeAssistant 재시작

<br/>

## 담다날씨를 설치하기 전 선행과정

### 공공데이터포털 회원가입 및 API키 발급받기

- [공공데이터포털](https://www.data.go.kr/) 에서 회원가입
- API 활용신청하기
- [기상청\_단기예보 조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084) 활용신청
- [기상청\_중기예보 조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15059468) 활용신청
- [한국환경공단*에어코리아*대기오염정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15073861) 활용신청
- API키 확인(API키는 1회원 당 1개로 같은 API키로 여러개의 서비스를 호출 가능합니다.)

### 기상청 단기예보를 불러오기 위한 X,Y 격자좌표 찾기

- 기상청 단기예보 조회서비스 페이지에서 참고문서 `기상청41_단기예보 조회서비스_오픈API활용가이드_최종.zip` 를 다운로드
- 다운로드 받은 파일의 압축을 풀고 `기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20210401).xlsx` 파일을 열기
- 본인의 위치를 찾고 X,Y 격자좌표 기억하기

### 기상청 중기예보를 불러오기 위한 예보지점 코드 찾기

- 기상청 단기예보 조회서비스 페이지에서 참고문서 `기상청20_중기예보 조회서비스_오픈API활용가이드.zip` 를 다운로드
- 다운로드 받은 파일의 압축을 풀고 `기상청20_중기예보 조회서비스_오픈API활용가이드_지점코드.xlsx` 파일을 열기
- 본인의 위치를 찾고 코드 기억하기

### 에어코리아에서 대기오염정보 측정소명 찾기

- [에어코리아](https://www.airkorea.or.kr/web/stationInfo?pMENU_NO=93) 에서 측정소명을 검색
- 측정소명이 "강남구 측정소" 일 경우 "강남구"를 기억하기

<br/>

## 담다날씨를 통합구성요소로 설치하는 방법

### 통합구성요소

- HomeAssistant 사이드패널 > 설정 > 통합 구성요소 > 통합 구성요소 추가<br>
- 검색창에서 `담다 날씨` 입력 후 선택<br>
- Weather name 에는 보여지는 구성요소의 이름을 입력. ex)우리집<br>
- API key에는 공공데이터포털에서 발급받은 API 키를 입력.
- Station name에는 에어코리에서 찾은 측정소명을 입력.
- X value, Y value 에는 첨부된 엑셀파일`(기상청41_단기예보.xlsx)`에서 본인의 위치를 검색하여 입력.
- 중기예보 지역코드 에는 첨부된 엑셀파일`(기상청20_중기예보.xlsx)`에서 본인의 위치를 검색하여 입력.
- 중기예보를 원하지 않을 경우 공백으로 놔두면 됩니다.

<br/>

## 담다날씨를 lovelace에 추가하는 예제

### weather_card를 수정한 weather_gu 를 사용

![manual_sidebar](https://github.com/GuGu927/damda_weather/blob/main/images/weather_gu.png)

- [WeatherGu](https://cafe.naver.com/koreassistant/6611) 러브레이스 카드를 다운로드 및 설치해야합니다.

```yaml
type: custom:vertical-stack-in-card
cards:
  - type: custom:weather-gu
    entity: weather.damda_weather1_hourly
    current: true
    details: true
    hourly_forecast: true
    forecast: true
    number_of_forecasts: "8"
  - type: custom:weather-gu
    entity: weather.damda_weather1
    hourly_forecast: false
    forecast: true
    details: false
    current: false
    number_of_forecasts: "8"
```

[version-shield]: https://img.shields.io/badge/version-v1.5.3-orange.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
