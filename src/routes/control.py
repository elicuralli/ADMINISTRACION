from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash
from models.entities.control import Control
from models.controlmodel import ControlModel

control = Blueprint('control_es_blueprint',__name__)

@control.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@control.route('/')
def get_todo_control():
    try:

        control_es = ControlModel.get_todo_control()
        return jsonify({"ok": True, "status":200,"data": control_es})
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@control.route('/<cedula>')
def get_control(cedula):
    try:
        control_es = ControlModel.get_control(cedula)
        if control_es != None:
            return jsonify({"ok": True, "status":200,"data":control_es})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "usuario no encontrado"}}),404
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@control.route('/add', methods = ["POST"])
def add_control():
    try:

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")
        rol = request.json['rol']

        control_es = Control(str(cedula),fullname,correo,telefono,password,rol)

        affected_rows = ControlModel.add_control(control_es)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
    
@control.route('/update/<cedula>', methods = ["PUT"])
def update_coordinador(cedula):
    try:
    
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")
        rol = request.json['rol']

 
        control_es = Control(str(cedula),fullname,correo,telefono,password,rol)

        affected_rows = ControlModel.update_control(control_es)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@control.route('/delete/<cedula>', methods = ["DELETE"])
def delete_coordinador(cedula):
    try:
        
        control_es  =  Control(str(cedula))

        affected_rows = ControlModel.delete_control(control_es)


        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "usuario no encontrado"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500