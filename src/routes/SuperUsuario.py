from models.entities.SuperUsuario import SuperUsuario
from models.SuperUsuarioModel import SuperUsuarioModel
from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash


superUs = Blueprint('superUsuario_Blueprint',__name__)

@superUs.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@superUs.route('/<cedula>')
def get_Super(cedula):
    try:
        superUs = SuperUsuarioModel.get_super_user(cedula)
        if super != None:
            return jsonify({"ok": True, "status":200,"data":superUs})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "super usuario no encontrado"}}),404
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@superUs.route('/add', methods = ["POST"])
def add_Super():
    try:

        cedula = request.json['cedula']
        nombre = request.json['nombre']
        correo = request.json['correo']
        password = generate_password_hash(request.json["password"], method="sha256")

        superUs  = SuperUsuario(str(cedula),nombre,correo,password)

        affected_rows = SuperUsuarioModel.add_super_user(superUs)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
    
@superUs.route('/update/<cedula>', methods = ["PUT"])
def update_Super(cedula):
    try:
    
        cedula = request.json['cedula']
        nombre = request.json['nombre']
        correo = request.json['correo']
        password = generate_password_hash(request.json["password"], method="sha256")
 
        superUs = SuperUsuario(str(cedula),nombre,correo,password)

        affected_rows = SuperUsuarioModel.update_super_user(superUs)
        print(affected_rows)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500

@superUs.route('/delete/<cedula>', methods = ["DELETE"])
def delete_Super(cedula):
    try:
        
        superUs = SuperUsuario(str(cedula))

        affected_rows = SuperUsuarioModel.delete_super_user(superUs)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "super usuario no encontrado"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500