from summa import keywords

# 예시 텍스트
text = """
Natural language processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans using natural language. 
The ultimate objective of NLP is to enable computers to understand, interpret, and generate human language in a way that is both meaningful and valuable.
"""

# TextRank를 사용하여 키워드 추출
result = keywords.keywords(text)
print(result)
