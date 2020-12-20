import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from selenium import webdriver

import ssl

def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)

    try:
        ssl._create_default_https_context = ssl._create_unverified_context

        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')

            return ret

    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def StarbucksAddress(result):
    Starbucks_URL = 'https://www.starbucks.co.kr/store/store_map.do?disp=locale'
    wd = webdriver.Chrome('C:/Users/Administrator/CRWL_윤영훈/chromedriver.exe')
    wd.get(Starbucks_URL)
    time.sleep(10)
    wd.find_element_by_css_selector(
        '#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(1) > a').click()
    time.sleep(10)
    wd.find_element_by_css_selector('#mCSB_2_container > ul > li:nth-child(1) > a').click()
    time.sleep(10)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')

    starbucks_list = soup.select("#mCSB_3_container > ul > li")

    for i in range(0, len(starbucks_list)):

        lat = starbucks_list[i]['data-lat']
        long = starbucks_list[i]['data-long']
        store_info = list(starbucks_list[i].strings)
        store_name = store_info[1].string.strip()
        store_address = store_info[3].string

        result.append([store_name] + [store_address] + [lat] + [long])
        print(result);

    return


def main():
    result = []

    print('Starbucks ADDRESS CRAWLING START')
    StarbucksAddress(result)
    Starbucks_table = pd.DataFrame(result, columns=('매장명','주소명','위도','경도'))
    Starbucks_table.to_csv("./서울스타벅스매장.csv", encoding="cp949", mode='w', index=True)

    print('FINISHED')


if __name__ == '__main__':
    main()
