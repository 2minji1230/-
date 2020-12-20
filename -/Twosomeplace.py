import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import datetime
import time
from itertools import count
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



def TwosomePlace_Menu(result):
    TwosomePlace_URL = 'https://www.twosome.co.kr:7009/menu/list.asp?rank=2'    

    
    wd = webdriver.Chrome('/Users/imkyunghwan/Documents/CRWL/201109/chromedriver')

    wd.get(TwosomePlace_URL)
    time.sleep(10)

           
    rcv_data = wd.page_source        
    soupData = BeautifulSoup(rcv_data, 'html.parser')
    coffeeMenu = soupData.select('.des p a font')
    for font in coffeeMenu:
        result.append(font.string)
        print(font.string)
    
   
        
    return

def cswin_TwosomePlace():
    
    result =[]
    print('Twosomeplace ADDRESS CRAWLING START')
    TwosomePlace_Menu(result)
    twosomeplace_table = pd.DataFrame(result)
    twosomeplace_table.to_csv("./twosomeplace.csv", encoding="cp949", mode='w', index=True)

    print('FINISHED')

    
    
if __name__ == '__main__':
     cswin_TwosomePlace()
