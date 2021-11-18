# Target data
# Ex. 7371, 다이하이드록시메틸크로몬, Dihydroxy Methylchromone, 1013-69-0, 디하이드록시메칠크로몬, 산화방지제, 피부컨디셔닝제(기타)

import pandas as pd
import numpy as np

import time
import requests
import bs4
import traceback


## Global Var
BASE_URL = "https://kcia.or.kr/"
SEARCH_URL = "https://kcia.or.kr/cid/search/"
INIT_URLS = ["https://kcia.or.kr/cid/search/ingd_list.php?skind=ALL&page={}".format(i) for i in range(1264, 1996+1)]


def main():
    dict_result = {
        "ingredient_code": [],
        "ko_ingredient_name": [],
        "en_ingredient_name": [],
        "CAS_No": [],
        "before_name": [],
        "use_of_purpose": []
    }
    
    for page_url in INIT_URLS:
        with requests.Session() as req:
            res_page = req.get(page_url)
            try:
                res_page.raise_for_status()
            except:
                print(traceback.format_exc())
            time.sleep(3)

            soup_page = bs4.BeautifulSoup(res_page.text, "html")

            tr_tags = soup_page.select("#content > div > div.sub_content > div > div > table > tbody > tr")

            for tr_tag in tr_tags:
                td_tags = tr_tag.select("td")

                ingredient_code, \
                ko_ingredient_name, \
                en_ingredient_name, \
                CAS_No, \
                before_name = [td_tag.text.strip() if td_tag.text.strip() else np.NaN for td_tag in td_tags]

                a_tag_ingredient = tr_tag.select_one("a")

                ingredient_url = SEARCH_URL + a_tag_ingredient.get("href")
                res_ingredient = req.get(ingredient_url)
                try:
                    res_ingredient.raise_for_status()
                except:
                    print(traceback.format_exc())
                time.sleep(3)

                soup_ingredient = bs4.BeautifulSoup(res_ingredient.text, "html")

                tr_tags = soup_ingredient.select("table.table_list > tbody > tr")

                use_of_purpose = ""
                for tr_tag in tr_tags:
                    content = tr_tag.text.strip()
                    if "배합목적" in content and not use_of_purpose:
                        use_of_purpose = content.replace("배합목적", "").strip()

                dict_result["ingredient_code"].append(ingredient_code)
                dict_result["ko_ingredient_name"].append(ko_ingredient_name)
                dict_result["en_ingredient_name"].append(en_ingredient_name)
                dict_result["CAS_No"].append(CAS_No)
                dict_result["before_name"].append(before_name)
                dict_result["use_of_purpose"].append(use_of_purpose)

                print(" >> " + ", ".join([str(ingredient_code), str(ko_ingredient_name), str(en_ingredient_name), str(CAS_No), str(before_name), str(use_of_purpose)]))

            df_backup = pd.DataFrame(dict_result)
            df_backup.to_csv("./kcia_210326_renew.csv")
            print("~~~~ 백업 완료 ...")
            
            
if __name__ == "__main__":
    main()