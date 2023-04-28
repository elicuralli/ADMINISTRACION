from flask import Blueprint,jsonify,request
from models.entities.students import Student
from models.studentsmodel import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash


main= Blueprint('students_blueprint',__name__)
@main.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@main.route('/')
def get_students():
    try:

        students = StudentModel.get_students()
        return jsonify({"ok": True, "status":200,"data":students})
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@main.route('/<cedula>')
def get_student(cedula):
    try:
        student = StudentModel.get_student(cedula)
        if student != None:
            return jsonify({"ok": True, "status":200,"data":student})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Estudiante no encontrado"}}),404
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@main.route('/add', methods = ["POST"])
def add_student():
    try:

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        estado = request.json['estado']
        password = generate_password_hash(request.json["password"], method="sha256")

        student = Student(str(cedula),fullname,correo,telefono,semestre,password,estado)

        affected_rows = StudentModel.add_student(student)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al insertar"}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500
    
    

@main.route('/update/<cedula>', methods = ["PUT"])
def update_student(cedula):
    try:
    
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        estado = request.json['estado']
        password = generate_password_hash(request.json["password"], method="sha256")
 
        student = Student(str(cedula),fullname,correo,telefono,semestre,password,estado)

        affected_rows = StudentModel.update_student(student)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar"}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500


@main.route('/delete/<cedula>', methods = ["DELETE"])
def delete_student(cedula):
    try:
        
        student = Student(str(cedula))

        affected_rows = StudentModel.delete_student(student)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Estudiante no encontrado"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500


@main.route("/count", methods = ["GET"])
def count_student():
    try:
        count = StudentModel.count_students()
        if count != 0:
            return jsonify({"ok": True, "status": 200, "total": count})
        else:
            return jsonify({"ok": False, "status": 404, 'message': "No hay estudiantes registrados!"}), 404
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500