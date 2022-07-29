from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Chrome WebDriver의 옵션을 설정하는 모듈 Import
from datetime import datetime
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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #맨끝까지
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
    elements = driver.find_elements_by_xpath('//*[@id="bestPrdList"]/div/ul/li')
    results =[]
    for el in elements:
        temp_dict = dict()
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
        print(temp_dict)

    return results

def execute():
    category_lists = driver.find_elements(By.XPATH, "//div[@class='best_category_box']/ul/li/button")
    all_result = []
    for button_index in range(len(category_lists)):
        category = driver.find_element_by_xpath('//*[@id="metaCtgrLi' + str(button_index) + '"]/button')
        cate = category.text
        sub_cate = "전체"
        category.click()
        scroll_down_to_end()
        result_list = crawler(cate,sub_cate)
        all_result.extend(result_list)
        scroll_up_to_category()
        if button_index == 0:
            pass
        else:
            sub_category_lists = driver.find_elements_by_xpath('//*[@id="metaCtgrLi' + str(button_index) + '"]/div/ul/li/a')
            for a_index in range(1,len(sub_category_lists)):
                sub_category = driver.find_element_by_xpath('//*[@id="metaCtgrLi' + str(button_index) + '"]/div/ul/li['+str(a_index)+']/a')
                sub_cate = sub_category.text
                sub_category.click()
                time.sleep(1)
                scroll_down_to_end()
                result_list = crawler(cate,sub_cate)
                all_result.extend(result_list)
                scroll_up_to_category()

        # print(f"resulst_list : {result_list}") # 카테고리별 리스트

    return all_result

all_results = execute()
# pprint(f"all_results : {all_results}")
