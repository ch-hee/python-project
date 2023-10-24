from gtts import gTTS
from googletrans import Translator
# import playsound

user_input = input('번역할 텍스트를 입력하세요 : ')
selected_lang = input('어떤 언어로 번역을 해드릴까요? ex) en, la, ja : ')
translator = Translator()
translated_sentence = translator.translate(user_input, dest=selected_lang).text

text = translated_sentence
tts = gTTS(text, lang='ko')
tts.save('./output.mp3')


# playsound.playsound('./output.mp3')

