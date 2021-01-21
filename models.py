from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    def __repr__(self):
        return f"<Role {self.name}:{self.description} />"


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='users=', lazy='dynamic')
    def __repr__(self):
        return f"<User {self.id}:{self.email} />"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text())
    post_image = db.Column(db.Text()) # Should be a url
    post_image_alt = db.Column(db.String(40)) # Should be a url
    created_date = db.Column(db.DateTime())
    updated_date = db.Column(db.DateTime())
    
    @property
    def attr(self):
        return self.user_id

    @attr.setter
    def attr(self, value):
        if hasattr(value, 'id'):
            self.user_id = value.id
        else:
            self.user_id = value

    def __repr__(self):
        return f"<Post {self.id}:{self.title} />"