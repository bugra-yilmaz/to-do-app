import sqlite3
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from tempfile import mkdtemp
from datetime import datetime
from flask_session import Session
from flask import render_template

from helpers import add_user
from helpers import get_todo_items
from helpers import login_required
from helpers import check_username_password

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, title TEXT NOT NULL, description TEXT, status TEXT NOT NULL, created_date TEXT NOT NULL, last_update_date TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))')


@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    to_do, in_progress, done = get_todo_items(cursor, user_id)

    return render_template('index.html', to_do=to_do, in_progress=in_progress, done=done)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        result, user_id = check_username_password(cursor, username, password)
        if result:
            session['user_id'] = user_id
            return redirect('/')
        return render_template('login-error.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        result, user_id = add_user(db, cursor, username, password)
        if result:
            session['user_id'] = user_id
            return render_template('index.html')   
        return render_template('register-error.html')
    else:
        return render_template('register.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        user_id = session['user_id']
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        created_date = last_update_date = datetime.now().strftime('%Y %B %d %A %H:%M:%S')

        if not title:
            return render_template('create-error.html', message='Please enter a title for your TO DO item.')

        cursor.execute(f"INSERT INTO todos (user_id, title, description, status, created_date, last_update_date) VALUES({user_id}, '{title}', '{description}', '{status}', '{created_date}', '{last_update_date}')")
        db.commit()

        return render_template('create-success.html', title=title)
    else:
        return render_template('create.html')


@app.route('/update')
@login_required
def update():
    item_id = request.args.get('id')
    status = request.args.get('status')
    last_update_date = datetime.now().strftime('%Y %B %d %A %H:%M:%S')

    cursor.execute(f"UPDATE todos SET status = '{status}', last_update_date = '{last_update_date}' WHERE id = {item_id}")
    db.commit()
    return redirect('/')


@app.route('/delete')
@login_required
def delete():
    item_id = request.args.get('id')

    cursor.execute(f"DELETE FROM todos WHERE id = {item_id}")
    db.commit()
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')


if __name__ == '__main__':
	app.run()
