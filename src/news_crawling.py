import requests
from bs4 import BeautifulSoup
from gensim.summarization.summarizer import summarize
import requests
import json

def send_news_to_slack(top_news_list):
    slack_hooks_url = 'https://hooks.slack.com/services/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'
    headers = {'Content-type': 'application/json'}
    
    for news_list in top_news_list:
        attachments = []
        for news in news_list['news']:
            attachment = {
                'color': '#36a64f',  # 적절한 색상 지정
                'title': news['title'],
                'title_link': news['link'],
                'text': news['content']
            }
            attachments.append(attachment)

        payload = {
            'attachments': attachments,
            'text': f'*{news_list["media"]}*에서 주요 뉴스',
        }

        data = json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8')
        response = requests.post(slack_hooks_url, data=data, headers=headers)
        
        print(response.status_code)
        print('------------------- 전송 완료 -------------------')

def hello():
    slack_hooks_url = 'https://hooks.slack.com/services/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'
    message = '안녕하세요 오늘은 파이썬의 크롤링을 배웠습니다. 여기에 나중에 뉴스를 공유할 예정입니다.'
    response = requests.post(slack_hooks_url, data=json.dumps({'text' : message}), headers={'Content-Type' : 'application/json'})
    print(response.status_code)
def scrape_top_news_from_page(url):
    try:
        url = 'https://news.naver.com/main/ranking/popularDay.naver'
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(url, headers = headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        top_news_list = []

        for media_block in soup.select('.rankingnews_box')[:2]:
            media_name_element = media_block.select_one('.rankingnews_name')
            if media_name_element:
                media_name = media_name_element.get_text(strip=True)
                news_list = []

                for news_item in media_block.select('li .list_content a')[:5]:
                    news_title = news_item.get_text(strip=True)
                    news_link = news_item['href']

                    news_content = get_article_content(news_link, headers)
                    news_list.append({'title': news_title, 'link': news_link, 'content': news_content})

                top_news_list.append({'media': media_name, 'news': news_list})
        send_news_to_slack(top_news_list)
        # hello()
        return top_news_list
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_article_content(url, headers):
    try:
        response = requests.get(url, headers= {'User-Agent':'Mozilla/5.0'})
        response.raise_for_status()  # 에러 발생 시 예외 처리

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 기사 내용 가져오기
        article_body_element = soup.select_one('._article_content')
        if article_body_element:
            content = article_body_element.get_text('\n', strip=True)
            content_summary = summarize(content, ratio=0.3)
            return content_summary
        else:
            print(f"Error: Could not find article content on {article_url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # 주어진 페이지 URL
    given_page_url = 'https://news.naver.com/main/ranking/popularDay.naver'

    top_news_result = scrape_top_news_from_page(given_page_url)

    if top_news_result:
        for item in top_news_result:
            print(f"\n언론사: {item['media']}")
            for idx, news in enumerate(item['news'], start=1):
                print(f"\n제목 {idx}: {news['title']}")
                print(f"링크: {news['link']}")
                print(f"내용:\n{news['content'][:300]}...")  # 기사 내용 중 일부만 출력
                continue
    else:
        print("뉴스를 가져올 수 없습니다.")
