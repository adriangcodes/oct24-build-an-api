from init import db, ma


class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300))

    
class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'department', 'address')
        

one_teacher = TeacherSchema()
many_teachers = TeacherSchema(many=True)

teacher_without_id = TeacherSchema(exclude=['id'])