import requests
from bs4 import BeautifulSoup

def scrape_top_news_from_page(url):
    try:
        url = 'https://news.naver.com/main/ranking/popularDay.naver'
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(url, headers = headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        top_news_list = []

        for media_block in soup.select('.rankingnews_box')[:3]:
            media_name_element = media_block.select_one('.rankingnews_name')
            if media_name_element:
                media_name = media_name_element.get_text(strip=True)
                news_list = []

                for news_item in media_block.select('li a')[:5]:
                    news_title = news_item.get_text(strip=True)
                    news_link = news_item['href']

                    news_content = get_article_content(news_link, headers)
                    news_list.append({'title': news_title, 'link': news_link, 'content': news_content})

                top_news_list.append({'press': media_name, 'news': news_list})
        return top_news_list
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

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
            return content
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
            print(f"\n언론사: {item['press']}")
            for idx, news in enumerate(item['news'], start=1):
                print(f"\n기사 {idx}: {news['title']}")
                print(f"링크: {news['link']}")
                print(f"내용:\n{news['content'][:300]}...")  # 기사 내용 중 일부만 출력
    else:
        print("뉴스를 가져올 수 없습니다.")
