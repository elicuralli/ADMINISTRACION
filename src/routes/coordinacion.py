from models.entities.coordinacion import Coordinacion
from models.coordinacionmodel import CoordinacionModel
from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash

coordinacion = Blueprint('coordinacion_blueprint',__name__)

@coordinacion.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@coordinacion.route('/')
def get_coordinadores():
    try:

        coordinadores = CoordinacionModel.get_coordinadores()
        return jsonify({"ok": True, "status":200,"data": coordinadores})
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500

@coordinacion.route('/<cedula>')
def get_coordinador(cedula):
    try:
        coordinador = CoordinacionModel.get_coordinador(cedula)
        if coordinador != None:
            return jsonify({"ok": True, "status":200,"data":coordinador})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "coordinador no encontrado"}}),404
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@coordinacion.route('/add', methods = ["POST"])
def add_coordinador():
    try:

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        coordinador  = Coordinacion(str(cedula),fullname,correo,telefono,password)

        affected_rows = CoordinacionModel.add_coordinador(coordinador)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
    
@coordinacion.route('/update/<cedula>', methods = ["PUT"])
def update_coordinador(cedula):
    try:
    
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']

        password = generate_password_hash(request.json["password"], method="sha256")
 
        coordinador = Coordinacion(str(cedula),fullname,correo,telefono,password)

        affected_rows = CoordinacionModel.update_coordinador(coordinador)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@coordinacion.route('/delete/<cedula>', methods = ["DELETE"])
def delete_coordinador(cedula):
    try:
        
        coordinador  =  Coordinacion(str(cedula))

        affected_rows = CoordinacionModel.delete_coordinador(coordinador)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "coordinador no encontrado"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500