
# Flask 클래스를 임포트함
# ------------------------------------
#  - 이 클래스의 인스턴스가 우리 WSGI(Web Server Gateway Interface)
#    어플리케이션이 된다.
from flask import Flask, url_for, render_template, Markup, request, make_response, abort, redirect, escape, session
from werkzeug.contrib.fixers import LighttpdCGIRootFix


# 클래스 생성자
# ------------------------------------
#  - 첫번째 인자 : 어플리케이션의 이름 (단일 모듈 사용시, __name__ 을 이용한다.)
#                 어플리케이션으로 시작하는지 혹은 모듈로 임포트되는지에 따라 이름이 달라짐.
#                 모듈이나 패키지 이름을 인자로 -> 템플릿이나 정적파일을 찾을때 필요하다.
app = Flask(__name__)

# @app.route(url)
# ------------------------------------
#  - `route()` 데코레이터를 사용하여 Flask 에게
#      어떤 url 이 우리가 작성한 함수를 실행시키는지 알려준다.
#  - `route()` 데코레이터는 함수와 url 을 연결해준다.
@app.route('/')
def hello_world():
    return "<h1>Hello World!</h1>"


@app.route("/user/<username>")
def show_user_profile(username):
    # Show the user profile for that user.
    return "User {}".format(username)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # Show the post with the given id, the id is an integer.
    return "Post {}".format(post_id)


@app.route("/projects/")
def projects():
    # 파이썬 코드
    return "The project page"


@app.route("/about")
def about():
    return "The about page"

# HTTP 메서드
# ---------------------------------
#  - HTTP 는 URL 접근에 몇가지 방식을 제공한다. (기본적으로 get)
#  - get, post
# ---------------------------------
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

# url 생성
# ---------------------------------
# 1. flask.url_for(...) : 라우팅이 설정된 함수의 url 을 얻는 함수
# 2. Flask.test_request_context() : Flask 에게 현재 파이썬 쉘에서 테스트를 하고 있음에도
#    (문맥 관리자, context manager)   지금 실제로 요청을 처리하고 있는것 처럼 상황을 제공
with app.test_request_context():
    print(url_for("about"))
    print(url_for("projects"))
    print(url_for("projects", next="/"))
    print(url_for("show_user_profile", username="seunghun"))

with app.test_request_context('/hello', method="POST"):
    # 방법 1.
    # Now, we can do something with the request
    # until the end of thd "with" block, such as basic assertions
    assert request.path == "/hello"
    assert request.method == "POST"

# with app.request_context(environ=environ):
    # 방법 1.
    # assert request.method == "POST"

# Q. 키워드 `assert` 는 무엇?
# A. 0. 사용목적 : 디버깅
#    1. 사용형식 : `assert condition, message`
#    2. 작동방식 : condition 이 True 이면 pass, False 이면 message 출력 후 프로그램 종료
#                 ( AssertionError )

# Q. 왜 템플릿에 url 을 하드코딩하지 않고 url 을 얻어내야하나?
# A1. url 역변환이 하드코딩보다 설명적이다. (또, 한번에 url 을 모두 변경할 수 있다.)
# A2. url 을 얻어내는 것은 특수 문자 및 유니코드 데이터들에 대한 이스케이핑을 명확하게 해준다.
# A3. 작성한 어플리케이션이 url 의 최상위 바깥에 위치한다면, (ex. `/` 대신 `/myapplication`)
#      url_for() 함수가 그 위치를 상대위치로 적절하게 처리해준다.

# Q. 이스케이핑(escaping)이란?
# A. HTML 태그 자체를 화면에 표시하는것.
#    (ex. `<br/>` -> `&lt;br/&gt;`)


# 템플릿 보여주기
# ---------------------------------
# 1. 보안상 동적으로 변환되는 값에 대해 이스케이핑을 일일이 작성해야한다.
# 2. Flask 에서는 jinja2 를 템플릿 엔진으로 구성하여 자동으로 HTML 이스케이핑을 한다.
# 3. `render_template(템플릿이름, 템플릿에 보여줄 변수)` : 템플릿을 뿌려주는 메서드
# ---------------------------------
# ! Flask 는 templates 폴더에서 템플릿을 찾는다. !
# ---------------------------------
# Case 1. 모듈:
# /application.py
# /templates
#     /hello.html
#
# Case 2. 패키지:
# /application
#     /__init__.py
#     /templates
#         /hello.html
@app.route("/hello/")
@app.route("/hello<name>")
def hello(name=None):
    return render_template("hello.html", name=name)
# 템플릿 예제 ... name 을 부어서 최종 html 소스 코드를 얻는다.
# ---------------------------------
# <!doctype html>
# <title>Hello from Flask</title>
# {% if name %}
#   <h1>Hello {{ name }}!</h1>
# {% else %}
#   <h1>Hello World!</h1>
# {% endif %}


if __name__ == '__main__':
    # - run() 메서드를 사용해 어플리케이션을 로컬서버로 실행한다.
    # - 현재는 네트워크상의 다른 컴퓨터에서 접근 불가 상태임
    #    -> 디버그 모드상에서 어플리케이션의 사용자가 임의의 파이썬 코드를 실행할 수 있기 때문
    #    1. 디버그 모드를 해제
    #    2. app.run(host='0.0.0.0') <- 이 경우, 네트워크상의 사용자를 신뢰한다는 가정이 필요.
    #           (2.)의 변경으로 OS로 하여금 모든 public IP를 접근가능도록 설정한다.
    app.run()

# 디버그 모드
# ---------------------------------
# 1. app.debug = True
#    app.run()
#
# 2. app.run(debug=True)


# 정적파일
# ---------------------------------
#  - 동적인 웹 어플리케이션은 정적 파일을 필요로한다. (보통 javascript 나 css 파일을 의미)
#  - 웹 서버가 정적 파일을 서비스하는게 이상적이나 개발시에는 Flask 가 그 역할을 대신한다.
#  - static 이라는 폴더를 패키지 아래에 만들거나 모듈 옆에 위치시키면
#    개발된 어플리케이션에서 `/static` 위치에서 정적 파일을 제공한다.
#
# url_for('static', filename="style.css")


# Markup 클래스 사용 예제
markup = Markup("<strong>Hello %s!</strong>" % "<blink>hacker</blink>")
print(markup)
print(markup.escape("<blink>hacker</blink>"))

markup_striptags = Markup("<em>Marked up</em> &raquo; HTML").striptags()
print(markup_striptags)


# 요청 데이터 접근하기
# ---------------------------------
#  - request(전역객체)가 클라이언트가 서버로 보내는 데이터 정보를 제공한다.
#  - 컨텍스트 로컬 : 위 객체가 어떻게 글로벌하고 쓰레드 안전하게 처리되는지에 대한 해답.
#  - 요청 메서드 : method 속성
#  - 폼 데이터 접근 : form 속성 ( http 의 POST 혹은 PUT 요청으로 전달된 데이터 )
#  - Query String 접근 : args 속성
#    ( ex. `?key=value` -> search_word = request.args.get('key', '') )

# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#
#         # 아래 코드는 요청이 GET 이거나, 인증정보가 잘못되었을 경우 실행됨
#     return render_template("login.html", error=error)

# 파일 업로드
# ---------------------------------
#  - HTML form 설정 : ` enctype="multipart/form-data" `
#  - 파일명 : filename 속성, secure_filename() 함수
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["the_file"]
        f.save("path/file_name.file_extension")


# 쿠키 ( Cookie )
# ---------------------------------
#  - 쿠키 접근 : request.cookies 속성,
#  - 쿠키 저장 : request.set_cookie()
@app.route('/')
def index_read():
    username = request.cookies.get("username")
    print(username)
    # User cookies.get(key) instead of cookies[key]
    # to not get a KeyError if the cookie is missing.


@app.route('/')
def index_store():
    #  - 쿠키는 response 객체에 저장된다.
    #  - make_response() 함수 : 문자열을 response 객체로 명시적으로 변환한다.
    #  - response 객체가 존재하지 않는 시점에 쿠키 저장 : 지연된(deferred) 요청 콜백 패턴 사용
    response = make_response(render_template("url"))
    response.set_cookie('username', 'the username')
    return response


# 페이지 전환 기능
# ---------------
# 1. 왜? : 현재 작업중인 페이지에서 다른 페이지로 이동하기 위해서.
# 2. 전환 방법 2가지
#   2.1. Forward 방식
#       - Web Container 차원에서 페이지의 이동만 존재한다.
#       - 실제로 웹 브라우저는 다른 페이지로 이동했음을 알 수 없다.
#         ( 웹 브라우저에서는 최초에 호출한 url 만 표시되고
#           이동한 페이지의 url 정보는 확인할 수 없다.     )
#       - 현재 실행중인 페이지와 Forward 에 의해 호출된 페이지는
#         request 객체와 response 객체를 공유한다.
#
#   2.2. Redirect 방식
#       - 웹 브라우저는 url 을 지시된 주소로 바꾸고 해당 주소로 이동한다.
#       - 다른 웹 컨테이너에 있는 주소로 이동하여 새로운 페이지에서는 request 와 response 객체가 새로 생성됨.
#       - 최초의 request 와 response 객체는 유효하지 않다.

# 리다이렉션과 에러
# ---------------------------------
#  - redirect() 함수 : 사용자를 다른 엔드포인트로 redirect(다시 지시) 시킴.
#  - abort() 함수 : 에러코드를 가지고 일찍 요청을 중단시킴.
#  - @app.errorhandler(error_code) : 에러페이지 변경
@app.route("/")
def index_redirect():
    return redirect(url_for("login_redirect"))


@app.route("/login_redirect")
def login_redirect():
    abort(401)


@app.errorhandler(404)
def page_not_found(error):
    # 페이지의 상태 코드가 그 페이지를 찾을 수 없다는 404가 되어야 함을 Flask 에 말해 준다.
    # (기본값은 200)
    return render_template("page_not_found.html", error=error), 404


# 응답에 관하여
# ---------------------------------
#  1. view 함수로부터 반환된 값은 자동으로 response 객체로 변환된다.
#    ( ex. 반환값이 문자열인 경우, response body 로
#          문자열과 `200 OK` 코드, `text/html` mimtype 을 갖는 response 객체로 변환됨.)
#  2. 객체 변환 규칙
#    2.1. 정확한 response 객체 반환 -> 그대로 뷰로부터 반환됨.
#    2.2. 문자열 반환 -> 해당 데이터와 기본 파라미터를 갖는 response 객체가 생성됨.
#    2.3. 튜플 반환 (response, status, header) -> status(status code), headers(추가적인 정보의 list 혹은 dictionary)
#    2.4. 그 외 : WSGI application 을 response 객체로 변환.
@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error=error), 404


@app.errorhandler(404)
def not_found(error):
    response = make_response(render_template('error.html', error=error), 404)
    response.headers['X-Something'] = 'A value'
    return response


# 세션 (session)
#  Q. 세션이란?
#  A. 반영구적이고 상호작용적인 정보 교환을 전제하는
#     둘 이상의 통신 장치나 컴퓨터와 사용자 간의
#     대화나 `송수신 연결상태를 의미`하는
#    `보안적인` 다이얼로그(dialogue) 및 시간대를 가리킨다.
#     (세션은 연결상태 유지보다 연결상태의 안정성을 더 중요시함.)
# ---------------------------------
# 1. 객체 `session` : 하나의 요청에서 다음 요청까지 사용자에 대한 구체적인 정보를 저장한다.
#   1.1. 세션은 쿠키위에서 구현되고 암호화를 사용하여 그 쿠키를 서명한다.
#        (즉, 사용자는 쿠키 내용은 읽을 수 있지만 비밀키 없이 쿠키 내용을 변경할 수 없다.)
# 2. 쿠키 기반의 session
#   2.1. 값들을 세션 객체 안에 넣고 세션 객체들을 쿠키로 직렬화한다.
#   2.2. 쿠키는 사용할 수 있는데 세션에 저장된 값들이
#        여러 요청에 걸처 지속적으로 사용할 수 없고 에러 메세지를 얻을 수 없는 경우,
#        웹 브라우저에 의해 지원되는 쿠키 크기와 응답 페이지 내의 쿠키 크기를 꼭 체크 !
app_session = Flask(import_name=__name__)

@app_session.route('/')
def index_session():
    if 'username' in session:
        return 'Logged in as %s.' % escape(session['username'])
    return 'You are not logged in.'


@app_session.route('/login', method=['GET', 'POST'])
def login_session():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username></input></p>
            <p><input type=submit value=login></input></p>
        </form>
    '''


@app_session.route("/logout")
def logout():
    # Remove the username from the session if it's there.
    session.pop('username', None)
    return redirect(url_for("index"))


# Set the secret key. Keep this really secret !
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"


# 메시지 플래싱
# ---------------------------------
#  - 피드백 : 좋은 어플리케이션과 유저 인터페이스의 핵심
#  - "flashing system" : 1. 사용자에게 피드백을 주는 방법
#                        2. 요청의 끝과 바로 다음 요청에 접근할 때 메세지를 기록을 허용하는 것.
#                           (레이아웃 템플릿과 조합되어 있음.)
#  - flash() 메서드
#  - get_flashed_messages() 메서드 : 메세지를 가져오기 위해 템플릿에서 사용할 수 있는 메서드
#
#  - 예제 참고 : https://flask-docs-kr.readthedocs.io/ko/latest/patterns/flashing.html#message-flashing-pattern


# 로깅 (logging)
# ---------------------------------
app.logger.debug("A value for debugging")
app.logger.warning("A warning occurred (%d apples)", 42)
app.logger.error("An error occurred")


# WSGI 미들웨어에서 후킹하기
# ---------------------------------
# 1. 내부 WSGI 어플리케이션 래핑 : 개발한 어플리케이션을 WSGI 미들웨어에 올리기
#    Ex. 아래는 lighttpd 버그를 피하기 위해 Werkzeug 패키지의 미들웨어 중 하나를 사용하는 예제
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)


# 웹 서버에 배포하기
# ---------------------------------
# 개발한 어플리케이션을 hosted 된 플랫폼에 배포할 수 있다.
