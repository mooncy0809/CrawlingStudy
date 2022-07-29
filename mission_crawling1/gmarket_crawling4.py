import requests
from bs4 import BeautifulSoup
from datetime import datetime


def getall(url,cate):
    dictlist = []
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    for i in range(1, 10):
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
        dictlist.append(temp_dict)


    return dictlist

url=["http://corners.gmarket.co.kr/Bestsellers"]
for i in range(1,10):
    url.append("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G0"+str(i))
for i in range(10,13):
    url.append("http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G" + str(i))
cate=["ALL","패션의류","신발/잡화","화장품/헤어","유아동/출산","스포츠/자동차","컴퓨터/전자","식품","생활/주방/건강","가구/침구","도서/음반","여행","e쿠폰"]

for i in range(0,13):
    print(getall(url[i],cate[i]))











