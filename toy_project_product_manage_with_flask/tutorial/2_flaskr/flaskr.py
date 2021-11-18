# ================================================
# Step 2. 어플리케이션 셋업(Setup) 코드
# ================================================


# All the imports
from __future__ import with_statement  # python 2.x 를 사용한다.
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os

# Configuration
DATABASE = "/tmp/flaskr_db/flaskr.db"
DEBUG = True
# DEBUG = False
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "default"

# 실제 어플리케이션 생성 및 같은 파일의 설정을 가지고 어플리케이션 초기화
# ---------------------------------------
# Create our little application
app = Flask(__name__)

# Q. app.config.from_object(obj) ??
# A. 인자로 주어진 객체의 설정값을 읽어온다.
#     ( 인자가 문자열이면 해당 객체를 import 한다. )
#    그곳에 정의된 모든 대문자 변수를 찾는다.
app.config.from_object(__name__)


# 일반적으로 설정 파일에서 설정값을 로드하는 것이 좋은 생각이다.
# 아래와 같이 환경변수를 호출하여 설정값 로드도 가능하다.
# "FLASKR_SETTINGS" 에 명시된 설정 파일이 로드되면 기본 설정값들은 덮어쓰기가 된다.
# ---------------------------------------
# app.config.from_envvar("FLASKR_SETTINGS", silent=True)

# 운영시스템에서 디버그 모드는 반드시 비활성화 해야한다.
#  - 디버그 모드에서는 사용자가 서버의 코드를 실행할 여지가 있기 때문

# 명세화된 데이터베이스에 쉽게 접속할 방법을 추가한다.
# 이 방법으로 python 인터랙티브 쉘이나 스크립트에서 요청에 의한 커넥션을 얻을 수 있다.
def connect_db():
    db_path = app.config['DATABASE']
    db_path_split = db_path.split("/")
    db_dir_path = "/".join(db_path_split[:-1])
    if not os.path.exists(db_dir_path):
        os.makedirs(db_dir_path)
    return sqlite3.connect(app.config['DATABASE'])


# 단독 서버로 실행되는 애플리케이션을 위한 서버 실행 코드를 추가한다.
# if __name__ == "__main__":
#     app.run()
#     pass


# 아직까지는 아무런 뷰(view)를 만들지 않았으므로
# 브라우저에서는 404에러를 보게된다.
#
# 먼저, 데이터베이스가 잘 작동되는지 확인한다.


# ================================================
# Step 3. 데이터베이스 생성하기
# ================================================
# 1. 터미널에서 다음의 명령어 실행
#    >> sqlite3 db_path < schema.sql
#    ( 해당 방법은 sqlite3 명령어가 필요하고 경로문제도 발생할 수 있다. )
# 2. 데이터베이스를 초기화하는 함수를 추가한다.
# from __future__ import with_statement  # python 2.x 를 사용한다.
# from contextlib import closing


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('./schema.sql') as f:
            # open_resource(sql_path) : 리소스 경로의 파일을 열고 그 값을 읽을 수 있다.
            db.cursor().executescript(f.read().decode("utf-8"))
        db.commit()


# ================================================
# Step 4. 데이터베이스 커넥션 요청하기
# ================================================
@app.before_request
def before_request():
    # 파라미터가 없는 `before_request()` 함수는
    # 리퀘스트가 실행되기 전 호출되는 함수이다.
    # 즉, 리퀘스트 실행 전, DB와 연결한다.
    # -------------------------------------------------------
    # `after_request()` 함수는 리퀘스트 실행 이후 호출되는 함수로
    # 클라이언트에게 전송된 응답(response)를 파라미터로 넘겨줘야한다.
    # 이 함수들은 반드시 사용된 response 객체 혹은 새로운 response 객체를 리턴해야함.
    # 이 함수들은 response 객체 생성 이후 호출된다.
    # 이 함수들은 request 객체를 수정할 수 없고 리턴 값들은 무시된다.
    # 만약 리퀘스트 진행중 예외 발생 시, 해당 리퀘스트는 다시 각 함수들에게 전달된다.
    # 그렇지 않을 경우, None 이 전달된다.
    # -------------------------------------------------------
    # `g` 객체 : 각 함수들에 대해 오직 한번의 리퀘스트에 대한 유효한 정보를 저장한다.
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    # 예외상황은 `teardown_request()` 로 전달된다.
    g.db.close()


# ================================================
# Step 4. 데이터베이스 커넥션 요청하기
# ================================================
# 1. 작성된 글 보여주기
@app.route("/")
def show_entries():
    cur = g.db.cursor()
    cur.execute("SELECT title, text FROM entries ORDER BY id DESC")
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("show_entries.html", entries=entries)


# 2. 새로운 글 추가하기
@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401)
    g.db.execute("INSERT INTO entries (title, text) VALUES (?, ?)",
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash("New entry was successfully posted.")
    return redirect(url_for("show_entries"))


# 3. 로그인과 로그아웃
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash("You were logged in")
            return redirect(url_for("show_entries"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("show_entries"))


if __name__ == "__main__":
    # db가 실존하지 않는 경우, db를 초기화하는 코드를 실행
    if not os.path.exists(app.config["DATABASE"]):
        init_db()
    app.run()



# ================================================
# 표준 컨텍스트 (전역 변수)
# ================================================
# 1. config : 현재 설정값을 가진 객체
# 2. request : 현재 요청된 객체 (템플릿 활성화 이후 요청되어야함)
# 3. session : 현재 가지고 있는 세션 객체 (템플릿 활성화 이후 요청되어야함)
# 4. g : 요청에 한정된 전역 변수 (템플릿 활성화 이후 요청되어야함)
# 5. url_for()
# 6. get_flashed_messages()


# ================================================
# 자동변환(auto escaping) 제어
# ================================================
# 1. 자동변환 : HTML 에서 `&, <, >, ", '`등의 특수문자를 변환시키는 개념
# 2. 해당 문자들을 그대로 사용하려면 `entitles` 값으로 변환해야한다.
# 3. 템플릿에서 자동변환 비활성화 방법
#   3.1. HTML 문자열을 Markup 객체를 통해 템플릿에 전달하기 전 래핑한다.
#   3.2. 템플릿 내부에 `|safe` 필터를 명시적으로 사용한다.
#   3.3. 일시적으로 모두 자동변환 시스템을 해제한다.
#        ( `{% autoescape %}` 블럭을 사용한다. )
# 4. 자동변환 비활성화의 필요성
#   4.1. 명시적으로 HTML 을 페이지에 삽입하려는 경우


# ================================================
# 필터 등록하기
# ================================================
# 1. 필터 직접 등록 방법
#   1.1. `jinja_env` 이용         (Jinja 어플리케이션)
#   1.2. `template_filter()` 이용 (테코레이터)
# 2. 함수이름을 필터이름으로 사용하는 경우
#   2.1. 테코레이터의 아규먼트는 선택조건이어야한다.
#   2.2. 필터 등록후, jinja2 의 내장 필터를 사용하는 것과 똑같이 사용할 수 있다.
# 3. 사용 예
#   {% for x in mylist | reverse %}
#   {% endfor %}
# ================================================
# @app.template_filter("reverse")
# def reverse_filter(s):
#     return s[::-1]
#
#
# def reverse_filter(s):
#     return s[::-1]
# app.jinja_env.filters['reverse'] = reverse_filter


# ================================================
# 컨텍스트 프로세서 (context processor)
# ================================================
# 1. 컨텍스트 프로세서들은 새로운 값들을 템플릿 컨텍스트에 주입시키기 위해
#    템플릿이 렌더링되기 전에 실행되어야 한다.
# ================================================
# @app.context_processor
# def inject_user():
#     # 컨텍스트 프로세서는 user 라고 부르는 유효한 변수를
#     # 템플릿 내부에 g.user 의 값으로 만든다.
#     return dict(user=g.user)


# 아래의 컨텍스트 프로세서는 format_price 함수를 모든 템플릿들에서 사용할 수 있게 해준다.
# (사용 예.) {{ format_price(0.33) }}
# @app.context_processor
# def utility_processor():
#     def format_price(amount, currency=u"€"):
#         return u'{0:.2f}{1}'.format(amount, currency)
#     return dict(format_price=format_price)

