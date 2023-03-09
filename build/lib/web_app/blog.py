from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from web_app.auth import login_required
from web_app.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')



@bp.route('/')
def index():
    """
    Renders the index page, it shows list of posts.
    Crud operations are allowed to the logged in user only.
    """
    db = get_db()
    sql_query = """
        select p.id, title, body, created, author_id, username from post p inner join user u on u.id=p.author_id order by created desc
    """
    posts = db.execute(sql_query).fetchall()
    print("Posts Data ", posts)
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """
    After validating the title and body, adding post in the database.
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """
    This function takes post id and check author flag.
    If check_author flag is True then it checks whether the current login user is the auther of the post or not.
    If yes then it returns the post detail of the given post id.
    If no post with the given post id then it returns 404 error.
    """
    db = get_db()
    sql_query = """
        select p.id, title, body, created, author_id, username from post p inner join user u on u.id=p.author_id and p.id=?
    """
    post = db.execute(sql_query, (id,)).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    After validating the title and body, updating post in the database.
    """
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """
    After validating the post id, deleting post from the database.
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

