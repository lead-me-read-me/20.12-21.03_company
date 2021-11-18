import pymysql
import pandas as pd
import re
from flask import Flask, g, render_template, request, session, flash, redirect, url_for, abort

###########################
# config
DEBUG = True
USERNAME = "admin"
PASSWORD = "888"
SECRET_KEY = "development key-_"
###########################


app = Flask(__name__)
app.config.from_object(__name__)

init_table_name = "coupang_product_table"
table_name_for_selected_datas = "selected_datas_table"

# #####################################
# customized exception
# class NoElementException(Exception):
#     def __init__(self, alert_message):
#         super().__init__(alert_message)
# #####################################


# Connect to coupang_product_db
def connect_db():
    return pymysql.connect(host="localhost",
                           db="coupang_product_db",
                           user="root",
                           password="DKrmemf!@34",
                           port=3306,
                           charset="utf8")


# Initialize db
def init_db():
    with connect_db() as db:
        with db.cursor() as cursor:
            try:
                create_table(init_table_name)
            except:
                pass
            finally:
                cursor.execute("SELECT * FROM {}".format(init_table_name))
                datas_from_db_table = cursor.fetchall()

                if not datas_from_db_table:
                    path_to_csv = "/home/seunghun/문서/baby_lab/source_code/crawling/coupang_baby_product/crawled_data/backup_dry_tissue_page8.csv"
                    df = pd.read_csv(path_to_csv)
                    for col in df.columns:
                        df[col] = df[col].apply(lambda x: "" if str(x) == "nan" else str(x))

                    df2numpy = df.to_numpy()
                    df2numpy2list = []
                    for data in df2numpy:
                        df2numpy2list.append(data.tolist()[2:])

                    sql = \
                        """
                        INSERT INTO {} (id, code, name, brand_name, hash_tag, star, star_count, weight, ml, product_count, price, date, flag, ingredient_name, view, product_img_path, product_detail_img_paths, product_url)
                        VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """.format(init_table_name)
                    cursor.executemany(sql, df2numpy2list)
                    db.commit()
                cursor.close()


#############################
# before request
@app.before_request
def before_request():
    g.db = connect_db()
    with app.app_context():
        init_db()


#############################
# teardown_request
@app.teardown_request
def teardown_request(exception):
    g.db.close()
#############################


#############################
# views
#############################
@app.route("/admin")
def show_main():
    if not session.get("logged_in"):
        abort(401)
    datas = None
    with g.db.cursor() as cursor:
        cursor.execute("SELECT * FROM {}".format(init_table_name))
        datas = cursor.fetchall()
    return render_template("show_entries.html", datas=datas)


@app.route("/admin/success/delete", methods=['POST'])
def data_delete():
    if not session.get("logged_in"):
        abort(401)

    init_selected_datas = request.form.getlist("check")

    selected_ids = []
    for data in init_selected_datas:
        data = data[1:-1]
        data = re.split(", ", data)
        for idx, string in enumerate(data):
            data[idx] = string.strip().replace("'", "")
        selected_ids.append(data[0])

    with g.db.cursor() as cursor:
        delete_sql = \
            """
            DELETE FROM {} WHERE id = %s
            """.format(table_name_for_selected_datas)
        cursor.executemany(delete_sql, selected_ids)
        g.db.commit()
    return redirect(url_for("show_main"))


def create_table(table_name):
    create_sql = \
        """
        CREATE TABLE {} (
        id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
        code varchar(20),
        name varchar(200),
        brand_name varchar(20),
        hash_tag varchar(20),
        star varchar(20),
        star_count varchar(20),
        weight varchar(50),
        ml varchar(300),
        product_count varchar(50),
        price varchar(50),
        date varchar(30),
        flag varchar(20),
        ingredient_name varchar(200),
        view varchar(20),
        product_img_path varchar(200),
        product_detail_img_paths varchar(5000),
        product_url varchar(200)
        );
        """.format(table_name)
    with g.db.cursor() as cursor:
        cursor.execute(create_sql)
        g.db.commit()


def drop_table(table_name):
    drop_sql = \
        """
        DROP TABLE {};
        """.format(table_name)
    g.db.cursor().execute(drop_sql)
    g.db.commit()


@app.route("/admin/revising", methods=['POST'])
def data_revising():
    data_willbe_revised = request.form.getlist("revised_element")
    original_data = request.form.get("original_data")
    original_data = [string.strip().replace("'", "") for string in original_data[1:-1].split("', ")]

    selected_detail_img_paths = request.form.getlist("selected_detail_img")
    selected_detail_img_paths_to_string = ",".join(selected_detail_img_paths)

    revised_data = original_data[:]
    revised_data[1:] = data_willbe_revised
    for idx, element in enumerate(revised_data):
        if "detail" in element:
            revised_data[idx] = selected_detail_img_paths_to_string

    with g.db.cursor() as cursor:
        id = revised_data[0]
        data_delete_sql = \
            """
            DELETE FROM {} WHERE id={}
            """.format(table_name_for_selected_datas, id)
        cursor.execute(data_delete_sql)

        insert_sql = \
            """
            INSERT INTO {} (id, code, name, brand_name, hash_tag, star, star_count, weight, ml, product_count, price, date, flag, ingredient_name, view, product_img_path, product_detail_img_paths, product_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """.format(table_name_for_selected_datas)
        cursor.execute(insert_sql, revised_data)
        g.db.commit()
        cursor.close()

    return redirect(url_for("data_select_success"))


@app.route("/admin/before_revise", methods=['GET', 'POST'])
def show_revised_page_for_selected_data():
    if not session.get('logged_in'):
        abort(401)
    data_willbe_revised = request.form.get("button_for_revise")
    data = re.split(", ", data_willbe_revised[1:-1])
    data = [element.replace("'", "").strip() for element in data]

    return render_template('data_revise.html', datas=data)


@app.route("/admin/success", methods=['GET', 'POST'])
def data_select_success():
    if not session.get("logged_in"):
        abort(401)

    init_selected_datas = request.form.getlist("check")

    selected_datas = []
    for data in init_selected_datas:
        if " , " in data:
            data = data.replace(" , ", ",")
        data = [string.strip().replace("'", "") for string in data[1:-1].split(", ")]
        selected_datas.append(data)

    selected = None
    # 테이블 없으면 생성
    with g.db.cursor() as cursor:
        try:
            create_table(table_name_for_selected_datas)
        except Exception as e:
            print(str(e))
        finally:
            try:
                create_table("tmp")
            except Exception as e:
                print(str(e))
                drop_table("tmp")
                create_table("tmp")
            finally:
                insert_sql = \
                    """
                    INSERT INTO {} (id, code, name, brand_name, hash_tag, star, star_count, weight, ml, product_count, price, date, flag, ingredient_name, view, product_img_path, product_detail_img_paths, product_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """.format("tmp")
                cursor.executemany(insert_sql, selected_datas)

            alter_sql = \
                """
                ALTER TABLE {} RENAME {};
                """.format(table_name_for_selected_datas, table_name_for_selected_datas+"_tmp")
            try:
                cursor.execute(alter_sql)
            except Exception as e:
                print(str(e))
                drop_table(table_name_for_selected_datas+"_tmp")
                cursor.execute(alter_sql)

            union_sql = \
                """
                SELECT * FROM {}
                UNION
                SELECT * FROM tmp
                WHERE id NOT IN (SELECT id FROM {});
                """.format(table_name_for_selected_datas+"_tmp", table_name_for_selected_datas+"_tmp")
            cursor.execute(union_sql)
            try:
                datas = cursor.fetchall()

                drop_table("tmp")
                drop_table(table_name_for_selected_datas+"_tmp")

                create_table(table_name_for_selected_datas)
                insert_sql = \
                    """
                    INSERT INTO {} (id, code, name, brand_name, hash_tag, star, star_count, weight, ml, product_count, price, date, flag, ingredient_name, view, product_img_path, product_detail_img_paths, product_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """.format(table_name_for_selected_datas)
                cursor.executemany(insert_sql, datas)
                g.db.commit()

                select_sql = \
                    """
                    SELECT * FROM {};
                    """.format(table_name_for_selected_datas)
                cursor.execute(select_sql)
                selected = cursor.fetchall()
            except Exception as e:
                print(str(e))
                pass

    return render_template("show_entries.html", datas=selected)


@app.route("/", methods=['GET', 'POST'])
def before_login():
    return render_template('show_entries.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username!"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid password"
        else:
            session['logged_in'] = True
            flash("login success")
            return redirect(url_for("show_main"))
    return render_template("show_entries.html", error=error)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("logged_in", None)
    flash("logged out!")
    return redirect(url_for("before_login"))
#############################


#############################
# template_filter()
#############################
@app.template_filter("to_string")
def to_string(any_element):
    return str(any_element)


@app.template_filter("split_by_comma")
def split_by_comma(file_paths):
    result = file_paths.split(",")
    return result
#############################


if __name__ == "__main__":
    app.run()

