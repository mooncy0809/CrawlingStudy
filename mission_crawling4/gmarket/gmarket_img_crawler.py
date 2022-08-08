from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Chrome WebDriver의 옵션을 설정하는 모듈 Import
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import ssl
import pysftp
import os

url = 'http://corners.gmarket.co.kr/Bestsellers'
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

def crawler(cate, sub_cate, category_code1 , category_code2):
    market_name = 'G마켓'
    crawling_date = datetime.today().strftime("%Y-%m-%d")
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    elements = soup.select('#gBestWrap > div > div:nth-child(5) > div > ul > li')
    results = []

    for el in elements:
        temp_dict = dict()
        ranking = el.find('p').text
        category_code1 = category_code1
        category_code2 = category_code2
        cate = cate
        sub_cate = sub_cate
        name = el.find('a', attrs={"class": "itemname"}).text
        image = el.find('img', attrs={"class": "lazy"})['src']
        img_url_list.append('https:'+image)
        img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
        try:
            rate = el.find('em').text.strip('%')
        except:
            rate = 0 # 할인하지 않는 상품

        try:
            if rate != 0:
                sales_price = el.find('div', attrs={"class": "o-price"}).find('span').find('span').text.strip('원')
                sales_price = int(sales_price.replace(',', ''))
            else:
                sales_price = el.find('div', attrs={"class": "s-price"}).find('strong').find('span').find('span').text.strip('원')
                sales_price = int(sales_price.replace(',', ''))


        except:
            sales_price = 0 # 무료상품

        try:
            discount_price = el.find('div', attrs={"class": "s-price"}).find('strong').find('span').find('span').text.strip('원')
            discount_price = int(discount_price.replace(',', ''))
        except:
            discount_price = 0 # 무료상품

        real_path = el.find('a')['href']

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
        # print(temp_dict)

        results.append(temp_dict.copy())

    return results

def execute():
    category_list = driver.find_elements_by_xpath("//*[@id='gBestWrap']/div/div[2]/ul/li/a")
    all_result = []
    for category_index in range(1,len(category_list)+1):
        category = driver.find_element_by_xpath('//*[@id="categoryTabG"]/li['+str(category_index)+']/a')
        if category_index <= 10:
            category_code1 = '0'+str(category_index-1)
        else:
            category_code1 = str(category_index - 1)
        category_code2 = '00'
        cate = category.text
        sub_cate = 'ALL'
        category.click()
        result_list = crawler(cate,sub_cate,category_code1,category_code2)
        all_result.extend(result_list)
        if category_index == 1:
            pass
        else:
            sub_category_lists = driver.find_elements_by_xpath('//*[@class="cate-l"]/div/ul/li/a')
            for sub_category_index in range(1,len(sub_category_lists)+1):
                if sub_category_index < 10:
                    category_code2 = '0' + str(sub_category_index)
                else:
                    category_code2 = str(sub_category_index)

                if sub_category_index == 1:
                    sub_category = driver.find_element_by_xpath('//*[@class="cate-l"]/div/ul/li[' + str(sub_category_index) + ']/a')
                    sub_cate = sub_category.text
                    sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
                    result_list = crawler(cate, sub_cate, category_code1, category_code2)
                    all_result.extend(result_list)
                else:
                    open_list = driver.find_element_by_xpath('//*[@id="subGroupListLink"]')
                    open_list.click()
                    sub_category = driver.find_element_by_xpath('//*[@id="subGroupList"]/div/ul/li['+ str(sub_category_index) +']/a')
                    sub_cate = sub_category.text
                    sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
                    result_list = crawler(cate, sub_cate, category_code1, category_code2)
                    all_result.extend(result_list)

    return all_result


def img_download():
    ssl._create_default_https_context = ssl._create_unverified_context
    for i in range(len(img_url_list)):
        urllib.request.urlretrieve(img_url_list[i], "/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/gmarket/data/images_bk/" + img_name_list[i])

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

    local_path = '/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/gmarket/data/images/'
    remote_path = '/home/develop/test2/gmarket/'
    list = os.listdir('/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/gmarket/data/images/')

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


# execute()

# print(img_url_list)
# print(img_name_list)
# img_download()

# transfer_image_to_ftp_server()
# list = os.listdir('/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/gmarket/data/images_bk/')
# print(len(list))