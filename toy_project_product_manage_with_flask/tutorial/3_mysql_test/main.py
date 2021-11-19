from flask import Flask, g, render_template, redirect, url_for
import pymysql
# import numpy as np

##########################
#  Config
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "admin"
##########################


app = Flask(__name__)
app.config.from_object(__name__)


####################
# before request ! 
@app.before_request
def before_request():
    g.db = init_db()


@app.teardown_request
def teardown_request(exception):
    print(str(exception))
    g.db.close()


@app.route("/")
def show_entries():
    # cursor = g.db.cursor(pymysql.cursors.DictCursor)
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM ewg_test_table")
    # return "anything"
    return str(cursor.fetchall())


@app.route("/success")
def submit_click():
    return "success"


def init_db():
    return pymysql.connect(user="root",
                           passwd="DKrmemf!@34",
                           host="localhost",
                           db="ewg_db_test",
                           port=3306,
                           charset="utf8")


def create_and_run_app():
    with app.app_context():
        init_db()
    app.run()


if __name__ == "__main__":
    create_and_run_app()


