# Target Format
#
# |  |ingredient name|data available level|score with min|score|score class|cancer|development & reproductive toxicity|allergies & immunotoxicity|etc|
# |::|:-------------:|:------------------:|:------------:|:---:|:---------:|:----:|:---------------------------------:|:------------------------:|:--------------:|
# |0 |WATER          |Robust              |1             |1    |Green      |LOW   |LOW                                |LOW                       |                |
# |1 |FRAGRANCE      |Fair                |8             |8    |Red        |LOW   |LOW                                |HIGH                      |                |
# |2 |GLYCERIN       |Good                |1-2           |2    |Green      |LOW   |LOW                                |LOW                       |depends on usage|

import requests
import bs4
import pandas as pd
import time
import re


## ----------------------------
## Global Variables
BASE_URL = "https://www.ewg.org/"
INGREDIENT_URL = "https://www.ewg.org/skindeep/search/?search_type=ingredients"

HEADERS = {'User-Agent': 'Mozilla/5.0'}
REQUEST_SESS = requests.Session()

WAITING_TIME = 3
## ----------------------------


def get_score_infos_in(img_tag_containing_score_infos) :
    """score_min, score를 img tag에서 얻어낸다."""
    string_of_src_of_img_tag = str(img_tag_containing_score_infos.get("src"))
    matched_for_score = re.search(r'score=\d', string_of_src_of_img_tag)
    score_info = matched.group()
    score = score_info.split("=")[-1]

    matched_for_score_min = re.search(r'score_min=\d', string_of_src_of_img_tag)
    score_min_info = matched.group()
    score_min = score_min_info.split("=")[-1]
    
    return [score_min, score]


def get_infos_in(page_url, request_sess, dict_header_info) :
    """페이지 단위로 데이터를 수집한다."""
    ingredient_names_in_url = []      # 1 - ex. GLYCERIN
    data_available_levels_in_url = [] # 2 - ex. Robust
    scores_with_min_in_url = []       # 3 - ex. 1-2 or 6
    scores_in_url = []                # 4 - ex.   2,   6
    score_classes_in_url = []         # 5 - Green, Yellow, Red

    cancer_infos_in_url = []          # 6 - LOW, LOW_MODERATE, MODERATE, HIGH
    developmental_infos_in_url = []   # 7 - LOW, LOW_MODERATE, MODERATE, HIGH
    allergies_infos_in_url = []       # 8 - LOW, LOW_MODERATE, MODERATE, HIGH
    
    res = request_sess.get(page_url, headers=dict_header_info)
    print("\n페이지 이동 시도 ... " + page_url)
    time.sleep(WAITING_TIME)
    
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    next_url = None
    try :
        next_url = soup.select("a.next_page")[0].get("href")
        next_url = BASE_URL + next_url[1:]
    except :
        next_url = ""
    
    a_tags_about_product = soup.select("p.product-name > a")
    
    for a_tag in a_tags_about_product :
        # 1. product_name
        ingredient_name = a_tag.text
        ingredient_names_in_url.append(ingredient_name)

        suffix = a_tag.get('href')
        url = BASE_URL + suffix[1:]
        response_from_url = request_sess.get(url, headers=HEADERS)
        response_from_url.raise_for_status()

        print(">> 데이터 수집 중 ... " + url)
        soup = bs4.BeautifulSoup(response_from_url.text)
        
        # 2. data_available_levels
        data_avilable_level = soup.find(text="Data: ").find_parent().text.split(" ")[-1]
        data_available_levels_in_url.append(data_avilable_level)

        # 3. scores_with_min
        # 4. scores
        img_tags = soup.select("div.chemical-score.float-r > a > img")
        img_tag = None
        if len(img_tags) != 0 :
            img_tag = img_tags[0]
        string_of_src_of_img_tag = str(img_tag.get("src"))
        
        score_min, score = get_score_infos_in(img_tag)
        
        if int(score) != int(score_min) :
            scores_with_min_in_url.append("{}-{}".format(score_min, score)) # 3-6
        else :
            scores_with_min_in_url.append(score) # 2
        scores_in_url.append(score)
        
        # 5. score_classes
        score_class = "None"
        int_score = int(score)
        if int_score <= 2 :
            score_class = "Green"
        elif int_score <= 6 :
            score_class = "Yellow"
        elif int_score <= 10 :
            score_class = "Red"
        score_classes_in_url.append(score_class)
        
        # 6. cancer_info
        # 7. developmental_info
        # 8. allergies_info
        img_tags_about_info = soup.select(".gauge-img")
        for img_tag in img_tags_about_info :
            split_info = img_tag.get("alt").split(" ")
            title = split_info[0]
            info_for_title = split_info[-1]
            if title == "Cancer" :
                cancer_infos_in_url.append(info_for_title)
            elif title == "Developmental" :
                developmental_infos_in_url.append(info_for_title)
            elif title == "Allergies" :
                allergies_infos_in_url.append(info_for_title)

        time.sleep(WAITING_TIME)
   
    return [ingredient_names_in_url, 
            data_available_levels_in_url,
            scores_with_min_in_url,
            scores_in_url,
            score_classes_in_url,
            cancer_infos_in_url, 
            developmental_infos_in_url, 
            allergies_infos_in_url,
            next_url]


def main() :
    with requests.session() as request_sess :
        headers = {'User-Agent': 'Mozilla/5.0'}
        current_url = INGREDIENT_URL # 처음(1page)부터 끝(500page)까지 스크래핑
    
        ingredient_names = []
        data_available_levels = []
        scores_with_min = []
        scores = []
        score_classes = []
        
        cancer_infos = []
        developmental_infos = []
        allergies_infos = []
        
        while True :
            all_infos_in_current_url = get_infos_in(page_url=current_url,
                                                    request_sess=request_sess,
                                                    dict_header_info=headers)

            ingredient_names_in_url, \
            data_available_levels_in_url, \
            scores_with_min_in_url, \
            scores_in_url, \
            score_classes_in_url, \
            cancer_infos_in_url, \
            developmental_infos_in_url, \
            allergies_infos_in_url, \
            current_url = all_infos_in_current_url
            
            ingredient_names += ingredient_names_in_url
            data_available_levels += data_available_levels_in_url
            scores_with_min += scores_with_min_in_url
            scores += scores_in_url
            score_classes += score_classes_in_url
            
            cancer_infos += cancer_infos_in_url
            developmental_infos += developmental_infos_in_url
            allergies_infos += allergies_infos_in_url
            
            if len(current_url) == 0 :
                break

        result = {
            "ingredient name" : ingredient_names,
            "data available level" : data_available_levels,
            "score with min" : scores_with_min,
            "score" : scores,
            "score class" : score_classes,
            "cancer" : cancer_infos,
            "developmental & reproductive toxicity" : developmental_infos,
            "allergies & immunotoxicity" : allergies_infos
        }

        result = pd.DataFrame(result)

        file_name = "./my_result_from_ewg.csv"
        print("\n\n데이터 수집 완료 ... '{}'".format(file_name))
        result.to_csv(file_name)
        
        
if __name__ == "__main__" :
    main()
    
