"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def users_list():
    """ Show all users. """
    users = User.query.order_by(User.last_name, User.first_name).all()
    print(users)
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
