import time, os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from crawling import get_weather

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
    if '시리야' in input_text:
        answer_text = '네, 무엇을 도와드릴까요?'
        speak(answer_text)
    elif '날씨' in input_text:
        print('in')
        speak(get_weather(input_text))
        speak('더 필요한게 있으신가요?')

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