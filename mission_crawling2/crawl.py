from crawler import SeleniumRequest
from crawler.parser import parser_11st
from pprint import pprint  # 객체를 예쁘게 출력해주는 파이썬 내장 라이브러리

targets = {
    "11st": {
        "url": 'https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain'
        , "parser": "parser_11st"
    }
}

request = SeleniumRequest( driver_path='/usr/local/bin/chromedriver')

for key in targets.keys():
    info = targets[key]

    url = info['url']
    callback = eval(info['parser']) # 문자열로된 st11_parser함수를 callback에 저장하는 용도로 사용됨.

    data = request.get( url, callback=callback)

    pprint(data)