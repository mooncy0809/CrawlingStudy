import requests
from bs4 import BeautifulSoup as BS

def mnet_Crawling(html):
    temp_dict={}
    tr_list = html.select('div')