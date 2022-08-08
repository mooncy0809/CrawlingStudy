from selenium import webdriver
from datetime import datetime
import time
import urllib.request
import ssl
import pysftp
import os

class Common:
    img_url_list = []
    img_name_list = []
    def __init__(self):
        self.webdriver = None

    def set_url(self,url):
        self.url = url


    def get_url(self):
        print(self.url)
        return self.url

    def set_driver(self,driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    def make_driver(self):
        driver_options = webdriver.ChromeOptions()
        # driver_options.add_argument('--headless')  # [ --headless ]: WebDriver를 Browser 없이 실행하는 옵션.
        driver_options.add_argument('--log-level=3')  # Chroem Browser의 로그 레벨을 낮추는 옵션.
        driver_options.add_argument('--disable-logging')  # 로그를 남기지 않는 옵션.
        driver_options.add_argument('--no-sandbox')  # 샌드박스 사용 안함.
        driver_options.add_argument('--disable-gpu')  # gpu 에러 방지 옵션
        driver_options.add_argument("--start-maximized")
        chrome_driver = webdriver.Chrome('chromedriver', options=driver_options)
        chrome_driver.implicitly_wait(10)
        chrome_driver.get(self.get_url())
        chrome_driver.switch_to.window(chrome_driver.window_handles[0])
        self.set_driver(chrome_driver)
        return chrome_driver

    def dictionary(self, ranking, category_code1, category_code2, cate, sub_cate, name, sales_price, discount_price, image, rate, real_path):
        crawling_date = datetime.today().strftime("%Y-%m-%d")
        temp_dict = dict()
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

        return temp_dict

    def scroll_down_to_end(self):
        driver = self.get_driver()
        check_body_height = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 맨끝까지
            time.sleep(1)
            body_height = driver.execute_script("return document.body.clientHeight;")
            # 스크롤이 사이트 마지막에 다다르면 while -> break
            if check_body_height == body_height:
                break
            check_body_height = body_height
            time.sleep(1)

    def scroll_up_to_category(self):
        driver = self.get_driver()
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

    def img_download(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        for i in range(len(self.img_url_list)):
            urllib.request.urlretrieve(self.img_url_list[i], "/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling4/gmarket/data/images_bk/" + self.img_name_list[i])

    def transfer_image_to_ftp_server(self):
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

