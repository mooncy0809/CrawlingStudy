import MySQLdb
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
chrome_options.add_argument('--headless') # [ --headless ]: WebDriver를 Browser 없이 실행하는 옵션.
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

def crawler(cate,sub_cate,category_code1,category_code2):
    market_name = '11번가'
    crawling_date = datetime.today().strftime("%Y-%m-%d")
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    elements = soup.select('#bestPrdList > div > ul > li')
    results = []
    for el in elements:
        temp_dict = dict()
        ranking = el.find('span', attrs={"class": "best"}).text
        category_code1 = category_code1
        category_code2 = category_code2
        cate = cate
        sub_cate = sub_cate
        name = el.find('div', attrs={"class": "pname"}).find('p').text
        name = name.replace('"', '')
        image = el.find('div', attrs={"class": "img_plot"}).find('img')['src']
        try:
            rate = el.find('span', attrs={"class": "sale"}).text.strip('%\n')
        except:
            rate = 0  # 할인하지 않는 상품

        try:
            if rate != 0:
                sales_price = el.find('strong', attrs={"class": "sale_price"}).text.strip('원')
                sales_price = int(sales_price.replace(',', ''))
            else:
                sales_price = el.find('span', attrs={"class": "price_detail"}).find('s').text.strip('원')
                sales_price = int(sales_price.replace(',', ''))
        except:
            sales_price = 0  # 무료상품

        try:
            discount_price = el.find('strong', attrs={"class": "sale_price"}).text.strip('원')
            discount_price = int(discount_price.replace(',', ''))
        except:
            discount_price = 0  # 무료상품

        real_path = el.find('div').find('a')['href']
        temp_dict['crawling_date'] = crawling_date
        temp_dict['ranking'] = ranking
        temp_dict['category_code1'] = category_code1
        temp_dict['category_code2'] = category_code2
        temp_dict['category_name1'] = cate
        temp_dict['category_name2'] = sub_cate
        temp_dict['product_name'] = name
        temp_dict['sales_price'] = sales_price
        temp_dict['discount_price'] = discount_price
        temp_dict['discount_rate'] = rate
        temp_dict['image_name'] = category_code1 + '_' + category_code2 + '_' + ranking + '.jpg'
        temp_dict['image_path'] = image
        temp_dict['real_path'] = real_path

        print(temp_dict)
        cursor.execute(f"INSERT INTO test_best_product_11st(crawling_date,ranking,category_code1,category_code2, category_name1, category_name2, product_name, sales_price, discount_price, discount_rate, image_name, image_path, real_path,insert_userid, insert_time) VALUES(\"{temp_dict['crawling_date']}\",\"{temp_dict['ranking']}\",\"{temp_dict['category_code1']}\",\"{temp_dict['category_code2']}\",\"{temp_dict['category_name1']}\",\"{temp_dict['category_name2']}\",\"{temp_dict['product_name']}\",\"{temp_dict['sales_price']}\",\"{temp_dict['discount_price']}\",\"{temp_dict['discount_rate']}\",\"{temp_dict['image_name']}\",\"{temp_dict['image_path']}\",\"{temp_dict['real_path']}\",\"{'admin'}\",NOW())")
        conn.commit()
    # pprint(results)
    return results

def execute():
    category_lists = driver.find_elements(By.XPATH, "//div[@class='best_category_box']/ul/li/button")
    all_result = []
    for button_index in range(len(category_lists)):
        category = driver.find_element_by_xpath('//*[@id="metaCtgrLi' + str(button_index) + '"]/button') # 카테고리 find
        if button_index < 10:
            category_code1 = '0'+str(button_index)
        else:
            category_code1 = str(button_index)
        category_code2 = '00'
        cate = category.text
        sub_cate = "전체"
        category.click() # 카테고리 클릭하여 페이지 이동
        time.sleep(1)
        scroll_down_to_end()
        result_list = crawler(cate,sub_cate,category_code1,category_code2)
        all_result.extend(result_list)
        scroll_up_to_category()
        if button_index == 0:
            pass
        else:
            sub_category_lists = driver.find_elements_by_xpath('//*[@id="metaCtgrLi' + str(button_index) + '"]/div/ul/li/a')
            for a_index in range(1,len(sub_category_lists)+1):
                if a_index < 10:
                    category_code2 = '0' + str(a_index)
                else:
                    category_code2 = str(a_index)
                sub_category = driver.find_element_by_xpath('//*[@id="metaCtgrLi' + str(button_index) + '"]/div/ul/li['+str(a_index)+']/a') # 서브 카테고리
                sub_cate = sub_category.text
                sub_category.click() # 서브 카테고리 클릭하여 페이지 이동
                time.sleep(1)
                scroll_down_to_end()
                result_list = crawler(cate,sub_cate,category_code1,category_code2)
                all_result.extend(result_list)
                scroll_up_to_category()

    return all_result

conn = MySQLdb.connect(
    user="kiesrnd",
    passwd="kiesrnd!@#",
    host="192.168.116.173",
    port=3307,
    db="TEST"
)

cursor = conn.cursor()
cursor.execute("DELETE FROM test_best_product_11st")
execute()
conn.commit()
conn.close()