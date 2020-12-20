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



def CoffeeBean_Menu(result):
    for page_idx in range(10,27):
        for i in range(0,3):
        
            CoffeeBean_URL = 'https://www.coffeebeankorea.com/menu/list.asp?page=%d&category=%s'%(i+1,str(page_idx+1))    

    
            wd = webdriver.Chrome('/Users/imkyunghwan/Documents/CRWL/201109/chromedriver')

            wd.get(CoffeeBean_URL)
            time.sleep(10)

           
            rcv_data = wd.page_source        
            soupData = BeautifulSoup(rcv_data, 'html.parser')
            coffeeMenu = soupData.select('.txt dt span.kor')
        
            for item in coffeeMenu:
            
                result.append(item.string)
                print(item.string)
        
        
   
        
    return

def cswin_CoffeeBean():
    
    result =[]
    print('CoffeeBean ADDRESS CRAWLING START')
    CoffeeBean_Menu(result)
    coffeebean_table = pd.DataFrame(result)
    coffeebean_table.to_csv("./coffeebean.csv", encoding="cp949", mode='w', index=True)

    print('FINISHED')

    
    
if __name__ == '__main__':
     cswin_CoffeeBean()
