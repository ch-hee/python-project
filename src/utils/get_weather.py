import requests
from datetime import datetime, timedelta
from googletrans import Translator
import os 

def translate_to_ko(input_text):
    translator = Translator()
    return translator.translate(input_text, dest='ko').text

def translate_to_en(input_text):
    translator = Translator()
    return translator.translate(input_text, dest='en').text

def parse_user_input(user_input):
    # 사용자 입력에서 도시 추출
    words = user_input.split()
    city_index = -1

    # "날씨"라는 키워드 다음에 오는 도시를 추출
    if "날씨" in words:
        city_index = words.index("날씨") - 1

    if city_index != -1 and city_index < len(words):
        return words[city_index]

    return None

def get_weather(api_key, city, is_today=True):
    # is_today = True -> 오늘 else 내일
    if is_today:
        target_date = datetime.utcnow()
    else:
        target_date = datetime.utcnow() + timedelta(days=1)

    # OpenWeatherMap API 엔드포인트
    api_endpoint = "http://api.openweathermap.org/data/2.5/forecast"

    # 파라미터 설정
    params = {
        'q': city,
        'appid': api_key,
    }

    # API 요청 보내기
    response = requests.get(api_endpoint, params=params)

    # 응답 처리
    if response.status_code == 200:
        weather_data = response.json()

        # 가장 가까운 시간대 찾기
        closest_time = min(weather_data['list'], key=lambda x: abs(target_date - datetime.utcfromtimestamp(x['dt'])))
        
        # 온도를 켈빈에서 섭씨로 변환
        temperature_celsius = closest_time['main']['temp'] - 273.15

        # 날씨 정보 출력
        translated_city = translate_to_ko(city)
        translated_weather = translate_to_ko(closest_time['weather'][0]['description'])
        return_text = f"{target_date.strftime('%m월 %d일')} {translated_city}의 날씨 정보입니다. 날씨는 {translated_weather}, 온도는 {temperature_celsius:.2f}도, 습도: {closest_time['main']['humidity']}% 입니다.  더 필요한게 있으신가요?"
        return return_text
    else:
        return "도시를 찾을 수 없습니다. 다시 한번 말씀해 주세요."

if __name__ == "__main__":
    api_key = os.environ.get("WEATHER_API_KEY")
    print(get_weather(api_key, 'suwon'))