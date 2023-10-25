from textrankr import TextRank
from konlpy.tag import Komoran

# 예시 한글 텍스트
text = """
자연어 처리 (Natural Language Processing, NLP)는 인공 지능의 한 분야로, 기계가 인간의 언어를 이해하고 처리하는 데 관련된 기술입니다.
NLP는 텍스트에서 의미를 추출하고, 문장의 구조를 이해하며, 언어의 의미를 해석하는 등의 작업을 수행합니다.
"""

# Komoran을 사용하여 토크나이징
komoran = Komoran()
tr = TextRank(tokenizer=komoran.morphs)
keywords = tr.summarize(text)

print(keywords)