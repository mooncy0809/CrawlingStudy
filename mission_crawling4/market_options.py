

gmarket_option={
    "market_name" : "gmarket" ,
    "base_url":"http://corners.gmarket.co.kr/Bestsellers",
    "first_category_xpath": "//*[@id='gBestWrap']/div/div[2]/ul/li/a",
    "first_category_xpath_1" : "//*[@id='categoryTabG']/li[",
    "first_category_xpath_2" : "]/a",

    "second_category_xpath": "//*[@class='cate-l']/div/ul/li/a",
    "second_category_list_type" : "one",

    "second_category_xpath_1" : "//*[@class='cate-l']/div/ul/li[",
    "second_category_xpath_2" : "]/a",
    "open_second_category_xpath" : "//*[@id='subGroupListLink']",
    "ch_second_category_xpath_1" : "//*[@id='subGroupList']/div/ul/li[",
    "ch_second_category_xpath_2" : "]/a",
    "second_category_type" : "two",
    "page_type" : "category_pannel_change",

    "product_list" : "#gBestWrap > div > div:nth-child(5) > div > ul > li",
    "table_name" : "test_best_product_gmarket",
    "ranking" : "p",
    "name" : "a.itemname",
    "image" : "img.lazy",
    "rate" : "em",
    "sales_price" : "div.item_price > div.o-price > span:nth-child(2)",
    "discount_price" : "div.item_price > div.s-price > strong > span",
    "real_path" : "a",

    "ftp_remote_path" : "/home/develop/test2/gmarket_0811/",
    "img_path" : "/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling5/data/gmarket/images/",
}

elevenst_option={
    "market_name" : "11st",
    "base_url":'https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain',
    "first_category_xpath": "//div[@class='best_category_box']/ul/li/button",
    "first_category_xpath_1" : "//*[@id='metaCtgrLi",
    "first_category_xpath_2" : "']/button",

    "second_category_xpath_l1" : "//*[@id='metaCtgrLi",
    "second_category_xpath_l2" : "']/div/ul/li/a",
    "second_category_list_type" : "two",

    "second_category_xpath_1" : "//*[@id='metaCtgrLi",
    "second_category_xpath_2" : "']/div/ul/li[",
    "second_category_xpath_3" : "]/a",
    "second_category_type" : "three",
    "page_type": "scroll_down",

    "product_list" : "#bestPrdList > div > ul > li",
    "table_name" : "test_best_product_11st",
    "ranking" : ".best",
    "name" : "div > a > div.pname > p",
    "image" : "div > a > div.img_plot > img",
    "rate" : "div > a > div.pname > div.price_info.cfix > span.sale",
    "sales_price" : "div.price_info.cfix > span.price_detail > s",
    "discount_price" : "div > a > div.pname > div.price_info.cfix > span.price_detail > strong",
    "real_path" : "div > a",

    "ftp_remote_path" : "/home/develop/test2/11st_0811/",
    "img_path" : "/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling5/data/11st/images/",
}

auction_option={
    "market_name" : "auction",
    "base_url":"http://corners.auction.co.kr/corner/categorybest.aspx",

    "first_category_xpath": "//*[@id='contents']/div[1]/div[2]/ul/li/a",
    "first_category_xpath_1" : "//*[@id='contents']/div[1]/div[2]/ul/li[",
    "first_category_xpath_2" : "]/a",

    "second_category_xpath_l1": "//*[@id='contents']/div[1]/div[2]/div[",
    "second_category_xpath_l2": "]/ul/li",
    "second_category_list_type" : "two",

    "second_category_xpath_1" : "//*[@id='contents']/div[1]/div[2]/div[",
    "second_category_xpath_2" : "]/ul/li[",
    "second_category_xpath_3" : "]/a",
    "second_category_type" : "three",
    "page_type": "category_pannel_hover",

    "product_list" : "#itembest_T > ul.uxb-img",
    "product_list2" : "li",
    "table_name" : "test_best_product_auction",
    "ranking" : "div.rank",
    "name" : "div > div.info > em > a",
    "image" : "div.img > a > img",
    "rate" : "span.down",
    "sales_price" : "li.c_price > span > strike > span",
    "discount_price" : "li.d_price > span.sale > span",
    "real_path" : "div.img > a",

    "ftp_remote_path" : "/home/develop/test2/auction_0811/",
    "img_path" : "/Users/mcy/PycharmProjects/CrawlingStudy/mission_crawling5/data/auction/images/",
    }

def get_market_options():
    markets= [auction_option, gmarket_option, elevenst_option]
    return markets