from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Chrome WebDriver의 옵션을 설정하는 모듈 Import
from datetime import datetime
from bs4 import BeautifulSoup
from pprint import pprint
import time

from selenium.webdriver.common.by import By

url = 'https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain'
driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
# chrome_options.add_argument('--headless') # [ --headless ]: WebDriver를 Browser 없이 실행하는 옵션.
chrome_options.add_argument( '--log-level=3' ) # Chroem Browser의 로그 레벨을 낮추는 옵션.
chrome_options.add_argument( '--disable-logging' ) # 로그를 남기지 않는 옵션.
chrome_options.add_argument( '--no-sandbox' ) #샌드박스 사용 안함.
chrome_options.add_argument( '--disable-gpu' ) #gpu 에러 방지 옵션
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome( executable_path=driver_path, chrome_options=chrome_options )
driver.get(url)

def scroll_down_to_end():
    check_body_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 맨끝까지
        time.sleep(1)
        body_height = driver.execute_script("return document.body.clientHeight;")
        # 스크롤이 사이트 마지막에 다다르면 while -> break
        if check_body_height == body_height:
            break
        check_body_height = body_height
        time.sleep(1)

def scroll_up_to_category():
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

def crawler(cate,sub_cate):
    market_name = '11번가'
    crawling_date = datetime.today().strftime("%Y-%m-%d")
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    elements = soup.select('#bestPrdList > div > ul > li')
    results = []
    for el in elements:
        temp_dict = dict()
        cate = cate
        sub_cate = sub_cate
        ranking = el.find('span', attrs={"class": "best"}).text
        name = el.find('div', attrs={"class": "pname"}).find('p').text
        image = el.find('div', attrs={"class": "img_plot"}).find('img')['src']
        try:
            sales_price = el.find('strong', attrs={"class": "sale_price"}).text
            sales_price = int(sales_price.replace(',', ''))
        except:
            sales_price = 0 # 무료상품

        try:
            rate = el.find('span', attrs={"class": "sale"}).text.strip('%')
            rate = float(rate)
        except:
            rate = 0 # 할인하지 않는 상품
        temp_dict['crawling_date'] = crawling_date
        temp_dict['market_name'] = market_name
        temp_dict['category_name'] = cate
        temp_dict['sub_category_name'] = sub_cate
        temp_dict['ranking'] = ranking
        temp_dict['product_name'] = name
        temp_dict['sales_price'] = sales_price
        temp_dict['image_path'] = image
        temp_dict['sales_rate'] = '%.2f' % rate
        results.append(temp_dict.copy())

    pprint(results)
    return results

def execute():
    all_result = []
    category_lists = driver.find_elements(By.XPATH, "//div[@class='best_category_box']/ul/li/button")
    for category in category_lists:
        category_index = category_lists.index(category)
        cate = category.text
        sub_cate = "전체"
        driver.execute_script("arguments[0].click();", category) # 카테고리 클릭하여 페이지 이동
        time.sleep(2)
        scroll_down_to_end()
        result_list = crawler(cate,sub_cate)
        all_result.extend(result_list)
        scroll_up_to_category()
        if category_index == 0:
            pass
        else:
            sub_category_lists = driver.find_elements_by_xpath('//*[@id="metaCtgrLi' + str(category_index) + '"]/div/ul/li/a')
            for sub_category in sub_category_lists:
                sub_cate = sub_category.text
                driver.execute_script("arguments[0].click();", sub_category) # 서브 카테고리 클릭하여 페이지 이동
                scroll_down_to_end()
                result_list = crawler(cate,sub_cate)
                all_result.extend(result_list)
                scroll_up_to_category()
        # pprint(f"resulst_list : {result_list}")  # 카테고리별 리스트
    return all_result

all_results = execute()
pprint(f"all_results : {all_results}")
