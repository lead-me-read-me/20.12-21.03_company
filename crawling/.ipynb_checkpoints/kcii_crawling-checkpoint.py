# Target Data
#
# Ex. 2-브로모-2-나이트로프로판-1,3-디올(브로노폴), 
#     2-Bromo-2-Nitropropane-1,3-Diol / Bronopol/2-Bromo-2-nitropropane-1,3-diol / Bronopol, 
#     52-51-7, 
#     보존제/살균보존제/Preservatives, 
#     한도, 
#     0.1%, 
#     아민류나 아마이드류를 함유하고 있는 제품에는 사용금지, 
#     살균보존제


import pandas as pd
import numpy as np
import re
import os

import traceback

import datetime
import time

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


## Global Var
BASE_URL = "http://cis.kcii.re.kr/"


def login(driver):
    login_id = "any_id"
    login_pass = "any_password"
    
    # 로그인 창으로 이동
    goto_login = driver.find_element_by_css_selector("div.header > ul.rMenu > li > a")
    goto_login.click()
    
    # 아이디 입력
    id_input = driver.find_element_by_css_selector("#memberId")
    id_input.send_keys(login_id)
    
    # 패스워드 입력
    password_input = driver.find_element_by_css_selector("#memberPw")
    password_input.send_keys(login_pass)
    
    # 로그인 버튼 클릭
    login_button = driver.find_element_by_css_selector("#login")
    login_button.click()
    
    time.sleep(3)
    

def goto_limit_info_db(driver):
    # 상단의 `화장품 규제정보DB` 클릭
    limit_info_db_button = driver.find_element_by_css_selector("#wrap > div.gnbArea > div > ul > li.reg > a")
    limit_info_db_button.click()
    
    # 상단의 `국가별 검색` 클릭
    sub_buttons_under_limit_info_db_button = driver.find_elements_by_css_selector("#wrap > div.gnbArea > div > ul > li.reg.on > ul > li > a")

    search_per_nation_button = None
    for sub_button in sub_buttons_under_limit_info_db_button:
        if sub_button.text.strip() == "국가별 검색":
            search_per_nation_button = sub_button
    search_per_nation_button.click()
    time.sleep(3)
    
    # `한국(1428)` 클릭
    korean_button = None
    nation_buttons = driver.find_elements_by_css_selector("#table-nat > tbody > tr > td > a")
    for nation_button in nation_buttons:
        if "한국" in nation_button.text:
            korean_button = nation_button
            break
    korean_button.click()
    
    time.sleep(3)
    
    
def scrap_from(driver, button_ingredient_url):
    # 새탭 열고 전환
    ActionChains(driver).move_to_element(button_ingredient_url).key_down(Keys.COMMAND).click().perform()
    
    # button_ingredient_url.send_keys(Keys.COMMAND)
    # button_ingredient_url.click()
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    
    # 국문명, 영문명 스크랩핑
    kor_name = ""
    en_name = ""
    tr_tags_on_detail_table = driver.find_elements_by_css_selector("table.detail > tbody > tr")
    for tr_tag in tr_tags_on_detail_table:
        if not kor_name:
            if "표준명" in tr_tag.text:
                kor_name = tr_tag.find_element_by_css_selector("td").text.strip()
            if "고시명" in tr_tag.text:
                kor_name = tr_tag.find_element_by_css_selector("td").text.strip()
        if not en_name:
            if "영문명" in tr_tag.text:
                en_name = tr_tag.find_element_by_css_selector("td").text.strip()
        
    # CAS_No 스크랩핑
    cas_no = ""
    tr_tags_on_detail_ids_and_names = driver.find_elements_by_css_selector("table.detail.Ids_and_Names > tbody > tr")
    for tr_tag in tr_tags_on_detail_ids_and_names:
        if not cas_no:
            if "CAS No" in tr_tag.text:
                cas_no = tr_tag.find_element_by_css_selector("td").text.strip()
    
    # 배합목적 스크랩핑
    combine_of_purpose = ""
    tr_tags_on_detail_properties = driver.find_elements_by_css_selector("table.detail.Properties > tbody > tr")
    for tr_tag in tr_tags_on_detail_properties:
        if not combine_of_purpose:
            if "배합목적" in tr_tag.text:
                combine_of_purpose = tr_tag.find_element_by_css_selector("td").text.strip()
    
    # 경우 1. 한국 내에서 성분의 구분, 배합한도, 규제기타, 사용범위 및 제한조건, 사용목적
    # 경우 2. 한국 내에서 성분의 구분, 금지비고, 배합한도, 규제기타, 사용범위 및 제한조건, 사용목적, 기타    
    case = ""
    limit = ""
    regulation = ""
    use_range = ""
    use_of_purpose = ""
    
    tr_tags_on_regulationDetailTable = driver.find_elements_by_css_selector("#regulationDetailTable > table > tbody > tr")
    th_tags_on_regulationDetailTable = driver.find_elements_by_css_selector("#regulationDetailTable > table > thead > tr > th")
    
    for tr_tag in tr_tags_on_regulationDetailTable:
        if "한국" in tr_tag.text:
            td_tags = tr_tag.find_elements_by_css_selector("td")
            texts_in_td_tag = [td_tag.text.strip() for td_tag in td_tags]
            for order, th_tag in enumerate(th_tags_on_regulationDetailTable):
                if "국가" in th_tag.text.strip():
                    continue
                elif "구분" in th_tag.text.strip():
                    case = texts_in_td_tag[order]
                elif "배합한도" in th_tag.text.strip():
                    limit = texts_in_td_tag[order]
                elif "규제기타" in th_tag.text.strip():
                    regulation = texts_in_td_tag[order]
                elif "사용범위" in th_tag.text.strip():
                    use_range = texts_in_td_tag[order]
                elif "사용목적" in th_tag.text.strip():
                    use_of_purpose = texts_in_td_tag[order]
        else:
            continue

    # 현재 탭 닫고 처음탭으로 이동후 3초 쉬기
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    
    print(" >> 스크랩 완료 : " + ", ".join([kor_name, en_name, cas_no, combine_of_purpose, case, limit, regulation, use_range, use_of_purpose]))
    
    return [kor_name, \
            en_name, \
            cas_no, \
            combine_of_purpose, \
            case, \
            limit, \
            regulation, \
            use_range, \
            use_of_purpose]


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR") # 한국어
    
    ### headless 숨기기
    # 1. user-agent 에서 headless 없애기
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    
    # 2. 가짜 플러그인 삽입
    
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    try:
        driver.get("about:blank")
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
        driver.get(BASE_URL)
        driver.implicitly_wait(10)
        login(driver)
        goto_limit_info_db(driver)
        
        list_of_scrap_infomations = []
        
        tr_webelements = driver.find_elements_by_css_selector("#table_1 > tbody > tr")
        for order, tr_webelement in enumerate(tr_webelements):
            button_ingredient_url = tr_webelement.find_element_by_css_selector("td > a")
            list_of_scrap_infomations.append(scrap_from(driver, button_ingredient_url))
            
            if order % 5 == 1:
                df_scrap_infomations = pd.DataFrame(list_of_scrap_infomations)
                df_scrap_infomations.columns = ["kor_name", "en_name", "CAS_No", "배합목적(국/영)", "구분", "배합한도", "규제기타", "사용범위", "사용목적"]
                df_scrap_infomations.to_csv("./kcii_210326.csv")
            
        df_scrap_infomations = pd.DataFrame(list_of_scrap_infomations)
        df_scrap_infomations.columns = ["kor_name", "en_name", "CAS_No", "배합목적(국/영)", "구분", "배합한도", "규제기타", "사용범위", "사용목적"]
        df_scrap_infomations.to_csv("./kcii_210326.csv")
    except:
        print(traceback.format_exc())
    finally:
        driver.quit()
        time.sleep(3)


if __name__ == "__main__":
    main()
