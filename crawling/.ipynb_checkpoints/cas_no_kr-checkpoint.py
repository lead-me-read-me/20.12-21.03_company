import requests
import bs4

import re
import os
import time

import traceback

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
import numpy as np


BASE_URL = "http://www.chemnet.com"
CAS_KR_BASE_URL = "http://www.chemnet.com/cas/kr/"


def scrap_from(a_product_url):
    name = ""
    alias = ""
    CAS_No = ""
    EC_No = ""
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    
    try:
        driver.get(a_product_url)
        driver.implicitly_wait(10)
        time.sleep(3)
        
        print(" >> 크롤링 시도 ... {}".format(a_product_url))
        
        tr_tags_for_contents = driver.find_elements_by_css_selector("#main-en > div.left-en > table > tbody > tr > td > table > tbody > tr")

        for order, tr_tag_for_contents in enumerate(tr_tags_for_contents):
            content_in_tr_tag = tr_tag_for_contents.text.strip()
            if "명칭" in content_in_tr_tag and not name:
                name = content_in_tr_tag.replace("상품명칭", "").strip()
            elif "별명" in content_in_tr_tag and not alias:
                alias = content_in_tr_tag.replace("별명", "").strip()
            elif "cas번호" in content_in_tr_tag and not CAS_No:
                CAS_No = content_in_tr_tag.replace("cas번호", "").strip()
            elif "EC번호" in content_in_tr_tag and not EC_No:
                EC_No = content_in_tr_tag.replace("EC번호", "").strip()

        print("   >> {}".format(", ".join([name, alias, CAS_No, EC_No])))
    except:
        print(traceback.format_exc())
    finally:
        driver.quit()
        time.sleep(2)
        return [name, alias, CAS_No, EC_No]
    
    
def main():
    dict_result = {
        "name": [],
        "alias": [],
        "CAS_No": [],
        "EC_No": []
    }
    
    with requests.Session() as req:
        res_CAS_kr = req.get(CAS_KR_BASE_URL)
        try:
            res_CAS_kr.raise_for_status()
        except:
            print(traceback.format_exc())
        time.sleep(2)
        soup_CAS_kr = bs4.BeautifulSoup(res_CAS_kr.text, "html")
        
        a_tags_for_several_products = soup_CAS_kr.select("ul > li > a.blue")
        
        for a_tag_for_several_products in a_tags_for_several_products[42:]:
            several_products_url = BASE_URL + a_tag_for_several_products.get("href")
            print("Move to ... {}, {}".format(a_tag_for_several_products.text, several_products_url))
            
            res_several_products = req.get(several_products_url)
            try:
                res_several_products.raise_for_status()
            except:
                print(traceback.format_exc())
            time.sleep(2)
            soup_several_products = bs4.BeautifulSoup(res_several_products.text, "html")
            
            a_tags_for_a_product = soup_several_products.select("ul > li.bw2 > a.blue")
            
            for a_tag_for_a_product in a_tags_for_a_product:
                a_product_url = BASE_URL + a_tag_for_a_product.get("href")
                
                name, alias, CAS_No, EC_No = scrap_from(a_product_url)

                dict_result['name'].append(name)
                dict_result['alias'].append(alias)
                dict_result['CAS_No'].append(CAS_No)
                dict_result['EC_No'].append(EC_No)
            
            df_result = pd.DataFrame(dict_result)
            df_result.to_csv("./CAS_No_210329.csv")
            
        df_result = pd.DataFrame(dict_result)
        df_result.to_csv("./CAS_No_210329.csv")


if __name__ == "__main__":
    main()
    
