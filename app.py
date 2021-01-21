import os
from flask import Flask, render_template, send_from_directory
from flask_migrate import Migrate
from models import db, User, Role, Post
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from configs import get_config
from flask_security import Security, SQLAlchemyUserDatastore, login_required

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgresdev:password@localhost:5432/flask'
# db = SQLAlchemy()

@app.route('/')
def home_page():
    posts = db.session.query(Post).all()
    print(posts)
    return render_template('home.html', posts=posts)

@app.route('/demo')
def demo_page():
    import ipdb; ipdb.set_trace()
    return ''


@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory('node_modules', filename)

@app.cli.command("db:create")
def create_database():
    app.config.from_object(get_config())
    db.init_app(app)
    db.create_all()
    print('Database Created')


@app.cli.command("db:drop")
def drop_database():
    app.config.from_object(get_config())
    db.init_app(app)
    db.drop_all()
    print('Database Dropped')

@app.cli.command('db:migrate')
def migrate_database():
    app.config.from_object(get_config())
    db.init_app(app)
    Migrate(app, db)

@app.cli.command('db:seed')
def seed_database():
    app.config.from_object(get_config())
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    user_datastore.create_user(email='larry@cherry.com', password='password')
    user = db.session.query(User).first()
    post = Post()
    post.user = user
    post.title = "Test Title"
    post.content = 'This is the post content.'
    post.post_image = 'https://source.unsplash.com/random'
    post.post_image_alt = 'Unsplashed Image'
    db.session.add(post)
    db.session.commit()

# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='matt@nobien.net', password='password')
#     db.session.commit()

if __name__ == "__main__":
    print('__name__', __name__)
    print('*' * 80,'\nIf running in production make sure to set FLASK_ENV to production\n' + '*' * 80)
    flask_env = os.getenv('FLASK_ENV')
    app.config.from_object(get_config())
    os.environ['FLASK_ENV'] = 'development'
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    app.run()

    
