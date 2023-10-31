from googletrans import Translator

def translate(input_text, lang):
    translator = Translator()
    translated_sentence = translator.translate(input_text, dest=lang).text
    return translated_sentence


if __name__ == "__main__":
    input_text = input('번역할 문장을 입력하세요 : ')
    selected_lang = input('어떤 언어로 번역을 해드릴까요? ex) en, la, ja : ')
    translated_sentence = translate(input_text, selected_lang)
    print(translated_sentence)