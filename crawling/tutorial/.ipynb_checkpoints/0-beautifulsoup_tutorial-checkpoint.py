## beaurifulsoup_tutorial.py

kDebug = False

# 1. import
import bs4
if kDebug :
    print("Current bs4 version :", bs4.__version__)

# 1.1. 수프 만들기
# soup = BeautifulSoup(open("*.html"))
# soup = BeautifulSoup(markup, parser)

# 2. test html(markup)
HTML_DOC = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
if kDebug :
    print(type(HTML_DOC))
    print(HTML_DOC)
    
    
def main():
    # 1. markup 문서를 html.parser에 적용하면 BeautifulSoup객체를 얻는다.
    soup = bs4.BeautifulSoup(HTML_DOC, features="html.parser")
    if kDebug :
        print(soup.prettify())
        print("---------------\n" + str(type(soup.title)))
        print(str(soup.title))
        print(soup.title.name)
        print(soup.title.string)
        
        print(soup.title.parent)
        print(soup.title.parent.name)
        print(soup.title.parent.string)

        print(soup.a)
        print(soup.find_all('a'))    # 문서 전체를 탐색한다.
        print(soup.find(id='link1')) # 문서 탐색 중, 하나 발견시(id는 고유함.) 바로 반환.

        print(soup.head.title)
        print(soup.find('head'))
        print(soup.find('head').find('title'))

        # 자주 사용되는 패턴 : <a>태그를 모두 꺼내서 href(링크)를 출력
        for link in soup.find_all('a') :
            print(link.get('href'))
            # print(link['href']) # 위와 같은 의미임.
        
        # 자주 사용되는 패턴 : 페이지에서 텍스트를 모두 뽑아낸다.
        print(soup.get_text())

    if kDebug :
        a_string = soup.find(text='Lacie')
        print(a_string)
        print(a_string.find_parents('a')) # find_all
        print(a_string.find_parent('a'))  # find

    print(soup.select('p > a'))
    

if __name__ == "__main__" :
    main()
    