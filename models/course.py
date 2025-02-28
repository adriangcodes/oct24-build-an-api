from init import db, ma
from marshmallow_sqlalchemy import fields


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', back_populates='courses') # Pulls data from teacher table without creating table entry in courses # back_populates forces an update if a dependent record updates

    
class CourseSchema(ma.Schema):
    teacher = fields.Nested('TeacherSchema') # States that teacher is to be a set of nested fields within the Course schema
    
    class Meta:
        fields = ('id', 'name', 'start_date', 'end_date', 'teacher_id', 'teacher')
        

one_course = CourseSchema()
many_courses = CourseSchema(many=True, exclude=['teacher']) # Excludes the full teacher schema from all courses query

course_without_id = CourseSchema(exclude=['id'])