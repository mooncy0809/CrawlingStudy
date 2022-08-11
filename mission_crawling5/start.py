from main import Common
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import time
from market_options import get_market_options


class Crawler(Common):
    def __init__(self):
        pass

    def find_products_list(self,req,product_list):
        soup = BeautifulSoup(req, 'html.parser')
        elements = soup.select(product_list)
        return elements

    def find_second_products_list(self,elements):
        element = BeautifulSoup(elements, 'html.parser')
        elements_2 = element.select('li')
        return elements_2

    def find_first_category_elements(self, category_xpath):
        driver = self.get_driver()
        category_list = driver.find_elements_by_xpath(category_xpath)
        return category_list

    def category_click(self,category_xpath):
        driver = self.get_driver()
        category = driver.find_element_by_xpath(category_xpath)
        cate = category.text
        if category.text == '':
            cate = category.find_element_by_xpath('img')
            cate = cate.get_attribute('alt')
        category.click()

        return cate

    def find_second_category_elements(self, subcategory_xpath):
        driver = self.get_driver()
        sub_category_lists = driver.find_elements_by_xpath(subcategory_xpath)
        return sub_category_lists

    def second_category_click(self,subcategory_xpath):
        driver = self.get_driver()
        sub_category = driver.find_element_by_xpath(subcategory_xpath)
        sub_cate = sub_category.text
        sub_category.click()  # 서브 카테고리 클릭하여 페이지 이동
        return sub_cate

    def scraper(self,el,mall_option,category_code1,category_code2,cate,sub_cate):
        ranking = el.select_one(mall_option['ranking']).text
        category_code1 = category_code1
        category_code2 = category_code2
        cate = cate
        sub_cate = sub_cate
        name = el.select_one(mall_option['name']).text
        name = name.replace('"', '')
        if mall_option['page_type'] == 'category_pannel_hover' or mall_option['page_type'] == 'category_pannel_change':
            image = 'https:' + el.select_one(mall_option['image'])['src']
        else :
            image = el.select_one(mall_option['image'])['src']
        self.img_url_list.append(image)
        self.img_name_list.append(category_code1 + '_' + category_code2 + '_' + ranking + '.jpg')
        try:
            rate = el.select_one(mall_option['rate']).text.strip('%\n')
        except:
            rate = 0  # 할인하지 않는 상품

        try:
            if rate != 0:  # 할인하는 상품의 할인전 가격
                sales_price = el.select_one(mall_option['sales_price']).text.strip('원')
                sales_price = int(sales_price.replace(',', ''))
            else:  # 할인가격
                sales_price = el.select_one(mall_option['discount_price']).text.strip('원')
                sales_price = int(sales_price.replace(',', ''))
        except:
            sales_price = 0  # 무료상품

        try:
            discount_price = el.select_one(mall_option['discount_price']).text.strip('원')
            discount_price = int(discount_price.replace(',', ''))
        except:
            discount_price = 0  # 무료상품

        real_path = el.select_one(mall_option['real_path'])['href']

        temp_dict = self.dictionary(ranking, category_code1, category_code2, cate, sub_cate, name, sales_price,
                                    discount_price, image, rate, real_path)
        print(temp_dict)

        return temp_dict


    def crawler(self, cate, sub_cate, category_code1, category_code2,mall_option):
        results = []
        driver = self.get_driver()
        req = driver.page_source
        table_name = mall_option['table_name']
        elements = self.find_products_list(req,mall_option['product_list'])

        if mall_option['page_type'] == 'category_pannel_hover':
            for element in elements:
                elements2 = element.select(mall_option['product_list2'])
                for el in elements2:
                    try:
                        temp_dict = self.scraper(el, mall_option, category_code1, category_code2, cate, sub_cate)
                        self.insert_db(temp_dict, table_name)
                        results.append(temp_dict)
                    except:
                        pass
        else:
            for el in elements:
                temp_dict = self.scraper(el,mall_option,category_code1,category_code2,cate,sub_cate)
                self.insert_db(temp_dict, table_name)
                results.append(temp_dict)


        # print(results)
        return results

    def execute(self, mall_option):
        all_result = []
        mall_option = mall_option
        self.set_url(mall_option['base_url'])
        self.make_driver()
        driver = self.get_driver()
        category_list = self.find_first_category_elements(mall_option['first_category_xpath'])
        if mall_option['page_type'] == "scroll_down":  # 페이지타입 scroll_down이면 카테고리 리스트 0번부터 시작
            category_index = 0
            zero_start = True
        else:
            category_index = 1
            zero_start = False
        for i in range(len(category_list)):
            # 카테고리 코드 설정 (00~1..)
            if category_index < 10:
                category_code1 = '0' + str(category_index)
            else:
                category_code1 = str(category_index)
            category_code2 = '00' # '전체'는 항상 00
            sub_cate = 'ALL' # 상위 카테고리 크롤링 시작하기 전 서브 카테고리 'ALL'로 초기화

            if mall_option['page_type'] == "scroll_down":
                cate = self.category_click(mall_option['first_category_xpath_1'] + str(category_index) + mall_option['first_category_xpath_2'])
                time.sleep(1)
                self.scroll_down_to_end()
                time.sleep(1)
                result_list = self.crawler(cate, sub_cate, category_code1, category_code2,mall_option)
                all_result.extend(result_list)
                self.scroll_up_to_category()
            else:
                cate = self.category_click(mall_option['first_category_xpath_1'] + str(category_index) + mall_option['first_category_xpath_2'])
                result_list = self.crawler(cate, sub_cate, category_code1, category_code2,mall_option)
                all_result.extend(result_list)

            if zero_start == True and category_index == 0:
                pass
            elif zero_start == False and category_index == 1:
                pass
            else:
                if mall_option['second_category_list_type'] == 'one':
                    sub_category_lists = self.find_second_category_elements(mall_option['second_category_xpath'])
                elif mall_option['second_category_list_type'] == 'two' :
                    sub_category_lists = self.find_second_category_elements(mall_option['second_category_xpath_l1'] + str(category_index) + mall_option['second_category_xpath_l2'])

                for sub_category_index in range(1, len(sub_category_lists)+1):
                    # 서브카테고리 코드 설정
                    if sub_category_index < 10:
                        category_code2 = '0' + str(sub_category_index)
                    else:
                        category_code2 = str(sub_category_index)

                    if mall_option['second_category_type'] == 'two':
                        sub_category_xpath = mall_option['second_category_xpath_1'] + str(sub_category_index) + mall_option['second_category_xpath_2']
                    elif mall_option['second_category_type'] == 'three':
                        sub_category_xpath = mall_option['second_category_xpath_1'] + str(category_index) + mall_option['second_category_xpath_2'] + str(sub_category_index) + mall_option['second_category_xpath_3']

                    if mall_option['page_type'] == 'category_pannel_change' and sub_category_index != 1:
                        self.second_category_click(mall_option['open_second_category_xpath'])
                        sub_cate = self.second_category_click(mall_option['ch_second_category_xpath_1'] + str(sub_category_index) + mall_option['ch_second_category_xpath_2'])
                        result_list = self.crawler(cate, sub_cate, category_code1, category_code2, mall_option)
                        all_result.extend(result_list)

                    elif mall_option['page_type'] == 'scroll_down':
                        sub_cate = self.second_category_click(sub_category_xpath)
                        time.sleep(1)
                        self.scroll_down_to_end()
                        time.sleep(1)
                        result_list = self.crawler(cate, sub_cate, category_code1, category_code2, mall_option)
                        all_result.extend(result_list)
                        self.scroll_up_to_category()

                    elif mall_option['page_type'] == 'category_pannel_hover':
                        category = driver.find_element_by_xpath(mall_option['first_category_xpath_1'] + str(category_index) + mall_option['first_category_xpath_2'])
                        ActionChains(driver).click_and_hold(category).perform()  # 하위 카테고리가 hover일때만 나오므로 카테고리 클릭 후 홀드
                        sub_cate = self.second_category_click(sub_category_xpath)
                        result_list = self.crawler(cate, sub_cate, category_code1, category_code2,mall_option)
                        all_result.extend(result_list)

                    else:
                        sub_cate = self.second_category_click(sub_category_xpath)
                        result_list = self.crawler(cate, sub_cate, category_code1, category_code2,mall_option)
                        all_result.extend(result_list)
            category_index += 1
        conn = self.db_connect()
        conn.close()
        self.img_download(mall_option['img_path'])
        self.transfer_image_to_ftp_server(mall_option['img_path'],mall_option['ftp_remote_path'])


if __name__ == '__main__':
    crawler = Crawler()
    market_options = get_market_options()
    for market in market_options:
        crawler.execute(market)
