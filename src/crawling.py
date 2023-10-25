from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def get_weather(text):
    current_time = datetime.now().strftime('%m월%d일 %H시%M분 ')

    browser = webdriver.Chrome()
    browser.get(f'https://search.naver.com/search.naver?query={text}')
    city = browser.find_element(By.CLASS_NAME, 'title').text
    if '내일' in text:
        datas = browser.find_element(By.CLASS_NAME, 'weather_info_list')
        result = []
        for data in datas.find_elements(By.CLASS_NAME, 'inner'):
            result.append(data.text.replace('\n', ' ').split())
        return '내일 ' + city + '의 날씨입니다. ' +  ' '.join(result[0]) + '입니다.' + ' '.join(result[1]) + '입니다.'
    else:
        temperature = browser.find_element(By.CLASS_NAME, 'weather_graphic').text
        rest_data = browser.find_element(By.CLASS_NAME, 'summary_list').text

        temperature = temperature.replace('\n', ' ').split()[1:]
        return current_time + city + '의 날씨입니다.' + ' '.join(temperature) + '이고 ' + rest_data + '입니다.'