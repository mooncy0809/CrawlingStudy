import requests
from bs4 import BeautifulSoup
from datetime import datetime

def getall(url,cate):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    for i in range(1, 101):
        rank = soup.select_one('#no' + str(i)).text
        name = soup.select_one('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child(' + str(i) + ') > a').text
        price = soup.select_one('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child('+str(i)+') > div.item_price > div.s-price > strong > span > span').text.strip('원')
        price = int(price.replace(',', ''))
        image = soup.select_one('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child('+str(i)+') > div.thumb > a > img')['data-original']
        try:
            rate = soup.select_one('#gBestWrap > div > div:nth-child(5) > div > ul > li:nth-child('+str(i)+') > div.item_price > div.s-price > span > em').text.strip('%')
            rate = float(rate)
        except:
            rate = 0
        temp_dict = {
            "crawling_date" : datetime.today().strftime("%Y-%m-%d"),
            "market_name" : "G-Market",
            "category_name": cate,
            'ranking': rank,
            'product_name': name,
            'sales_price' : price,
            'image_path': 'http:' + image,
            'sales_rate': '%.2f' % rate
        }
        print(temp_dict)
    return temp_dict

url=["http://corners.gmarket.co.kr/Bestsellers"]
for i in range(1,13):
    url.append("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G0"+str(i))

cate=["ALL","패션의류","신발/잡화","화장품/헤어",]

getall("http://corners.gmarket.co.kr/Bestsellers","ALL")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G01","패션의류")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G02","신발/잡화")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G03","화장품/헤어")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G04","유아동/출산")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07","식품")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G08","생활/주방/건강")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G09","가구/침구")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G05","스포츠/자동차")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G06","컴퓨터/전자")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G10","도서/음반")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G11","여행")
getall("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G12","e쿠폰")


