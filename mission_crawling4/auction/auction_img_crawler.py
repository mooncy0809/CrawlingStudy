from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Chrome WebDriver의 옵션을 설정하는 모듈 Import
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import time
import MySQLdb
import urllib.request
import ssl
import pysftp
import os

url = 'http://corners.auction.co.kr/corner/categorybest.aspx'
driver_path = '/usr/local/bin/chromedriver'
img_url_list = []
img_name_list = []

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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #맨끝까지
        time.sleep(0.5)
        body_height = driver.execute_script("return document.body.clientHeight;")
        # 스크롤이 사이트 마지막에 다다르면 while -> break
        if check_body_height == body_height:
            break
        check_body_height = body_height
        time.sleep(0.5)

def scroll_up_to_category():
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

def crawler(cate, sub_cate, category_code1, category_code2):
    market_name = '옥션'
    crawling_date = datetime.today().strftime("%Y-%m-%d")
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    elements1 = soup.select('#itembest_T > ul.uxb-img')
    results = []

    for element in elements1:
        elements2 = element.select('li')
        for el in elements2:
            try:
                temp_dict = dict()
                ranking = el.find('div','rank').text
                category_code1 = category_code1
                category_code2 = category_code2
                cate = cate
                sub_cate = sub_cate
                name = el.find('div', attrs={"class": "info"}).find('em').find('a').text
                image = el.find('div', attrs={"class": "img"}).find('a').find('img')['src']
                img_url_list.append('https:' + image)
                img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
                try:
                    rate = el.find('span',attrs={"class": "down"}).text.strip('%')
                except:
                    rate = 0  # 할인하지 않는 상품

                try:
                    if rate != 0:
                        sales_price = el.find('li', attrs={"class": "c_price"}).find('strike').find('span').text.strip('원')
                        sales_price = int(sales_price.replace(',', ''))
                    else:
                        sales_price = el.find('li', attrs={"class": "d_price"}).find('span').find('span').text.strip('원')
                        sales_price = int(sales_price.replace(',', ''))
                except:
                    sales_price = 0  # 무료상품

                try:
                    discount_price = el.find('li', attrs={"class": "d_price"}).find('span').find('span').text.strip('원')
                    discount_price = int(discount_price.replace(',', ''))
                except:
                    discount_price = 0  # 무료상품

                real_path = el.find('div', attrs={"class": "img"}).find('a')['href']

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
                temp_dict['image_path'] = 'https:' + image
                temp_dict['real_path'] = real_path

                print(temp_dict)

                # cursor.execute(f"INSERT INTO test_best_product_auction(crawling_date,ranking,category_code1,category_code2, category_name1, category_name2, product_name, sales_price, discount_price, discount_rate, image_name, image_path, real_path,insert_userid, insert_time) \
                #         VALUES(\"{temp_dict['crawling_date']}\",\"{temp_dict['ranking']}\",\"{temp_dict['category_code1']}\",\"{temp_dict['category_code2']}\",\"{temp_dict['category_name1']}\",\"{temp_dict['category_name2']}\",\
                #         \"{temp_dict['product_name']}\",\"{temp_dict['sales_price']}\",\"{temp_dict['discount_price']}\",\"{temp_dict['discount_rate']}\",\"{temp_dict['image_name']}\",\"{temp_dict['image_path']}\",\"{temp_dict['real_path']}\",\"{'admin'}\",NOW())")
            except:
                pass

    return results

def execute():
    category_list = driver.find_elements_by_xpath("//*[@id='contents']/div[1]/div[2]/ul/li/a")
    all_result = []
    for category_index in range(1,len(category_list)+1):
        category = driver.find_element_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li['+str(category_index)+']/a')
        if category_index <= 10:
            category_code1 = '0'+str(category_index-1)
        else:
            category_code1 = str(category_index - 1)
        category_code2 = '00'
        cate = category.find_element_by_xpath(('img'))
        cate = cate.get_attribute('alt')
        sub_cate = '전체'
        category.click()
        result_list = crawler(cate, sub_cate, category_code1, category_code2)
        all_result.extend(result_list)
        if category_index == 1:
            pass
        else:
            sub_category_lists = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/div['+str(category_index)+']/ul/li')
            for sub_category_index in range(1,len(sub_category_lists)+1):
                category = driver.find_element_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[' + str(category_index) + ']/a')
                ActionChains(driver).click_and_hold(category).perform() # 하위 카테고리가 hover일때만 나오므로 카테고리 클릭 후 홀드
                if sub_category_index < 10:
                    category_code2 = '0' + str(sub_category_index)
                else:
                    category_code2 = str(sub_category_index)
                sub_category = driver.find_element_by_xpath('//*[@id="contents"]/div[1]/div[2]/div['+str(category_index)+']/ul/li['+str(sub_category_index)+']/a')
                sub_cate = sub_category.text

                ActionChains(driver).move_to_element(sub_category).click().perform()
                result_list = crawler(cate, sub_cate, category_code1, category_code2)
                all_result.extend(result_list)

    return all_result

def img_download():
    ssl._create_default_https_context = ssl._create_unverified_context
    for i in range(len(img_url_list)):
        urllib.request.urlretrieve(img_url_list[i], "/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/auction/data/images/" + img_name_list[i])

def transfer_image_to_ftp_server():
    today = datetime.today()
    date = today.isoformat()[0:10]
    success_cnt = 0

    host = "192.168.116.220"
    username = "develop"
    password = "develop!2#"
    port = 22
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    local_path = '/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/auction/data/images/'
    remote_path = '/home/develop/test2/auction/'
    list = os.listdir('/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/auction/data/images/')

    try:
        with pysftp.Connection(host, port=port, username=username, password=password, cnopts=cnopts) as sftp:
            with sftp.cd(remote_path):
                if date in sftp.listdir():
                    sftp.cd(date)
                else:
                    sftp.mkdir(date)
                    sftp.cd(remote_path + date + "/")
            for file_name in list:
                sftp.put(local_path + file_name, remote_path + date + "/" + file_name)
                success_cnt += 1
    except:
        print(file_name)
    sftp.close()
    print(str(success_cnt) + ' 파일 전송 완료')

# conn = MySQLdb.connect(
#     user="kiesrnd",
#     passwd="kiesrnd!@#",
#     host="192.168.116.173",
#     port=3307,
#     db="TEST"
# )
#
# cursor = conn.cursor()
# # cursor.execute("DELETE FROM test_best_product_auction")

# execute()
# conn.commit()
# conn.close()

# print(img_url_list)
# print(img_name_list)
# img_download()

transfer_image_to_ftp_server()
list = os.listdir('/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/auction/data/images/')
print(len(list))
