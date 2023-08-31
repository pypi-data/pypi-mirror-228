from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class EsliteUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.eslite\.com\/.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer': url, #解決直接request有頁數的頁面回傳內容常是上一頁像有快取的問題，referer要設
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        #prd_urls = [(('http://www.eslite.com' + u['href']) if 'eslite.com' not in u['href'] else u['href']) for u in soup.select('div.box_mid_billboard h3 > a')]
        prd_urls = []
        for item in soup.select('div.box_mid_billboard'):
            u=item.select_one('h3 > a')
            p=item.select_one('span.price_sale span').text.replace(',','')
            prd_urls.append({'url': (('http://www.eslite.com' + u['href']) if 'eslite.com' not in u['href'] else u['href']), 
                           'price':int(p)})

        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.select_one('div.pages a#ctl00_ContentPlaceHolder1_newbook_pages_next')

        if elem:
            self._next_pg_url = ('http://www.eslite.com' + elem['href']) if 'eslite.com' not in elem['href'] else elem['href']
        else:
            self._next_pg_url = None
        return prd_urls
 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    