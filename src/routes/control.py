from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta
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

        control_es = Control(str(cedula),fullname,correo,telefono,password)

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

        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

 
        control_es = Control(str(cedula),fullname,correo,telefono,password)

        affected_rows = ControlModel.update_control(control_es)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    
    except Exception as ex:
        print(ex)
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

@control.route('/login',methods = ["POST"])
def login():
    try: 
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        control_estudio = Control(correo=usuario)
        control_estudio = ControlModel.login(control_estudio)
        if control_estudio is not None:
            if check_password_hash(control_estudio.password, clave): # comprobamos que el hash sea igual a la clave ingrasada
                access_token = create_access_token(identity=control_estudio.correo, expires_delta=timedelta(hours=1), additional_claims={'rol': 'CE'}) # creamos el token que vive una hora
                return jsonify({"ok":True, "status": 200, "data": {"control_estudio": control_estudio.to_JSON(), "access_token": f"Bearer {access_token}"}})
        
            else:
                return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401


    except Exception as ex:
        return jsonify({"ok":False, "status": 500, "data": {"message": str(ex)}}), 500

@control.route('/refresh')
@jwt_required()
def jwt_coordinador():
    try:
        correo_coordinador = get_jwt_identity() # esto obtiene la identidad del token, en este caso, un correo
        control_estudio: Control | None # declaramos sin iniciar la variable del control_estudio
        if correo_coordinador is not None:
            coordinador_entity = Control(correo=correo_coordinador) # creamos la entidad del control_estudio
            control_estudio = ControlModel.login(coordinador_entity) #revisamos la bd
            if control_estudio != None:
                return jsonify({"ok": True, "status":200,"data":control_estudio.to_JSON()}) # retornamos si es correcto
            
        else:
            return jsonify({"ok": False, "status":401,"data":{"message": "no autorizado"}}),401
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500