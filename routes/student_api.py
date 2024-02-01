from flask import Blueprint, jsonify, request
from models.student import Student, StudentSchema
from extension import db

student_api = Blueprint('api',__name__,url_prefix='/api/student')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


@student_api.route("/get", methods=["GET"])
def students_list():
    students = Student.query.all()
    return students_schema.dump(students)

@student_api.route("/create", methods=["POST"])
def student_create():
    firstname=request.json["firstname"]
    lastname=request.json["lastname"]
    new_student = Student(firstname, lastname)
    db.session.add(new_student)
    db.session.commit()
    return student_schema.jsonify(new_student)

@student_api.route("/get/<id>", methods=["GET"])
def student_detail(id):
    student = Student.query.get(id)
    return student_schema.dump(student)

@student_api.route("/update/<id>", methods=["PUT"])
def student_update(id):
    student = Student.query.get(id)
    firstname=request.json["firstname"]
    lastname=request.json["lastname"]
    student.firstname = firstname
    student.lastname = lastname
    db.session.commit()
    return student_schema.jsonify(student)

@student_api.route("/delete/<id>", methods=["DELETE"])
def student_delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return student_schema.jsonify(student)