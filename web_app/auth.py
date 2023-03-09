import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, 
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from web_app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """
    This function will be called before the view function whenever a url is requested.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(current_function): # function on which this decorator is called
    """
    This is a decorator, it will be used to check a request is from the login user or not.
    """
    @functools.wraps(current_function) # this decorator helps to keep indentity of current function
    def wrapper_view(**kwargs): # current function args and kwargs
        if g.user is None:
            return redirect(url_for('auth.login'))
        return current_function(**kwargs)
    return wrapper_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if username and password:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    On login request, validate user credentials and store user id in the session.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))
        print(error)
        flash(error)

    return render_template('auth/login.html')



@bp.route('/logout')
def logout():
    """
    On logout request, remove user id by clearing the session.
    """
    session.clear()
    return redirect(url_for('blog.index'))
