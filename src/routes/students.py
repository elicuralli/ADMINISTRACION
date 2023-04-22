from flask import Blueprint,jsonify,request
from models.entities.students import Student
from models.studentsmodel import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash

main= Blueprint('students_blueprint',__name__)

@main.route('/')
def get_students():
    try:

        students = StudentModel.get_students()
        return jsonify(students)
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@main.route('/<id>')
def get_student(id):
    try:
        student = StudentModel.get_student(id)
        if student != None:
            return jsonify(student)
        else:
            return jsonify({}),404
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@main.route('/add', methods = ["POST"])
def add_student():
    try:
        id = request.json['id']
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        password = generate_password_hash(request.json["password"], method="sha256")
 
        student = Student(str(id),cedula,fullname,correo,telefono,semestre,password)

        affected_rows = StudentModel.add_student(student)

        if affected_rows == 1:
            return jsonify(student.id)
        else:
            return jsonify({'message': "Error on insert"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    

@main.route('/update/<id>', methods = ["PUT"])
def update_student(id):
    try:
        id = request.json['id']
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        password = generate_password_hash(request.json["password"], method="sha256")
 
        student = Student(str(id),cedula,fullname,correo,telefono,semestre,password)

        affected_rows = StudentModel.update_student(student)

        if affected_rows == 1:
            return jsonify(student.id)
        else:
            return jsonify({'message': "Error on update"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@main.route('/delete/<id>', methods = ["DELETE"])
def delete_student(id):
    try:
        id = request.json['id']
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        password = generate_password_hash(request.json["password"], method="sha256")
 
        student = Student(str(id),cedula,fullname,correo,telefono,semestre,password)

        affected_rows = StudentModel.delete_student(student)

        if affected_rows == 1:
            return jsonify(student.id)
        else:
            return jsonify({'message': "Does not exists!"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500