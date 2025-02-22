from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.teacher import Teacher, many_teachers, one_teacher, TeacherSchema, teacher_without_id

teachers_bp = Blueprint('teachers', __name__)

# Read all - GET /teachers
@teachers_bp.route('/teachers')
def get_all_teachers():
    stmt = db.select(Teacher).order_by(Teacher.id.asc()) # Orders by id ascending
    teachers = db.session.scalars(stmt)
    return many_teachers.dump(teachers)

# Read one - GET /teachers/<int:teacher_id>
@teachers_bp.route('/teachers/<int:teacher_id>')
def get_one_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return one_teacher.dump(teacher)
    else:
        return {"error": f"Teacher with id {teacher_id} not found."}, 404

# Create - POST /teachers
@teachers_bp.route('/teachers', methods=['POST'])
def create_teacher():
    try:
        # Get incoming request body (JSON)
        data = teacher_without_id.load(request.json)
        # Create new instance of Teacher model
        new_teacher = Teacher(
            name = data['name'],
            department = data['department'],
            address = data.get('address', '')
        )
        # Add the instance to the db session
        db.session.add(new_teacher)
        # Commit the instance to the db
        db.session.commit()
        return one_teacher.dump(new_teacher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use."}, 409 # Conflict
        # elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        #     return {"error": str(err.orig)}, 406 # Not acceptable
        else:
            return {"error": err.orig.diag.message_detail}, 400

# Update - PUT /teachers/<int:teacher_id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['PUT', 'PATCH'])
def update_teacher(teacher_id):
    try:
        # Fetch teacher by id
        stmt = db.select(Teacher).filter_by(id=teacher_id)
        teacher = db.session.scalar(stmt)
        if teacher:
            # Get incoming request body (JSON)
            data = teacher_without_id.load(request.json)
            # Update the attributes of the teacher with the incoming data
            # OR option means that the below code covers both PUT and PATCH methods
            teacher.name = data.get('name') or teacher.name
            teacher.department = data.get('department') or teacher.department
            teacher.address = data.get('address') or teacher.address
            # Commit the instance to the db
            db.session.commit()
            return one_teacher.dump(teacher), 200
        else:
            return {"error": f"Teacher with id {teacher_id} not found."}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use."}, 409 # Conflict
        # elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        #     return {"error": str(err.orig)}, 400
        else:
            return {"error": err.orig.diag.message_detail}, 400

# Delete - DELETE /teachers/<int:teacher_id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204
    else:
        return {"error": f"Teacher with id {teacher_id} not found."}, 404