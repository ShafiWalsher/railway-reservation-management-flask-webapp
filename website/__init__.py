from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
# from flask_mysqldb import MySQL

# DB Object
db = SQLAlchemy()
# Migrate Object
migrate = Migrate()

# Database Name
DB_NAME = "ARDatabase.db"
# MYSQL PASSWORD toor123

def create_app():
    app = Flask(__name__)
    # Secrete Key
    app.config['SECRETE_KEY'] = 'my super secret key'
    # Config Database
    # Sqlite DB URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # MySQL DB URI
    # mysql://username:password@server/db
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:@127.0.0.1/aincraddb'
    
    # DB Object instanciate
    db.init_app(app)

    # Initialize Flask Migrate
    migrate.init_app(app, db)

    # Register created Blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    # Defining database models & Creating Dataase
    from .models import User,Train,Ticket,Station,Feedback
    create_database(app)

    # Initiate LoginManager
    login_manager = LoginManager()
    # redirect if not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # loading user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int (id))

    return app


# Function to create databse if not exists
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database is Created!')