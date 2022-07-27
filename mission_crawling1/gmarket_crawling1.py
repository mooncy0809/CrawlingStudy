import requests
from bs4 import BeautifulSoup
from datetime import datetime

response = requests.get("http://corners.gmarket.co.kr/Bestsellers")
html = response.text
soup = BeautifulSoup(html,'html.parser')

def getrank(select):
    rank = soup.select_one(select).text
    print(type(rank))
    return rank

def getname(select):
    name = soup.select_one(select).text
    print(type(name))
    return name

def getprice(select):
    price = soup.select_one(select).text.strip('원')
    price = int(price.replace(',',''))
    print(type(price))
    return price

def getimage(select):
    image = soup.select_one(select)['data-original']
    print(type(image))
    return 'http:' + image

def getsale_rate(select):
    rate = soup.select_one(select).text.strip('%')
    rate = float(rate)
    print(type(rate))
    return '%.2f' % rate

results = [
    {
        "crawling_date" : datetime.today().strftime("%Y-%m-%d") ,
        "market_name" : "G-Market",
        "category_name" : "ALL",
        "ranking": getrank('#no1'),
        "product_name" : getname('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child(3) > a'),
        "sales_price" : getprice('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child(3) > div.item_price > div.s-price > strong > span > span'),
        "image_path" : getimage('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child(3) > div.thumb > a > img'),
        "sales_rate" : getsale_rate('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child(1) > div.item_price > div.s-price > span > em')
    }
]

print(results)