from datetime import datetime
from time import time

def scroll_down_to_end(response=None):
    check_body_height = 0
    while True:
        response.execute_script("window.scrollTo(0, document.body.scrollHeight)") #맨끝까지
        time.sleep(0.5)
        body_height = response.execute_script("return document.body.clientHeight;")
        # 스크롤이 사이트 마지막에 다다르면 while -> break
        if check_body_height == body_height:
            break
        check_body_height = body_height
        time.sleep(0.5)

def scroll_up_to_category(response=None):
    response.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

def parser_11st(response=None):
    datas = list()
    categorys = response.find_elements_by_xpath('//*[@id="layBody"]/div[1]/ul/li/button')
    for i in range(len(categorys)):
        element = response.find_element_by_xpath('//*[@id="metaCtgrLi'+str(i)+'"]/button')
        cate = element.text
        element.click()
        scroll_down_to_end()
        elements = response.find_elements_by_xpath('//*[@id="bestPrdList"]/div/ul/li')
        market_name = '11번가'
        crawling_date = datetime.today().strftime("%Y-%m-%d")
        for el in elements:
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
            temp_dict = {
                "crawling_date": crawling_date,
                "market_name": market_name,
                "category_name": cate,
                'ranking': ranking,
                'product_name': name,
                'sales_price': sales_price,
                'image_path': image,
                'sales_rate': '%.2f' % rate
            }
            datas.append(temp_dict)

        scroll_up_to_category()
    return datas
