import time, os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from src.utils.get_weather import *
from src.utils.news_crawling import *
from src.utils.translator import *
import base64
import threading
import queue
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

def get_messages():
    global messages
    return messages

def working(input_text):
    global temp_flag
    global audio_buffer
    global messages

    answer_text = ''
    api_key = os.environ.get('WEATHER_API_KEY')

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
        speak('잠시만 기다려 주세요.')
        city = parse_user_input(input_text)
        translated_city = translate_to_en(city)
        if '내일' in input_text:
            is_today = False
        else:
            is_today = True
        speak(get_weather(api_key, translated_city, is_today))
    elif '뉴스' in input_text:
        url = 'https://news.naver.com/main/ranking/popularDay.naver'
        speak('네, 잠시만 기다려 주세요')
        print(scrape_top_news_from_page(url))
        speak('뉴스 정보를 요약해서 슬랙에 보냈습니다.')
    elif '번역' in input_text:
        speak('번역할 수 있는 언어는 영어, 중국어, 일본어가 있어요. 어느 언어로 번역해 드릴까요?')
        temp_flag = True
        text = transcribe_streaming()
        if '영'in text:
            speak('번역하실 문장을 말씀해 주세요.')
            translate_text = transcribe_streaming()
            translated_text = translate(translate_text, 'en')
            speak('번역한 문장이에요.' + translated_text)
        elif '중국' in text:
            speak('번역하실 문장을 말씀해 주세요.')
            translate_text = transcribe_streaming()
            translated_text = translate(translate_text, 'zh-cn')
            speak('번역한 문장이에요.' + translated_text)
        elif '일본' in text:
            speak('번역하실 문장을 말씀해 주세요.')
            translate_text = transcribe_streaming()
            translated_text = translate(translate_text, 'ja')
            speak('번역한 문장이에요.' + translated_text)
        else:
            speak('죄송해요 번역을 종료하겠습니다.')
        temp_flag = False
    elif '종료' in input_text:
        answer_text = '네 종료하겠습니다.'
        speak(answer_text)
    else:
        answer_text = '죄송해요. 이해하지 못했어요. 다시 한번 말씀해 주시겠어요?'
        speak(answer_text)

def speak(text):
    global messages

    messages.append('[Haru] : ' + text)
    file_name = 'voice.mp3'
    tts_ko = gTTS(text, lang='ko')
    tts_ko.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)
    
def listen_microphone():
    global end_of_stream_event
    global audio_buffer
    global temp_flag
    global messages

    stream = p.open(format=stream_config,
                    channels=channels,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    messages.append("[Haru] : 듣고있어요")

    try:
        while not end_of_stream_event.is_set():
            data = stream.read(CHUNK)
            audio_buffer.put(data)
    except KeyboardInterrupt:
        messages.append("Stopping the stream...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def transcribe_streaming():
    global messages

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="ko-KR", 
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=False,
    )

    requests = (speech.StreamingRecognizeRequest(audio_content=base64.b64encode(data).decode("utf-8"))
                for data in iter(audio_buffer.get, None))

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )
    
    for response in responses:
        for result in response.results:
            text = result.alternatives[0].transcript
            messages.append("[me]: {}".format(text))
            if temp_flag:
                return text
            else:
                if '종료' in text:
                    end_of_stream_event.set()
                    speak('네 종료하겠습니다.')
                    return
                else:
                    working(text)


google_application_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if not google_application_credentials:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

client = speech.SpeechClient.from_service_account_file(google_application_credentials)

RATE = 16000  # Sample rate
CHUNK = 1024  # Buffer size

client = speech.SpeechClient()

p = pyaudio.PyAudio()

stream_config = pyaudio.paInt16  # 16-bit PCM format
channels = 1  # Mono audio stream

# Buffer to store audio chunks
audio_buffer = queue.Queue()

# storage for message
messages = []

# Event to signal the end of streaming
end_of_stream_event = threading.Event()

# flag
temp_flag = False

if __name__ == "__main__":
    try:
        # Thread 시작
        mic_thread = threading.Thread(target=listen_microphone)
        mic_thread.start()

        transcribe_streaming()

    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print('stop')
    finally:
        end_of_stream_event.set()
        mic_thread.join()

        print("Exiting...")