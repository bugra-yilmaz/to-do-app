from flask import redirect, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function


def check_username_in_use(cursor, username):
	cursor.execute(f'SELECT * FROM users WHERE username = \'{username}\'')
	for row in cursor:
		return False
	return True


def check_username_password(cursor, username, password):
	cursor.execute(f'SELECT * FROM users WHERE username = \'{username}\'')
	for row in cursor:
		user_id = row[0]
		if check_password_hash(row[2], password):
			return True, user_id
	return False, None


def add_user(db, cursor, username, password):
	username_valid = check_username_in_use(cursor, username)
	if username_valid:
		print('Username valid.')
		password_hash = generate_password_hash(password)
		cursor.execute(f'INSERT INTO users (username, hash) VALUES(\'{username}\', \'{password_hash}\')')
		db.commit()
		cursor.execute(f'SELECT * from users WHERE username = \'{username}\'')
		for row in cursor:
			user_id = row[0]
		return True, user_id
	print('Username in use.')
	return False, None
