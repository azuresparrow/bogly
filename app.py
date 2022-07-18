"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

""" USER ROUTES """
@app.route('/users')
def users_list():
    """ Show all users. """
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def users_form():
    """show an add form for users"""
    return render_template('user_new.html')

@app.route('/users/new', methods=["POST"])
def users_create():
    """Process the add form, adding a new user and going back to /users"""
    user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form['image_url'] or None)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:id>')
def user_detail(id): 
    """Show information about the given user.
    Have a button to get to their edit page, and to delete the user."""
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

@app.route('/users/<int:id>/edit')
def user_edit(id): 
    """Show the edit page for a user.
    Have a cancel button that returns to the detail page for a user, 
    and a save button that updates the user."""
    user = User.query.get_or_404(id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:id>/edit', methods=["POST"])
def user_save(id): 
    """Process the edit form, returning the user to the /users page."""
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name'] 
    user.last_name = request.form['last_name'] 
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route('/users/<int:id>/delete', methods=["POST"])
def user_delete(id): 
    """Delete the user."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

""" POST ROUTES """
@app.route('/users/<int:id>/posts/new')
def posts_form(id):
    user = User.query.get_or_404(id)
    """Show form to add a post for that user."""
    return render_template('post_new.html', user=user)

@app.route('/users/<int:id>/posts/new', methods=["POST"])
def posts_create(id):
    """Handle add form; add post and redirect to the user detail page."""
    post = Post(title=request.form['title'], content=request.form['content'], user_id=id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{id}')

@app.route('/posts/<int:id>')
def posts_detail(id):
    """ Show a post. """
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:id>/edit')
def post_edit(id): 
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(id)
    return render_template('post_edit.html', post=post, user=post.user)

@app.route('/posts/<int:id>/edit', methods=["POST"])
def posts_save(id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{id}')

@app.route('/posts/<int:id>/delete', methods=["POST"])
def post_delete(id): 
    """Delete the post."""
    post = Post.query.get_or_404(id)
    author_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{author_id}')

@app.errorhandler(404)
def page_missing(e):
    return render_template('404.html'), 404
