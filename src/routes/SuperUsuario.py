from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models.entities.SuperUsuario import SuperUsuario
from models.SuperUsuarioModel import SuperUsuarioModel
from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash, check_password_hash

from models.entities.students import Student
from models.studentsmodel import StudentModel

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

@superUs.route('/login',methods = ["POST"])
def login():
    try:
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        super_usuario = SuperUsuario(correo=usuario)
        super_usuario = SuperUsuarioModel.login(super_usuario)
        if super_usuario is not None:
            print(super_usuario.to_JSON())
            if check_password_hash(super_usuario.password, clave): # comprobamos que el hash sea igual a la clave ingrasada

                access_token = create_access_token(identity=super_usuario.correo, expires_delta=timedelta(hours=2), additional_claims={'rol': 'S'}) # creamos el token que vive una hora
                return jsonify({"ok": True, "status": 200, "data": {"superUsuario": super_usuario.to_JSON(), "access_token": f"Bearer {access_token}"}})

            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401


    except Exception as ex:
        print(ex)
        return jsonify({"ok":False, "status": 500, "data": {"message": str(ex)}}), 500

@superUs.route('/refresh')
@jwt_required()
def jwt_super():
    try:
        correo_super = get_jwt_identity() # esto obtiene la identidad del token, en este caso, un correo
        super_entity: SuperUsuario | None # declaramos sin iniciar la variable del estudiante
        if correo_super is not None:
            super_entity = SuperUsuario(correo=correo_super) # creamos la entidad del estudiante
            super_entity = SuperUsuarioModel.login(super_entity) #revisamos la bd
            if super_entity != None:
                return jsonify({"ok": True, "status":200,"data":super_entity.to_JSON()}) # retornamos si es correcto

        else:
            return jsonify({"ok": False, "status":401,"data":{"message": "no autorizado"}}),401

    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500