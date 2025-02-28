from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow import fields # Required for .String validation
from marshmallow.validate import Length, And, Regexp # Required for Length validation


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', back_populates='courses') # Pulls data from teacher table without creating table entry in courses # back_populates forces an update if a dependent record updates

    
class CourseSchema(ma.Schema):
    name = fields.String(required=True, validate=And(
        Length(min=5, error='Name must be at least 5 characters long.'),
        Regexp('^[A-Za-z0-9 ()-]$', error='Error: only letters, numbers, spaces, parentheses and hyphens allowed') # Provides filter that only allows A-Z, a-z, 0-9, space, parentheses and hyphen in the input
        ) # Allows Marshmallow to provide data validation
    )
    
    teacher = fields.Nested('TeacherSchema') # States that teacher is to be a set of nested fields within the Course schema
    
    class Meta:
        fields = ('id', 'name', 'start_date', 'end_date', 'teacher_id', 'teacher')
        

one_course = CourseSchema()
many_courses = CourseSchema(many=True, exclude=['teacher']) # Excludes the full teacher schema from all courses query

course_without_id = CourseSchema(exclude=['id'])