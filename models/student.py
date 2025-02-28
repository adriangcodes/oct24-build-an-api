from init import db, ma
from marshmallow.validate import Email


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(300))

    
class StudentSchema(ma.Schema):
    email = Email(required=True) # Email validation
    
    class Meta:
        fields = ('id', 'name', 'email', 'address')
        

one_student = StudentSchema()
many_students = StudentSchema(many=True)

student_without_id = StudentSchema(exclude=['id'])