import time, os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

# 음성 인식 함수(STT)
def listen(reconizer, audio):
    pass

# 동작 함수
def working(input_text):
    pass

# 대답 함수(TTS)
def speak(text):
    print('[AI] : ' + text)
    file_name = 'voice.mp3'
    tts_ko = gTTS(text, lang='ko')
    tts_ko.save(file_name)
    playsound(file_name)


r = sr.Recognizer()
m = sr.Microphone()

speak('무엇을 도와드릴까요?')
stop_listening = r.listen_in_background(m, listen)
# stop_listening(wait_for_stop=False) # 더 이상 듣지 않음

while True:
    time.sleep(0.1)