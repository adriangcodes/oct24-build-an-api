from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.student import Student, many_students, one_student, StudentSchema, student_without_id

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student).order_by(Student.id.asc()) # Orders by id ascending
    students = db.session.scalars(stmt)
    return many_students.dump(students)

# Read one - GET /students/<int:student_id>
@students_bp.route('/students/<int:student_id>')
def get_one_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        return one_student.dump(student)
    else:
        return {"error": f"Student with id {student_id} not found."}, 404

# Create - POST /students
@students_bp.route('/students', methods=['POST'])
def create_student():
    try:
        # Get incoming request body (JSON)
        data = student_without_id.load(request.json)
        # Create new instance of Student model
        new_student = Student(
            name = data['name'],
            email = data['email'],
            address = data.get('address', '')
        )
        # Add the instance to the db session
        db.session.add(new_student)
        # Commit the instance to the db
        db.session.commit()
        return one_student.dump(new_student), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use."}, 409 # Conflict
        # elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        #     return {"error": str(err.orig)}, 406 # Not acceptable
        else:
            return {"error": err.orig.diag.message_detail}, 400

# Update - PUT /students/<int:student_id>
@students_bp.route('/students/<int:student_id>', methods=['PUT', 'PATCH'])
def update_student(student_id):
    try:
        # Fetch student by id
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)
        if student:
            # Get incoming request body (JSON)
            data = student_without_id.load(request.json)
            # Update the attributes of the student with the incoming data
            # OR option means that the below code covers both PUT and PATCH methods
            student.name = data.get('name') or student.name
            student.email = data.get('email') or student.email
            student.address = data.get('address') or student.address
            # Commit the instance to the db
            db.session.commit()
            return one_student.dump(student), 200
        else:
            return {"error": f"Student with id {student_id} not found."}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use."}, 409 # Conflict
        # elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        #     return {"error": str(err.orig)}, 400
        else:
            return {"error": err.orig.diag.message_detail}, 400

# Delete - DELETE /students/<int:student_id>
@students_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {}, 204
    else:
        return {"error": f"Student with id {student_id} not found."}, 404
    
# Possible extra routes:
# Enrol - POST /students/<int:student_id>/<int:course_id>
# Unenrol - DELETE /students/<int:student_id>/<int:course_id>