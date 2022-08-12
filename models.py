"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

def connect_db(app):
    """Establishes the connection"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users can create posts and give them tags"""
    __tablename__ = 'users'

    def __repr__(self):
        return f"<User {self.id} {self.full_name} {self.image_url}>"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                    nullable=False)

    last_name = db.Column(db.String(50),
                    nullable=False)

    image_url = db.Column(db.String(150),
                    nullable=True)
    posts = db.relationship('Post', back_populates='user', cascade="all, delete", passive_deletes=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    """Posts have a title and content and can be tied to tags"""
    __tablename__ = 'posts'

    def __repr__(self):
        return f""
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(50),
                    nullable=False)

    content = db.Column(db.String(500),
                    nullable=True)

    created_at = db.Column(db.DateTime, 
                    nullable=False, 
                    default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id', ondelete='CASCADE'))

    @property
    def created_f(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


    user = db.relationship('User', back_populates='posts')

class Tag(db.Model):
    """Tags in the pool"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text, nullable = False, unique = True)
    posts = db.relationship('Post', secondary='posts_tags', cascade="all,delete", backref="tags")

class PostTag(db.Model):
    """Connects tags to posts"""
    __tablename__ = 'posts_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)


