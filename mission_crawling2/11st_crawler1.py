from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Chrome WebDriver의 옵션을 설정하는 모듈 Import
from datetime import timedelta
from datetime import datetime
import time

from selenium.webdriver.common.by import By

market_name = '11번가'
crawling_date = datetime.today().strftime("%Y-%m-%d")
url = 'https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain'
driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
# chrome_options.add_argument('--headless') # [ --headless ]: WebDriver를 Browser 없이 실행하는 옵션.
chrome_options.add_argument( '--log-level=3' ) # Chroem Browser의 로그 레벨을 낮추는 옵션.
chrome_options.add_argument( '--disable-logging' ) # 로그를 남기지 않는 옵션.
chrome_options.add_argument( '--no-sandbox' ) #샌드박스 사용 안함.
chrome_options.add_argument( '--disable-gpu' ) #gpu 에러 방지 옵션

driver = webdriver.Chrome( executable_path=driver_path, chrome_options=chrome_options )
driver.get(url)

def scroll_down_to_end():
    check_body_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        body_height = driver.execute_script("return document.body.clientHeight;")
        # 스크롤이 사이트 마지막에 다다르면 while -> break
        if check_body_height == body_height:
            break
        check_body_height = body_height
        time.sleep(0.5)

def scroll_up_to_category():
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

def crawler(cate):
    elements = driver.find_elements_by_xpath('//*[@id="bestPrdList"]/div/ul/li')
    for el in elements:
        ranking = el.find_element_by_xpath('div/a/span')
        ranking = ranking.text
        name = el.find_element_by_xpath('div/a/div[2]/p')
        name = name.text
        image = el.find_element_by_xpath('div/a/div[1]/img')
        image = image.get_attribute('src')
        sales_price = el.find_element_by_xpath('div/a/div[2]/div[1]/span/strong')
        sales_price = sales_price.text
        sales_price = int(sales_price.replace(',', ''))
        cate = cate

        try:
            rate = el.find_element_by_xpath('div/a/div[2]/div[1]/span[1]')
            rate = rate.text.strip('%')
            rate = float(rate)
        except:
            rate = 0
        temp_dict = {
            "crawling_date": crawling_date,
            "market_name": market_name,
            "category_name": cate,
            'ranking': ranking,
            'product_name': name,
            'sales_price': sales_price,
            'image_path': image,
            'sales_rate': '%.2f' % rate
        }
        print(temp_dict)

def execute():
    elements = driver.find_elements_by_xpath('//*[@id="layBody"]/div[1]/ul/li/button')
    for i in range(len(elements)):
        element = driver.find_element_by_xpath('//*[@id="metaCtgrLi'+str(i)+'"]/button')
        cate = element.text
        element.click()
        scroll_down_to_end()
        crawler(cate)
        scroll_up_to_category()


execute()
