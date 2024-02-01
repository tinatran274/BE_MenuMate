from extension import db, ma 

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return f'<Student {self.firstname}>'
    

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname')