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
        table_name = 'test_best_product_gmarket'
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        elements = soup.select('#gBestWrap > div > div:nth-child(5) > div > ul > li') # 상품 리스트
        results = []

        for el in elements:
            ranking = el.select_one('p').text
            category_code1 = category_code1
            category_code2 = category_code2
            cate = cate
            sub_cate = sub_cate
            name = el.select_one('a.itemname').text
            image = 'https:' + el.select_one('img.lazy')['src']
            self.img_url_list.append(image)
            self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
            try:
                rate = el.select_one('em').text.strip('%')
            except:
                rate = 0 # 할인하지 않는 상품

            try:
                if rate != 0:
                    sales_price = el.select_one('div.item_price > div.o-price > span:nth-child(2)').text.strip('원')
                    sales_price = int(sales_price.replace(',', ''))
                else:
                    sales_price = el.select_one('div.item_price > div.s-price > strong > span').text.strip('원')
                    sales_price = int(sales_price.replace(',', ''))
            except:
                sales_price = 0 # 무료상품

            try:
                discount_price = el.select_one('div.item_price > div.s-price > strong > span').text.strip('원')
                discount_price = int(discount_price.replace(',', ''))
            except:
                discount_price = 0 # 무료상품

            real_path = el.select_one('a')['href']

            temp_dict = self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
                                        discount_price, image, rate, real_path)
            print(temp_dict)
            results.append(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
                                           discount_price, image, rate, real_path))
            # self.insert_db(temp_dict,table_name)


        return results

    def execute_gmarket(self):
        self.set_url('http://corners.gmarket.co.kr/Bestsellers')
        self.make_driver()
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

        conn = self.db_connect()
        conn.close()

        return all_result

    ########################### 옥션 ###########################
    def crawler_auction(self, cate, sub_cate, category_code1, category_code2):
        driver = self.get_driver()
        market_name = '옥션'
        table_name = 'test_best_product_auction'
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
                    ranking = el.select_one('div.rank').text
                    category_code1 = category_code1
                    category_code2 = category_code2
                    cate = cate
                    sub_cate = sub_cate
                    name = el.select_one('div > div.info > em > a').text
                    image = 'https:' + el.select_one('div.img > a > img')['src']
                    self.img_url_list.append(image)
                    self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
                    try:
                        rate = el.select_one('span.down').text.strip('%')
                    except:
                        rate = 0  # 할인하지 않는 상품

                    try:
                        if rate != 0:
                            sales_price = el.select_one('li.c_price > span > strike > span').text.strip('원')
                            sales_price = int(sales_price.replace(',', ''))
                        else:
                            sales_price = el.select_one('li.d_price > span.sale > span').text.strip('원')
                            sales_price = int(sales_price.replace(',', ''))
                    except:
                        sales_price = 0  # 무료상품

                    try:
                        discount_price = el.select_one('li.d_price > span.sale > span').text.strip('원')
                        discount_price = int(discount_price.replace(',', ''))
                    except:
                        discount_price = 0  # 무료상품

                    real_path = el.select_one('div.img > a')['href']

                    temp_dict = self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,discount_price, image, rate, real_path)
                    print(temp_dict)
                    results.append(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,discount_price, image, rate, real_path))
                    self.insert_db(temp_dict, table_name)


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

                    # ActionChains(driver).move_to_element(sub_category).click().perform()
                    sub_category.click()
                    result_list = self.crawler_auction(cate, sub_cate, category_code1, category_code2)
                    all_result.extend(result_list)

        conn = self.db_connect()
        conn.close()

        return all_result

    ########################### 11번가 ###########################

    def crawler_11st(self, cate, sub_cate, category_code1, category_code2):
        driver = self.get_driver()
        market_name = '11번가'
        table_name = 'test_best_product_11st'
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        elements = soup.select('#bestPrdList > div > ul > li')
        results = []
        for el in elements:
            ranking = el.select_one('.best').text
            category_code1 = category_code1
            category_code2 = category_code2
            cate = cate
            sub_cate = sub_cate
            name = el.select_one('div > a > div.pname > p').text
            name = name.replace('"', '')
            image = el.select_one('div > a > div.img_plot > img')['src']
            self.img_url_list.append(image)
            self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
            try:
                rate = el.select_one('div > a > div.pname > div.price_info.cfix > span.sale').text.strip('%\n')
            except:
                rate = 0  # 할인하지 않는 상품

            try:
                if rate != 0: #할인하는 상품의 할인전 가격
                    sales_price = el.select_one('div.price_info.cfix > span.price_detail > s').text.strip('원')
                    sales_price = int(sales_price.replace(',', ''))
                else: #할인가격
                    sales_price = el.select_one('div > a > div.pname > div.price_info.cfix > span.price_detail > strong').text.strip('원')
                    sales_price = int(sales_price.replace(',', ''))
            except:
                sales_price = 0  # 무료상품

            try:
                discount_price = el.select_one('div > a > div.pname > div.price_info.cfix > span.price_detail > strong').text.strip('원')
                discount_price = int(discount_price.replace(',', ''))
            except:
                discount_price = 0  # 무료상품

            real_path = el.select_one('div > a')['href']

            print(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
                                  discount_price, image, rate, real_path))
            # results.append(self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
            #                                discount_price, image, rate, real_path))
            # self.insert_db(temp_dict, table_name)
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
        conn = self.db_connect()
        conn.close()
        return all_result


if __name__ == '__main__':
    crawler = Crawler()
    # crawler.execute_gmarket()
    # crawler.execute_11st()
    crawler.execute_auction()
