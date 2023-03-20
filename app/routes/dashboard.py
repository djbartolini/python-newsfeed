from flask import Blueprint, render_template, session

from app.models import Post
from app.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def dash():
  # get all posts by user id
  db = get_db()
  posts = (
     db.query(Post)
      .filter(Post.user_id == session.get('user_id'))
      .order_by(Post.created_at.desc())
      .all()
  )

  # return page with data for posts and loggedIn (from session)
  return render_template(
    'dashboard.html',
    posts=posts,
    loggedIn=session.get('loggedIn')
  )

@bp.route('/edit/<id>')
def edit(id):
  # get a post by id
  db = get_db()
  post = (
    db.query(Post)
      .filter(Post.id == id)
      .one()
  )

  # return page with data for posts and loggedIn (from session)
  return render_template(
    'edit-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )
