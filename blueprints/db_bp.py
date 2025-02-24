from flask import Blueprint
from init import db
from datetime import date
from models.student import Student
from models.teacher import Teacher
from models.course import Course

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
    
    teachers = [
        Teacher(
            name='Mr. Robot',
            department='Training and Development',
            address='Brisbane'
        ),
        Teacher(
            name='Alex Holder',
            department='Training and Development',
            address='Sydney'
        )
    ]
    
    db.session.add_all(teachers) # Need to add and commit teachers before creating courses to enable teacher_id foreign key
    db.session.commit()
        
    courses = [
        Course(
            name='Diploma of Web Development',
            start_date=date(2025, 10, 1),
            end_date=date(2026, 4, 20),
            teacher_id=teachers[1].id # Allocate teacher_id by position in the table
        ),
        Course(
            name='Diploma of Cybersecurity',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 7, 10),
            teacher_id=teachers[0].id
        ),
    ]
    
    db.session.add_all(students)
    db.session.add_all(courses)
    db.session.commit()
    print('Tables seeded.')