from main import Common
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import time


class Crawler(Common):
    def __init__(self):
        pass

    ########################### G마켓 ###########################
    def crawler_gmarket(self, cate, sub_cate, category_code1 , category_code2):
        driver = self.get_driver()
        market_name = 'G마켓'
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        elements = soup.select('#gBestWrap > div > div:nth-child(5) > div > ul > li')
        results = []

        for el in elements:
            ranking = el.find('p').text
            category_code1 = category_code1
            category_code2 = category_code2
            cate = cate
            sub_cate = sub_cate
            name = el.find('a', attrs={"class": "itemname"}).text
            image = el.find('img', attrs={"class": "lazy"})['src']
            self.img_url_list.append('https:'+image)
            self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
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

            print(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price, discount_price, image, rate, real_path))
            results.append(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price, discount_price, image, rate, real_path))


        return results

    def execute_gmarket(self):
        self.set_url('http://corners.gmarket.co.kr/Bestsellers')
        driver = self.make_driver()
        driver = self.get_driver()
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
            result_list = self.crawler_gmarket(cate,sub_cate,category_code1,category_code2)
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
                        result_list = self.crawler_gmarket(cate, sub_cate, category_code1, category_code2)
                        all_result.extend(result_list)
                    else:
                        open_list = driver.find_element_by_xpath('//*[@id="subGroupListLink"]')
                        open_list.click()
                        sub_category = driver.find_element_by_xpath('//*[@id="subGroupList"]/div/ul/li['+ str(sub_category_index) +']/a')
                        sub_cate = sub_category.text
                        sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
                        result_list = self.crawler_gmarket(cate, sub_cate, category_code1, category_code2)
                        all_result.extend(result_list)

        return all_result

    ########################### 옥션 ###########################
    def crawler_auction(self, cate, sub_cate, category_code1, category_code2):
        driver = self.get_driver()
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
                    ranking = el.find('div', 'rank').text
                    category_code1 = category_code1
                    category_code2 = category_code2
                    cate = cate
                    sub_cate = sub_cate
                    name = el.find('div', attrs={"class": "info"}).find('em').find('a').text
                    image = el.find('div', attrs={"class": "img"}).find('a').find('img')['src']
                    self.img_url_list.append('https:' + image)
                    self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
                    try:
                        rate = el.find('span', attrs={"class": "down"}).text.strip('%')
                    except:
                        rate = 0  # 할인하지 않는 상품

                    try:
                        if rate != 0:
                            sales_price = el.find('li', attrs={"class": "c_price"}).find('strike').find(
                                'span').text.strip('원')
                            sales_price = int(sales_price.replace(',', ''))
                        else:
                            sales_price = el.find('li', attrs={"class": "d_price"}).find('span').find(
                                'span').text.strip('원')
                            sales_price = int(sales_price.replace(',', ''))
                    except:
                        sales_price = 0  # 무료상품

                    try:
                        discount_price = el.find('li', attrs={"class": "d_price"}).find('span').find('span').text.strip(
                            '원')
                        discount_price = int(discount_price.replace(',', ''))
                    except:
                        discount_price = 0  # 무료상품

                    real_path = el.find('div', attrs={"class": "img"}).find('a')['href']

                    print(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,discount_price, image, rate, real_path))
                    results.append(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,discount_price, image, rate, real_path))

                    # cursor.execute(f"INSERT INTO test_best_product_auction(crawling_date,ranking,category_code1,category_code2, category_name1, category_name2, product_name, sales_price, discount_price, discount_rate, image_name, image_path, real_path,insert_userid, insert_time) \
                    #         VALUES(\"{temp_dict['crawling_date']}\",\"{temp_dict['ranking']}\",\"{temp_dict['category_code1']}\",\"{temp_dict['category_code2']}\",\"{temp_dict['category_name1']}\",\"{temp_dict['category_name2']}\",\
                    #         \"{temp_dict['product_name']}\",\"{temp_dict['sales_price']}\",\"{temp_dict['discount_price']}\",\"{temp_dict['discount_rate']}\",\"{temp_dict['image_name']}\",\"{temp_dict['image_path']}\",\"{temp_dict['real_path']}\",\"{'admin'}\",NOW())")
                except:
                    pass

        return results

    def execute_auction(self):
        self.set_url('http://corners.auction.co.kr/corner/categorybest.aspx')
        self.make_driver()
        driver = self.get_driver()
        category_list = driver.find_elements_by_xpath("//*[@id='contents']/div[1]/div[2]/ul/li/a")
        all_result = []
        for category_index in range(1, len(category_list) + 1):
            category = driver.find_element_by_xpath(
                '//*[@id="contents"]/div[1]/div[2]/ul/li[' + str(category_index) + ']/a')
            if category_index <= 10:
                category_code1 = '0' + str(category_index - 1)
            else:
                category_code1 = str(category_index - 1)
            category_code2 = '00'
            cate = category.find_element_by_xpath(('img'))
            cate = cate.get_attribute('alt')
            sub_cate = '전체'
            category.click()
            result_list = self.crawler_auction(cate, sub_cate, category_code1, category_code2)
            all_result.extend(result_list)
            if category_index == 1:
                pass
            else:
                sub_category_lists = driver.find_elements_by_xpath(
                    '//*[@id="contents"]/div[1]/div[2]/div[' + str(category_index) + ']/ul/li')
                for sub_category_index in range(1, len(sub_category_lists) + 1):
                    category = driver.find_element_by_xpath(
                        '//*[@id="contents"]/div[1]/div[2]/ul/li[' + str(category_index) + ']/a')
                    ActionChains(driver).click_and_hold(category).perform()  # 하위 카테고리가 hover일때만 나오므로 카테고리 클릭 후 홀드
                    if sub_category_index < 10:
                        category_code2 = '0' + str(sub_category_index)
                    else:
                        category_code2 = str(sub_category_index)
                    sub_category = driver.find_element_by_xpath(
                        '//*[@id="contents"]/div[1]/div[2]/div[' + str(category_index) + ']/ul/li[' + str(
                            sub_category_index) + ']/a')
                    sub_cate = sub_category.text

                    ActionChains(driver).move_to_element(sub_category).click().perform()
                    result_list = self.crawler_auction(cate, sub_cate, category_code1, category_code2)
                    all_result.extend(result_list)

        return all_result

    ########################### 11번가 ###########################

    def crawler_11st(self, cate, sub_cate, category_code1, category_code2):
        driver = self.get_driver()
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
            self.img_url_list.append(image)
            self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
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

            print(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
                                  discount_price, image, rate, real_path))
            results.append(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
                                           discount_price, image, rate, real_path))
            # cursor.execute(f"INSERT INTO test_best_product_11st(crawling_date,ranking,category_code1,category_code2, category_name1, category_name2, product_name, sales_price, discount_price, discount_rate, image_name, image_path, real_path,insert_userid, insert_time) VALUES(\"{temp_dict['crawling_date']}\",\"{temp_dict['ranking']}\",\"{temp_dict['category_code1']}\",\"{temp_dict['category_code2']}\",\"{temp_dict['category_name1']}\",\"{temp_dict['category_name2']}\",\"{temp_dict['product_name']}\",\"{temp_dict['sales_price']}\",\"{temp_dict['discount_price']}\",\"{temp_dict['discount_rate']}\",\"{temp_dict['image_name']}\",\"{temp_dict['image_path']}\",\"{temp_dict['real_path']}\",\"{'admin'}\",NOW())")
            # conn.commit()
        # pprint(results)
        return results

    def execute_11st(self):
        self.set_url('https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain')
        self.make_driver()
        driver = self.get_driver()
        category_lists = driver.find_elements_by_xpath("//div[@class='best_category_box']/ul/li/button")
        all_result = []
        for button_index in range(len(category_lists)):
            category = driver.find_element_by_xpath(
                '//*[@id="metaCtgrLi' + str(button_index) + '"]/button')  # 카테고리 find
            if button_index < 10:
                category_code1 = '0' + str(button_index)
            else:
                category_code1 = str(button_index)
            category_code2 = '00'
            cate = category.text
            sub_cate = "전체"
            category.click()  # 카테고리 클릭하여 페이지 이동
            time.sleep(1)
            self.scroll_down_to_end()
            result_list = self.crawler_11st(cate, sub_cate, category_code1, category_code2)
            all_result.extend(result_list)
            self.scroll_up_to_category()
            if button_index == 0:
                pass
            else:
                sub_category_lists = driver.find_elements_by_xpath(
                    '//*[@id="metaCtgrLi' + str(button_index) + '"]/div/ul/li/a')
                for a_index in range(1, len(sub_category_lists) + 1):
                    if a_index < 10:
                        category_code2 = '0' + str(a_index)
                    else:
                        category_code2 = str(a_index)
                    sub_category = driver.find_element_by_xpath(
                        '//*[@id="metaCtgrLi' + str(button_index) + '"]/div/ul/li[' + str(a_index) + ']/a')  # 서브 카테고리
                    sub_cate = sub_category.text
                    sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
                    time.sleep(1)
                    self.scroll_down_to_end()
                    result_list = self.crawler_11st(cate, sub_cate, category_code1, category_code2)
                    all_result.extend(result_list)
                    self.scroll_up_to_category()

        return all_result


crawler = Crawler()
# crawler.execute_gmarket()

crawler.execute_11st()

#crawler.execute_auction()

