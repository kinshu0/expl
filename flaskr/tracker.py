from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from flask import send_file, request

bp = Blueprint('tracker', __name__)

# @bp.route('/')
# def index():
#     db = get_db()
#     posts = db.execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' ORDER BY created DESC'
#     ).fetchall()
#     return render_template('blog/index.html', posts=posts)

@bp.route('/')
def hello():
    return 'NSUT L 404 NOT FOUND'

@bp.route('/view')
@login_required
def index():
    db = get_db()
    trackers = db.execute(
        'SELECT t.id, target_name, created, author_id, username'
        ' FROM tracker t JOIN user u ON t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    z = trackers[0]['id']
    b = db.execute(
            'SELECT l.ip_address, accessed'
            '  FROM email_log l WHERE l.tracker_id = ?'
            '  ORDER BY accessed DESC', (z,) 
        ).fetchall()
    l = str(b)
    d = {
        tracker: db.execute(
            'SELECT l.ip_address, accessed'
            '  FROM email_log l WHERE l.tracker_id = ?'
            '  ORDER BY accessed DESC', (tracker['id'],) 
        ).fetchall()
        for tracker in trackers
    }

    return render_template('tracker/index.html', trackers=d)
    # return render_template('blog/index.html', trackers=trackers)



@bp.route('/create', methods=('GET', 'POST'))
# @login_required
def create():
    if request.method == 'POST':
        target_name = request.form['target_name']
        # body = request.form['body']
        error = None

        if not target_name:
            error = 'Target Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tracker (target_name, author_id)'
                ' VALUES (?, ?)',
                (target_name, g.user['id'])
            )
            db.commit()
            return redirect(url_for('tracker.index'))

    return render_template('tracker/create.html')


@bp.route('/l/<int:id>')
def log_email(id):
    if id:
        db = get_db()
        db.execute(
            'INSERT INTO email_log (ip_address, tracker_id)'
            'VALUES (?, ?)', (request.remote_addr, id)
        )
        db.commit()
        return send_file('static/whitep.jpg', mimetype='image/jpg')
    else:
        db = get_db()
        db.execute(
            'INSERT INTO email_log (ip_address, tracker_id)'
            'VALUES (?, ?)', (request.remote_addr, 0)
        )
        db.commit()
        return send_file('static/whitep.jpg', mimetype='image/jpg')



def get_tracker(id, check_author=True):
    post = get_db().execute(
        'SELECT t.id, target_name, created, author_id, username'
        ' FROM tracker t JOIN user u ON t.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_tracker(id)

    if request.method == 'POST':
        target_name = request.form['target_name']
        # body = request.form['body']
        error = None

        if not target_name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE tracker SET target_name = ?, body = ?'
                ' WHERE id = ?',
                (target_name, id)
            )
            db.commit()
            return redirect(url_for('target.index'))

    return render_template('tracker/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_tracker(id)
    db = get_db()
    db.execute('DELETE FROM tracker WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tracker.index'))