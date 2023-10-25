import time, os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from get_weather import parse_user_input, get_weather, translate_to_en
from schedule import Scheduler
from news_crawling import scrape_top_news_from_page

# 음성 인식 함수(STT)
def listen(reconizer, audio):
    try:
        text = reconizer.recognize_google(audio, language='ko')
        print('[me] ' + text)
        working(text)
    except sr.UnknownValueError:
        print('인식 실패')
    except sr.RequestError as e:
        print(f'요청 실패 : {e}')

# 동작 함수
def working(input_text):
    answer_text = ''
    api_key = "7f5acd97b26c88399f43eea58c1b37c9"

    if '하루' in input_text:
        answer_text = '네, 무엇을 도와드릴까요?'
        speak(answer_text)
    elif '안녕' in input_text:
        answer_text = '안녕하세요!, 무엇을 도와드릴까요?'
        speak(answer_text)
    elif '이름' in input_text:
        answer_text = '제 이름은 하루입니다.'
        speak(answer_text)
    elif '날씨' in input_text:
        city = parse_user_input(input_text)
        translated_city = translate_to_en(city)
        if '내일' in input_text:
            is_today = False
        else:
            is_today = True
        speak(get_weather(api_key, translated_city, is_today))
    elif '종료' in input_text:
        stop_listening(wait_for_stop=False)
        answer_text = '네 종료하겠습니다.'
        speak(answer_text)
    elif '뉴스' in input_text:
        url = 'https://news.naver.com/main/ranking/popularDay.naver'
        speak('네, 잠시만 기다려 주세요')
        print(scrape_top_news_from_page(url))
    else:
        answer_text = '죄송해요. 이해하지 못했어요. 다시 한번 말씀해 주시겠어요?'
        speak(answer_text)

# 대답 함수(TTS)
def speak(text):
    print('[AI] : ' + text)
    file_name = 'voice.mp3'
    tts_ko = gTTS(text, lang='ko')
    tts_ko.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)

r = sr.Recognizer()
m = sr.Microphone()

stop_listening = r.listen_in_background(m, listen)
# stop_listening(wait_for_stop=False) # 더 이상 듣지 않음

while True:
    time.sleep(0.1)