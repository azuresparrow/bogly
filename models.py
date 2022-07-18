"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
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
                    db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='posts')