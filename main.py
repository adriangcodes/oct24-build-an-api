from flask import Flask
from init import db, ma
import os

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    
    db.init_app(app)
    ma.init_app(app)
    
    return app