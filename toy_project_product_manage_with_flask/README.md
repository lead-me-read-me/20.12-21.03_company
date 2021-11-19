# :one: Intro

 사내 E-커머스 웹 애플리케이션 등을 유지보수하는 일을 하기 전, 나는 웹 개발을 해본 적 없는 비전공자였기때문에 관련 Toy Project 를 진행했다. 대부분의 사내 back-end 시스템이 `Django` 로 개발이 되어있었지만 개발팀의 다른 팀원들에게 물어보니 `Django` 는 지금 우리 시스템의 규모를 생각했을때 over-spec 이라는 의견이 있었다.  

 그리고 처음 back-end 개발을 장고로 시작하면 어려울 수 있다는 조언도 있었기 때문에 여러 프레임워크들 중 **`Flask`** 를 골라 documents 를 읽어보면서 간단한 웹 애플리케이션부터 만들면서 프레임워크에 익숙해지고 최종 Toy Project 를 완성하였다.

# :two: Contents

### 2.1.  Tutorials

1. [Quick Start](./tutorial/1_quick_start/main.py) 
   * 프레임워크를 처음 접하다 보니 [Documents 의 Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/) 를 보고 주석을 달면서 공부했다.
   * 이해하기 어려운 내용들도 많았지만 우선 적으면서 최대한 흐름이라도 파악해보려고 노력해보았다.

2. [flaskr](./tutorial/2_flaskr/flaskr.py) 및 [app test](./tutorial/2_flaskr/flaskr_test.py) 
   * Quick Start 와 마찬가지로 [Documents 의 Flaskr](https://flask.palletsprojects.com/en/0.12.x/tutorial/introduction/) 을 참고하였다. ([번역 페이지](https://flask-docs-kr.readthedocs.io/ko/latest/tutorial/introduction.html))
   * 로그인, 로그아웃 기능을 추가하는 Tutorial 로 자격 검증을 하는 과정을 추가하여 관리자만 DB 접근의 허용하도록 하는 것이 목표
   * 또, Flask app 을 테스트하는 방법도 제시된대로 따라서 작성하고 주석을 달면서 내용을 파악해보려고 시도했다.
   * 그 외에, [signal note](./tutorial/2_flaskr/4_signal_note.md), [pluggable views note](./tutorial/2_flaskr/5_pluggable_views.md), [application context note](./tutorial/2_flaskr/6_application_context.md) 등을 작성하며 공부해보았다.
3. [Flask 와 RDBMS(MySQL) 연동](./tutorial/3_mysql_test/main.py) 
   * [참고한 Documents](https://flask.palletsprojects.com/en/2.0.x/tutorial/database/) 보면서 코드를 작성했지만, 사내에서는 MySQL 을 사용하고 있기 때문에 Documents 에서 제시한 `sqlite3` 모듈 대신 `pymysql` 을 사용하였다.
   * 여기까지만 진행해도 Toy Project 를 진행하는데 무리가 없다고 생각하여 상품 데이터를 관리하는 웹 애플리케이션을 작성해보았다.

### 2.2. Toy Project

* 문제
  * 상품마다 브랜드, 영양소, 용량 정보가 안들어가는 경우가 많다.
  * 그리고 섬네일, 상세 이미지들이 일치하는지 확인할 필요가 있다.
* 요구사항
  * 위 문제들을 해결하기 위한 정보 추가 및 수정기능이 필요하다.
  * 작업을 쉽게 할 수 있도록 직관적인 UI 가 제공되어야한다.
* [Meta-data ](./data/backup_dry_tissue_page8.csv) 준비
  * `name`: 상품의 이름
  * `product img path`: 상품의 섬네일 이미지 경로
  * `product detail img paths`: 상품의 상세 이미지들의 경로
  * 그 외에 브랜드 정보, 용량, 무게 정보 등이 있음.
* [Code version 1.0](./tutorial/4_coupang_imgs/4_main.py) 
  * Custom Templates
    * [data_revise](./tutoal/4_coupang_imgs/templates/data_revise.html) 
    * [show entries](./tutoal/4_coupang_imgs/templates/show_entries.html) 
  * Pipeline Flow: [Link](./tutorial/4_coupang_imgs/coupang_data_admin_page_1st.pdf) 
* [Code version 2.0](./tutorial/5_coupang_imgs/5_main.py) 
  * version 1.0 대비 페이지를 더 세분화 시켰다.
  * Custom Templates
    * [just view page for selected data](./tutoal/5_coupang_imgs/templates/just_view_for_selected_data.html) 
    * [login page](./tutoal/5_coupang_imgs/templates/login.html) 
    * [show page for revised data](./tutoal/5_coupang_imgs/templates/show_revised_data.html) 
    * [show page for revising data](./tutoal/5_coupang_imgs/templates/show_revising_data.html) 
    * [show page for selectable elements](./tutoal/5_coupang_imgs/templates/show_selectable_elements.html) 
  * Pipeline Flow: [Link](./tutorial/5_coupang_imgs/coupang_data_admin_page_2nd.pdf) 
