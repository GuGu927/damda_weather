# 담다 날씨
Damda Weather Component


![HACS][hacs-shield]
![Version v1.4][version-shield]


문의 : 네이버 [HomeAssistant카페](https://cafe.naver.com/koreassistant)

## 담다 날씨가 도움이 되셨나요?

<a href="https://qr.kakaopay.com/281006011000098177846177" target="_blank"><img src="https://github.com/GuGu927/DAM-Pad/blob/main/images/kakao.png" alt="KaKao"></a>

카카오페이 : https://qr.kakaopay.com/281006011000098177846177

<a href="https://paypal.me/rangee927" target="_blank"><img src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_150x38.png" alt="PayPal"></a>

<a href="https://www.buymeacoffee.com/rangee" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee"></a>


## 버전 기록정보

| 버전   | 날짜         | 내용      |
|------|------------|---------|
| v1.0.0 | 2021.10.xx | 게시 |

<br/>


## 준비물

- HomeAssistant `최신버전`(**2021.9.0 이상**)
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

- `담다 자료실`게시판에서 `custom_components` 파일을 다운로드, 내부의 `damda_weather` 폴더 확인
- HomeAssistant 설정폴더인 `/config` 내부에 `custom_components` 폴더를 생성(이미 있으면 다음 단계)<br/>설정폴더는 `configuration.yaml` 파일이 있는 폴더를 의미합니다.<br>
- `/config/custom_components`에 위에서 다운받은 `damda_weather` 폴더를 넣기<br>
- HomeAssistant 재시작

<br/>

## 담다날씨를 설치하기 전 선행과정

### 공공데이터포털 회원가입 및 API키 발급받기

- [공공데이터포털](https://www.data.go.kr/) 에서 회원가입
- API 활용신청하기
-- [기상청_단기예보 조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084) 활용신청
-- [한국환경공단_에어코리아_대기오염정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15073861) 활용신청
- encoded API키 확인
-- API키는 1회원 당 1개로 같은 API키로 여러개의 서비스를 호출 가능합니다.

### 기상청 정보를 찾기 위한 X,Y 격자좌표 찾기

- 기상청 단기예보 조회서비스 페이지에서 참고문서 `기상청41_단기예보 조회서비스_오픈API활용가이드_최종.zip` 를 다운로드
- 다운로드 받은 파일의 압축을 풀면 `기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20210401).xlsx` 파일을 열기
- 본인의 위치를 찾고 X,Y 격자좌표 기억하기

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
- X value, Y value 에는 첨부된 엑셀파일에서 본인의 위치를 검색



[version-shield]: https://img.shields.io/badge/version-v1.0.0-orange.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
