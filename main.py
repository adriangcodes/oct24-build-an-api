from flask import Flask
from init import db, ma
from marshmallow.exceptions import ValidationError
from dotenv import load_dotenv
import os
from blueprints.db_bp import db_bp
from blueprints.students_bp import students_bp
from blueprints.teachers_bp import teachers_bp
from blueprints.courses_bp import courses_bp

def create_app():
    app = Flask(__name__)
    
    load_dotenv(override=True) # Required to override the local environment data link and send to cloud instead
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    
    db.init_app(app)
    ma.init_app(app)
    
    @app.errorhandler(ValidationError) # If a validation error happens anywhere in the application, this will be returned
    def validation_error(err):
        return {"error": str(err)}, 400
    
    app.register_blueprint(db_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)
    
    return app