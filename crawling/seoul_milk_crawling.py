import requests
import bs4
import pandas as pd
import time


## Globa Var
BASE = "https://www.na100shop.com:433/"
START_URL = "https://www.na100shop.com:433/goodsPlusList.do?c1=281&c2=282"


def main():
    with requests.Session() as req_sess:
        base_res = req_sess.get(START_URL)
        base_soup = bs4.BeautifulSoup(base_res.text, "html")
        
        a_tags_for_category = base_soup.select("ul.tab > li > a")
        
        result = []
        total = 0
        
        for a_tag in a_tags_for_category:
            category_res = req_sess.get(BASE + a_tag.get("href"))
            category_soup = bs4.BeautifulSoup(category_res.text, "html")
            
            product_names = [p_tag.text for p_tag in category_soup.select("p.prod_nm_s")]
            before_prices = [del_tag.text for del_tag in category_soup.select("p.prod_price > del")]
            after_prices = [strong_tag.text for strong_tag in category_soup.select("p.prod_price > strong")]
            
            
            for idx in range(len(product_names)):
                product_name = product_names[idx]
                before_price = before_prices[idx]
                after_price = after_prices[idx]
                
                result.append([product_name, before_price, after_price])
                total += 1
            
            time.sleep(1)
                
        df_result = pd.DataFrame(result, 
                                 columns=["product_name", "price before sale", "price after sale"])
        df_result.to_csv("./{:d}_{}_210310_euckr.csv".format(total, "서울우유"), encoding="euc-kr")


if __name__ == "__main__":
    main()
    