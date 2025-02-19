from flask import Blueprint
from init import db
from models.student import Student

db_bp = Blueprint('db', __name__)
# Commands need to be prefixed with the name of the group - in this instance, flask db init or flask db seed

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables created.')
    
@db_bp.cli.command('seed')
def seed_tables():
    students = [
        Student(
            name='Mary Jones',
            email='mary.jones@gmail.com',
            address='Sydney'
        ),
        Student(
            name='John Smith',
            email='johnsmith@outlook.com'
        )
    ]
    
    db.session.add_all(students)
    db.session.commit()
    print('Tables seeded.')