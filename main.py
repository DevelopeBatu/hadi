from flask_session import Session
from flask import Flask, request, render_template, redirect, session
import sqlite3
from sms import send

do = True

# Flask constructor
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":

        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        return iki(first_name,last_name)
    return render_template("index.html",do=do)

@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("fname")
        # getting input with name = lname in HTML form
        password = request.form.get("lname")
        a_password = request.form.get("aname")
        vt = sqlite3.connect('users.sqlite')
        im = vt.cursor()
        im.execute(f"SELECT * from users WHERE user_name = '{username}'")
        veriler = im.fetchall()
        if password == a_password and len(veriler)==0:
            im.execute(f"INSERT INTO users VALUES ('{username}','{password}','normal',0)")
            vt.commit()
            print("oldu")
            return render_template("go_login.html")
        else:
            do = False
            return render_template("register.html", do=False)

    return render_template("register.html",do=True)

@app.route("/anasayfa",methods=['GET', 'POST'])
def ana():
    if not session.get("username"):
        return redirect("/")
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        sonuc = send(phone_number,100,99)
        return render_template('anasayfa.html', phone_number=phone_number, sonuc=sonuc)

    return render_template("anasayfa.html")
do = True
@app.route("/iki")
def iki(username,password):
    vt = sqlite3.connect('users.sqlite')
    im = vt.cursor()
    print(username)
    print(password)
    im.execute(f"SELECT * from users WHERE user_name = '{username}' and password = '{password}'")
    veriler = im.fetchall()
    print(veriler)
    if len(veriler)>=1:
        session["username"] = username
        return render_template("iki.html")
    else:
        do=False
        return render_template("index.html", do=do)

@app.route("/adminsayfa", methods =["GET", "POST"])
def admin():
    vt = sqlite3.connect('users.sqlite')
    im = vt.cursor()
    im.execute(f"SELECT * from users")
    veriler = im.fetchall()
    return render_template("admin.html",veriler=veriler)

@app.route("/delete_user", methods =["GET", "POST"])
def delete():
    if request.method == "GET":
        user_name = request.args.get("deleteted_user")
        vt = sqlite3.connect('users.sqlite')
        im = vt.cursor()
        im.execute(f"DELETE from users WHERE user_name = '{user_name}'")
        vt.commit()
    return render_template("delete_users.html")

@app.route("/update_user", methods =["GET", "POST"])
def update_user():
    if request.method == "GET":
        user_name = request.args.get("updated_user")
        vt = sqlite3.connect('users.sqlite')
        im = vt.cursor()
        im.execute(f"SELECT * from users WHERE user_name = '{user_name}'")
        veriler = im.fetchall()
        return render_template("update.html",user_edit=veriler)
    return render_template("update.html")

@app.route("/update_save", methods =["GET", "POST"])
def update_save():
    if request.method == "GET":
        user_status = request.args.get("user_status")
        username = request.args.get("username")
        user_password = request.args.get("user_password")
        user_type = request.args.get("user_type")
        vt = sqlite3.connect('users.sqlite')
        im = vt.cursor()
        im.execute(f"UPDATE users set password='{user_password}', user_type='{user_type}', user_status='{user_status}' WHERE user_name='{username}'")
        vt.commit()
    return render_template("edit_go_user.html")


@app.route("/kaydet")
def kayıt():
    return render_template("kayıt.html")

if __name__=='__main__':
    app.run(debug=True)
