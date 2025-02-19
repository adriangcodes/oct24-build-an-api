from flask import Blueprint
from init import db
from models.student import Student, many_students, one_student

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student)
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
# Update - PUT /students/<int:student_id>
# Delete - DELETE /students/<int:student_id>

# Possible extra routes:
# Enrol - POST /students/<int:student_id>/<int:course_id>
# Unenrol - DELETE /students/<int:student_id>/<int:course_id>