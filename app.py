import sqlite3
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from tempfile import mkdtemp

from helpers import login_required, add_user, check_username_password

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")

@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        result, user_id = check_username_password(cursor, username, password)
        if result:
            session['user_id'] = user_id
            return render_template("index.html")
        return render_template("login-error.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        result, user_id = add_user(db, cursor, username, password)
        if result:
            session['user_id'] = user_id
            return render_template("index.html")   
        return render_template("register-error.html")
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect('/')


if __name__ == '__main__':
	app.run()
