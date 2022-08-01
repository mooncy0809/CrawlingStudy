from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Chrome WebDriver의 옵션을 설정하는 모듈 Import
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint

url = 'http://corners.gmarket.co.kr/Bestsellers'
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

# def scroll_down_to_end():
#     check_body_height = 0
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #맨끝까지
#         time.sleep(0.5)
#         body_height = driver.execute_script("return document.body.clientHeight;")
#         # 스크롤이 사이트 마지막에 다다르면 while -> break
#         if check_body_height == body_height:
#             break
#         check_body_height = body_height
#         time.sleep(0.5)
#
# def scroll_up_to_category():
#     driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

def crawler(cate, sub_cate):
    market_name = 'G마켓'
    crawling_date = datetime.today().strftime("%Y-%m-%d")
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    elements = soup.select('#gBestWrap > div > div:nth-child(5) > div > ul > li')
    results = []
    for el in elements:
        temp_dict = dict()
        cate = cate
        sub_cate = sub_cate
        ranking = el.find('p').text
        name = el.find('a', attrs={"class": "itemname"}).text
        image = el.find('img', attrs={"class": "lazy"})['data-original']
        try:
            sales_price = el.find('div', attrs={"class": "s-price"}).find('strong').find('span').find('span').text.strip('원')
            sales_price = int(sales_price.replace(',', ''))
        except:
            sales_price = 0 # 무료상품

        try:
            rate = el.find('span', attrs={"class": "sale"}).find('em').text.strip('%')
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
    category_list = driver.find_elements_by_xpath("//*[@id='gBestWrap']/div/div[2]/ul/li/a")
    all_result = []
    print(len(category_list))
    for category_index in range(1,len(category_list)+1):
        category = driver.find_element_by_xpath('//*[@id="categoryTabG"]/li['+str(category_index)+']/a')
        cate = category.text
        sub_cate = '전체'
        category.click()
        result_list = crawler(cate,sub_cate)
        # print(f"resulst_list : {result_list}") # 카테고리별 리스트
        all_result.extend(result_list)
        if category_index == 1:
            pass
        else:
            sub_category_lists = driver.find_elements_by_xpath('//*[@class="cate-l"]/div/ul/li/a')
            for sub_category_index in range(1,len(sub_category_lists)+1):
                if sub_category_index==1:
                    sub_category = driver.find_element_by_xpath('//*[@class="cate-l"]/div/ul/li[' + str(sub_category_index) + ']/a')
                    sub_cate = sub_category.text
                    sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
                    result_list = crawler(cate, sub_cate)
                    all_result.extend(result_list)
                else:
                    open_list = driver.find_element_by_xpath('//*[@id="subGroupListLink"]')
                    open_list.click()
                    sub_category = driver.find_element_by_xpath('//*[@id="subGroupList"]/div/ul/li['+ str(sub_category_index) +']/a')
                    sub_cate = sub_category.text
                    sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
                    result_list = crawler(cate, sub_cate)
                    all_result.extend(result_list)

            # pprint(f"resulst_list : {result_list}")  # 카테고리별 리스트
    return all_result

all_results = execute()
pprint(f"all_results : {all_results}")
