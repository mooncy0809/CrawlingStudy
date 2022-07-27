import requests
from bs4 import BeautifulSoup
from datetime import datetime

def gmarket_Crawling_ALL(html):
    temp_dict = {}

    ul_list = html.select('#gBestWrap > div > div:nth-child(5) > div > ul')
    for li in ul_list:
        rank = li.find('li').find('p').text
        name = li.find('li').find('a',{'class':'itemname'}).text
        price = li.find('li').find('div',{'class':'s-price'}).find('span').text.strip('원')
        price = int(price.replace(',', ''))
        img = 'http:'+ li.find('li').find('img')['data-original']
        rate = li.find('em').text.strip('%')
        rate = float(rate)

        temp_dict = {
            "crawling_date" : datetime.today().strftime("%Y-%m-%d"),
            "market_name" : "G-Market",
            "category_name": "ALL",
            'ranking': rank,
            'name': name,
            'price' : price,
            'image_path' : img,
            'sales_rate' : '%.2f'%rate
        }
        print(temp_dict)
    return temp_dict

gmarket_dict = {}
req = requests.get("http://corners.gmarket.co.kr/Bestsellers")
html = BeautifulSoup(req.text,'html.parser')
gmarket_dict = dict(gmarket_dict, **gmarket_Crawling_ALL(html)) #여러 개의 사전을 합쳐야할 때는 ** 연산자를 사용하여, 중괄호 안에 합칠 사전들을 쉼표(,)로 구분하여 나열

print(gmarket_dict)
