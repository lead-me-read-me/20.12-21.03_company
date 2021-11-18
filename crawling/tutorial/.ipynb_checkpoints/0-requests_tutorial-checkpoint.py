## requests_tutorial.py

# 1. import
import requests
print("Current requests version :", requests.__version__)

if __name__ == "__main__":
    # ---------------------------------------------------------
    # 2. 사용 - get(url)로 응답상태 체크
    url = "http://www.naver.com"
    response = requests.get(url)
    # print(type(response)) 
    # -> <class 'requests.models.Response'>

    print("status code(get, only url) :", response.status_code)

    # ---------------------------------------------------------
    # 3. 테이터와 같이 보내기
    # ----
    # 3.1.1 get으로 parameter보내기
    url="http://www.naver.com?a=bbb&b=123"
    response = requests.get(url)

    print("status code(get, param are in url) :", response.status_code)

    # 3.1.2 get과 Dict 이용
    param_dict = {
        "a" : "bbb",
        "b" : 123
    }
    url = "http://www.naver.com"
    response = requests.get(url, params=param_dict)
    print("status code(get, param is in param_dict) :", response.status_code)

    # 3.2. post로 data 보내기
    datas = {
        "a" : "bbb",
        "b" : 123
    }
    url = "http://www.naver.com"

    response = requests.post(url, data=datas)
    print("status code(post, param is in datas) :", response.status_code)

    # ---------------------------------------------------------
    # 4. SSL 인증서를 사용하는 경우
    #  - 보안 문제로 http보다 https를 많이 이용한다.
    #  - SSL로 오류 발생시, verify옵션을 넣는다.
    url = "https://www.naver.com"
    reponse = requests.post(url)

    print("status code(SSL) :", response.status_code)

    # 20.12.21. : 지금은 오류가 없어서 주석처리
    url = "https://www.naver.com"
    reponse = requests.post(url, verify=False)
    print("\nline57\n")
    reponse.raise_for_status()
    #
    # print("status code(SSL, verify=False) :", response.status_code)

    # ---------------------------------------------------------
    # 5. 인증이 필요한 경우
    #  - API 사용시, key토큰을 할당받아 사용하기도 하지만, 
    #    id와 passwd를 통해 인증을 하는 경우도 있다.
    #     -> `auth=(id, pass)`` 옵션 사용.
    url = "https://www.naver.com"
    response = requests.post(url, auth=("id", "pass"))

    print("status code(auth=('id', 'pass')) :", reponse.status_code)

    if response.status_code == 200 :
        print("---\nOkay\n---")
        # print(reponse.text) # reponse.text : 응답으로 얻은 html코드(<class 'str'>)
        print(type(reponse.text))
    else :
        print("Fail")


    # ---------------------------------------------------------
    # 6. 그 외의 옵션들
    # response.raise_for_status() : 200 코드가 아닌 경우, 에러발동.
    # headers
    # cookies
    # timeout

    a_tag = """
    <td>2-브로모-2-나이트로프로판-1,3-디올(브로노폴)</td>
    """
    print(a_tag.get_text())
