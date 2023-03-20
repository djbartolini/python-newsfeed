from flask import Blueprint, request, jsonify, session
import sys

from app.models import User, Post, Comment, Vote
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # post new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    # sqlalchemy INSERT statement
    db.add(newUser)
    # save in database
    db.commit()
  except:
    # sys module (built-in) to print error to console
    print(sys.exc_info()[0])
    # rollback (discard) last commit to prevent hung pending state
    db.rollback()
    # return error to frontend
    return jsonify(message = 'Validation Error'), 500

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = 'Email or password incorrect. Woopsie!'), 400

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Email or password incorrect. Woopsie!'), 400
  
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
def comment():
  data = request.get_json()
  db = get_db()

  try:
    # post new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    # sqlalchemy INSERT statement
    db.add(newComment)
    # save in database
    db.commit()
  except:
    # sys module (built-in) to print error to console
    print(sys.exc_info()[0])
    # rollback (discard) last commit to prevent hung pending state
    db.rollback()
    # return error to frontend
    return jsonify(message = 'Request failed, woopsie!'), 500

  return jsonify(id = newComment.id)

@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # post upvote using incoming id (post) and session if (user performing upvote)
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    # sqlalchemy INSERT statement
    db.add(newVote)
    # save in database
    db.commit()
  except:
     # sys module (built-in) to print error to console
    print(sys.exc_info()[0])
    # rollback (discard) last commit to prevent hung pending state
    db.rollback()
    # return error to frontend
    return jsonify(message = 'Request failed, woopsie!'), 500
  
  return '', 204

@bp.route('/posts', methods=['POST'])
def create():
  data = request.get_json()
  db = get_db()

  try:
    # post a blog-post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )
    # sqlalchemy INSERT statement
    db.add(newPost)
    # save in database
    db.commit()
  except:
    # sys module (built-in) to print error to console
    print(sys.exc_info()[0])
    # rollback (discard) last commit to prevent hung pending state
    db.rollback()
    # return error to frontend
    return jsonify(message = 'Request failed, woopsie!'), 500
  
  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # update post by id:
    # query post by id
    post = db.query(Post).filter(Post.id == id).one()
    # update post title
    post.title = data['title']
    # save in database
    db.commit()
  except:
    # sys module (built-in) to print error to console
    print(sys.exc_info()[0])
    # rollback (discard) last commit to prevent hung pending state
    db.rollback()
    # return error to frontend
    return jsonify(message = 'Post not found, woopsie!'), 404
  
  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
  db = get_db()

  try:
    # query post by id, delete post by id
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    # sys module (built-in) to print error to console
    print(sys.exc_info()[0])
    # rollback (discard) last commit to prevent hung pending state
    db.rollback()
    # return error to frontend
    return jsonify(message = 'Post not found, woopsie!'), 404
  
  return '', 204
