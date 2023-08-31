from .base_parser import BaseParser
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import logging
from ..common.utility import utility
from requests.adapters import HTTPAdapter
requests.adapters.DEFAULT_RETRIES = 0
import html

class EsliteParser(BaseParser):
    def __init__(self):
        self._ecid = 4
        self._ecpid = None
    def get_ec_popidx(self):
        return 90
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.eslite\.com\/product\.aspx\?pgid=(\w+)?', url.lower())
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if ecpid:
            self._ecpid = ecpid
            is_book = True
        return is_book

    def scrape_page_to_strprd(self, url, res):
        '''# ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='http://www.eslite.com/')
        res = reqss.get(url, headers=headers, timeout=10)'''
        if res.status_code == 404:
            print('-- 商品已下架? 404找不到商品頁') 
            return None
        if res.status_code != 200:
            raise ValueError(f'-- status_code is {res.status_code}')
        pure_html = res.text
        res.connection.close()
        # ---- 準備剖析html ----
        popIdx = self.get_ec_popidx()
        prd = {}
        soup = BeautifulSoup(pure_html,features="lxml")
        is_onshelf = self._extract_if_onshelf(soup)
        if is_onshelf == 1: 
            # ---- step1 商品頁可取得的資訊 ----
            prd['Name'] = self._extract_name(soup)
            prd['Url'] = self._extract_url(soup)
            prd['ImgUrl'] = self._extract_imgurl(soup)
            prd['ImgUrlList'] = self._extract_imgurl_list(soup) if self._extract_imgurl_list(soup) else prd['ImgUrl']
            prd['VideoUrl'] = None
            prd['VideoUrlList'] = None
            prd['OriPrice'] = self._extract_oriprice(soup)
            prd['Price'] = self._extract_price(soup)
            prd['Author'] = self._extract_author(soup)
            prd['ISBN'] = self._extract_isbn(soup)
            prd['ECID'] = self._ecid
            prd['ECPID'] = self._extract_ecpid_by_url(url)
            prd['ECCatlog'] = self._extract_eccatlog(soup) 
            prd['isOnShelf'] = is_onshelf
            
            prd['isEnable'] = True # esc index v2是用boolean
            prd['Desc'] = self._extract_desc(soup)
            prd['ModifyTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            prd['CreateTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            prd['PopIdx'] = popIdx
            prd['CatID'] = None
            prd['Translator'] = self._extract_translator(soup)
            prd['PublishDate'] = self._extract_pub_date(soup)
            
            prd['Publisher'] = self._extract_publisher(soup) # esc index v2改名為publishcompany->publisher
            prd['Painter'] = self._extract_painter(soup)
            prd['OriginName'] = self._extract_origin_name(soup)
            prd['Summary'] = self._extract_summary(soup)
            prd['ISBN10'] = self._extract_isbn10(soup)
            prd['ISBNADD'] = self._extract_isbnadd(soup)
            prd['BookType'] = self._extract_booktype(soup, prd)
            prd['Text1'] = None
            prd['Text2'] = None
            prd['Text3'] = None
            prd['Keyword1'] = None
            prd['Keyword2'] = None
            prd['Keyword3'] = None
            
            # ---- step2 特殊處理的資訊 ----
            # 沒有原價的商品:https://www.kingstone.com.tw/basics/basics.asp?kmcode=2019920474639&lid=book_class_sec_se&actid=WISE
            if prd['OriPrice'] is None:
                prd['OriPrice'] = prd['Price']
            
            return prd

        else:
            print('-- 商品已下架? 找不到購物車鈕') 
            return None #回傳None則在main_parser下架商品

    # ======== 私有 萃取各值的方法 ========
    def _extract_if_onshelf(self, soup):
        val = 0
        elem = soup.select_one("div.PI_info iframe")
        if elem:
            response = requests.get(elem.attrs['src'])
            iframe_soup = BeautifulSoup(response.content)
            btn = iframe_soup.select_one("div#cartDiv a.PI_cart")
            if btn:
                val = 1
        return val
    
    def _extract_name(self, soup):
        val = soup.select_one("span#ctl00_ContentPlaceHolder1_lblProductName").get_text()
        return val
    
    def _extract_url(self, soup):
        val = soup.find("link", rel="canonical")['href']
        return val
    
    def _extract_imgurl(self, soup):
        val = soup.select_one('div.PI_img-more a#mainlink img')['src']
        return val
    
    def _extract_imgurl_list(self, soup):
        elems = soup.select('div#showArea a[rel*="lightbox"]')
        val = ','.join([elem['href'] for elem in elems])
        return val #已測試若沒有為''

    def _extract_ecpid_by_url(self, url):
        match = re.search('\?pgid=(\w+)?', url.lower())
        return match.group(1)

    def _extract_eccatlog(self, soup):
        eccats = [item.get_text() for item in soup.select('div#path a')[1:]]
        return '>'.join(eccats)

    def _extract_author(self, soup):
        val = None
        elem = soup.select_one('h2.PI_item #ctl00_ContentPlaceHolder1_CharacterList_ctl00_CharacterName_ctl00_linkName')
        if elem:
            val = elem.get_text()
        return val

    def _extract_isbn(self, soup):
        val = None
        href = soup.find("a", rel="lyteframe")
        if href:
            match = re.search('\?isbn=(\d+)?', href['href'])
            val = match.group(1)
        return val

    def _extract_desc(self, soup):
        val = None
        elem = soup.select_one("div#ctl00_ContentPlaceHolder1_Product_info_more1_introduction")
        if elem:
            val = html.escape(elem.decode_contents())[:8000]
        return val

    def _extract_translator(self, soup):
        val = None
        elem = soup.select_one('h3.PI_item #ctl00_ContentPlaceHolder1_CharacterList_ctl02_CharacterName_ctl00_linkName')
        if elem:
            val = elem.get_text()
        return val

    def _extract_pub_date(self, soup):
        val = None
        elem = soup.find(text=re.compile(r'出版日期 ／'))
        if elem:
            val = elem.replace('出版日期 ／', '').strip()
        return val

    def _extract_publisher(self, soup):
        val = None
        elem = soup.find(text=re.compile(r'出版社 ／'))
        if elem:
            e = elem.parent.select_one('a')
            if e:
                val = e.get_text()
        return val

    def _extract_oriprice(self, soup):
        val = None
        elem = soup.select_one('h3.PI_item span.price')
        if elem:
            val = elem.get_text().replace(',', '')
        return val

    def _extract_price(self, soup):
        val = None
        elem = soup.select('h3.PI_item span.price_sale')[-1]
        if elem:
            val = elem.get_text().replace(',', '')
        return val

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
        for elem in soup(text=re.compile(r'繪者：')):
            match = re.search(r'繪者：(.+)', elem.parent.text)
            val = match.group(1) if match else None
            if val:
                val = val.strip()
        return val
    def _extract_origin_name(self, soup):
        val = None
        elem = soup.select_one("span#ctl00_ContentPlaceHolder1_lblOriginalName")
        if elem:
            val = elem.get_text()
        return val  
    def _extract_summary(self, soup):
        val = None
        return val
    def _extract_isbn10(self, soup):
        val = None
        elem = soup.find(text=re.compile(r'ISBN 10 ／'))
        if elem:
            val = elem.replace('ISBN 10 ／', '').strip()
        return val
    def _extract_isbnadd(self, soup):
        val = None
        elem = soup.find(text=re.compile(r'EAN ／'))
        if elem:
            val = elem.replace('EAN ／', '').strip()
        return val
    
    def _extract_booktype(self, soup, prd):
        book_type = 'book'
        ary_name = [prd['Name'] , prd['ECCatlog']]
        filtered_ary_name = [x for x in ary_name if x is not None]
        if any('電子書' in x for x in filtered_ary_name):
            book_type = 'ebook'
        return book_type
    
    