# Flask 어플리케이션 테스트하기 !
# ------------------------------------------
# 1. Flask 는 Werkzeug 를 통해 테스트 `Client`를 제공하여
#    어플리케이션의 컨텍스트 로컬을 처리하고 테스트 방법 제공.
# 2. 여기서는 python 에서 기본 제공하는 `unittest`를 사용.


# 테스팅 스켈레톤 (Skeleton)
# ------------------------------------------
import os
import flaskr
import unittest
import tempfile


# 테스트 함수들의 이름은 `test`로 시작한다.
#   -> 이를 활용하여 `unittest`에서 테스트를 수행할 함수를 자동적으로 식별한다.
class FlaskrTestCase(unittest.TestCase):

    # 1. 새로운 테스트 클라이언트 생성 및 새로운 데이터베이스를 초기화.
    # 2. 각 테스트 함수 실행 전에 먼저 호출된다.
    # 3. 아래 함수 실행 동안, `TESTING` 플래그가 활성화된다.
    # 4. 테스트 클라이언트의 어플리케이션에 대한 인터페이스
    #   4.1. 어플리케이션에 테스트 요청 실행
    #           -> 테스트 클라이언트는 테스트를 위해 쿠키를 놓치지 않고 기록
    def setUp(self):
        # 1. tempfile.mkstemp() 함수의 역할
        #   1.1. 로우-레벨 파일핸들과 임의의 파일이름을 리턴한다.
        #   1.2. 임의의 파일이름 -> 데이터베이스 이름
        #   1.3. db_fd 라는 파일 핸들을 `os.close()`함수를 사용하여 파일을 닫기 전까지 유지한다.
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()  # 우선 SQLite3 에서 유효
        self.app = flaskr.app.test_client()
        # flaskr.app.config['TESTING'] = True
        flaskr.init_db()

    # 테스트후 데이터베이스를 삭제하기 위해
    # 아래의 함수에서 파일을 닫고 파일시스템에서 제거한다.
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    # 어플리케이션 루트(`/`)로 접근시 어플리케이션이
    # "No entries here so far"을 보여주는지 확인한다.
    def test_empty_db(self):
        rv = self.app.get('/')
        # TypeError: a bytes-like object is required, not 'str'
        # ------------------------------------------
        # 1. Bytes Object
        #   1.1. string.encode() : str -> byte stream [ 역변환 : string.decode() ]
        #   1.2. b"string"
        assert b'No entries here so far' in rv.data

    # 입력과 출력로깅
    # ------------------------------------------
    def login(self, username, password):
        data = {
            "username": username,
            "password": password
        }
        return self.app.post("/login",
                             data=data,
                             follow_redirects=True)

    def logout(self):
        return self.app.get("/logout",
                            follow_redirects=True)

    # 테스트 클라이언트에서 어플리케이션의 입출력에 대한 로그를 기록한다.
    def test_login_logout(self):
        rv = self.login("admin", "default")
        assert b"You were logged in" in rv.data
        rv = self.logout()
        assert b"You were logged out" in rv.data
        rv = self.login("admin", "defaultX")
        assert b"Invalid password" in rv.data
        rv = self.login("adminX", "default")
        assert b"Invalid username" in rv.data
        rv = self.login("adminX", "defaultX")
        assert b"Invalid username" in rv.data

    # 메시지 추가 테스트
    def test_messages(self):
        self.login("admin", "default")
        data = dict(
            title='<Hello>',
            text="<strong>HTML</strong> allowed here"
        )
        rv = self.app.post("/add",
                           data=data,
                           follow_redirects=True)
        assert b"No entries here so far" not in rv.data
        assert b"&lt;Hello&gt;" in rv.data
        assert b"<strong>HTML</strong> allowed here" in rv.data


if __name__ == '__main__':
    unittest.main()

# 다른 테스팅 기법들
# ------------------------------------------
# 1. with app.test_request_context():
#     -> `request`, `g`, `session`와 같은 뷰 함수들에서 사용하는 객체에 접근한다.
# 2. app.preprocess_request() 메서드로 before_request()를 직접 호출해야한다.
# 3. app.preprocess_request(response) 메서드로 after_request()를 직접 호출해야한다.


# 컨텍스트 유지하기
# ------------------------------------------
# 1. with app.test_client() as test_client:


# 세션에 접근하고 수정하기
# ------------------------------------------
# 1. 테스트 클라이언트에서 세션에 접근하고 수정하는 일
#   1.1. flask.session : 세션이 특정 키 값으로 설정되있고 그 값이 컨텍스트를 통해 유지되고 접근 가능한 경우
# ------------------------------------------
# with app.test_client() as test_client:
#     rv = test_client.get("/")
#     assert flask.session['foo'] == 42
# ------------------------------------------
# with app.test_client() as test_client:
#     with test_client.session_transaction() as sess:
#         sess['a_key'] = 'a_value'
    # Once this is reached, the session was stored.

