from gensim.summarization.summarizer import summarize
from konlpy.tag import Okt
# 한글 텍스트
text = """경기도 버스 노사가 임금협상과 준공영제 도입 시기 등을 놓고 최종 조정에 나선 결과 합의에 도달했습니다.

경기도 내 52개 버스 업체 노조가 소속된 경기도버스노동조합협의회는 어제(25일) 오후 4시부터 경기지방노동위원회에서 7시간 넘게 진행된 사측과의 조정회의 끝에 합의에 이르렀다고 밝혔습니다.

이에 따라 노조가 예고했던 파업은 철회됐고, 오늘(26일) 경기 지역 버스는 정상 운행됩니다.

노사 합의서에는 준공영제와 민영제 노선 운수종사자의 임금을 각각 4%와 4.5% 인상하는 안이 담겼습니다.

합의서에 따르면, 준공영제 적용을 받는 33개 버스회사 조합원은 월 소정 근로일수 내 22일을 초과해 일한 경우엔 임금조견표에 의한 1일 임금을 추가로 지급받습니다.

또 내년 1월 1일부터 2층 버스 운행 조합원에게는 근무일당 만 원의 추가 수당이 지급됩니다.

민영제 적용을 받는 25개 버스회사 조합원의 임금 인상률은 정비직조합원과 근로시간 면제자에게도 적용되며, 내년에 운행을 시작하는 공공관리제 노선에서도 별도의 임금협정서를 체결하기 전까지는 경기도 공공버스가 적용받는 임금협정서를 적용합니다.

협상장을 방문한 김동연 경기도지사는 노사 합의서 조인식에서 "도민의 발인 버스가 오늘(26일)도 정상 운행하게 돼 대단히 기쁘게 생각한다"며 "2027년까지 시내버스 전 노선을 공공관리제로 전환하는 것에 대해 양해 말씀을 드리면서 차질 없이 노사 양측의 의견을 들어 추진할 것을 약속한다"고 밝혔습니다.

합의서에 서명한 이기천 경기도버스노동조합협의회 위원장은 "경기도 버스는 정말 열악한 상태이고, 저임금·장시간 근로에 많이 시달리고 있다"며, 김 지사를 향해 "필요한 부분은 제도적으로 개선하고 많은 투자를 해주시리라 믿고 있다"고 말했습니다.

김기성 경기도버스운송사업조합 이사장은 "지사님과 도 직원들이 3일 밤낮을 함께 하며 협상이 원만히 되도록 지원해주셔서 감사하다"며 "준공영제를 훌륭히 완수할 수 있도록 지원 부탁드린다"고 전했습니다."""

# KoNLPy를 사용하여 명사만 추출

# Gensim을 사용하여 요약
summary = summarize(text, ratio=0.5)  # 20%의 요약 비율
print(summary)