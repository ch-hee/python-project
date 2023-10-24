import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print('듣고 있어요')
    audio = r.listen(source) #마이크로부터 음성 듣기

try:
    # 구글 API로 인식(하루 50회)
    # 영어
    # text = r.recognize_google(audio, language='en-us')
    # print(text)

    # 한국어
    text = r.recognize_google(audio, language='ko')
    print(text)

except sr.UnknownValueError:
    print('인식 실패')
except sr.RequestError as e:
    print(f'요청 실패 : {e}')
