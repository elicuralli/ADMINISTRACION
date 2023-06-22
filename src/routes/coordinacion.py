from models.entities.coordinacion import Coordinacion
from models.coordinacionmodel import CoordinacionModel
from flask import Blueprint,jsonify,request
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

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

@coordinacion.route('/login',methods = ["POST"])
def login():
    try: 
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        coordinador = Coordinacion(correo=usuario)
        coordinador = CoordinacionModel.login(coordinador)
        if coordinador is not None:
            if check_password_hash(coordinador.password, clave): # comprobamos que el hash sea igual a la clave ingrasada
                access_token = create_access_token(identity=coordinador.correo, expires_delta=timedelta(hours=1), additional_claims={'rol': 'CO'}) # creamos el token que vive una hora
                return jsonify({"ok":True, "status": 200, "data": {"coordinador": coordinador.to_JSON(), "access_token": f"Bearer {access_token}"}})
        
            else:
                return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectosa"}}), 401
        else:
            return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectosb"}}), 401


    except Exception as ex:
        return jsonify({"ok":False, "status": 500, "data": {"message": str(ex)}}), 500

@coordinacion.route('/refresh')
@jwt_required()
def jwt_coordinador():
    try:
        correo_coordinador = get_jwt_identity() # esto obtiene la identidad del token, en este caso, un correo
        coordinador: Coordinacion | None # declaramos sin iniciar la variable del coordinador
        if correo_coordinador is not None:
            coordinador_entity = Coordinacion(correo=correo_coordinador) # creamos la entidad del coordinador
            coordinador = CoordinacionModel.login(coordinador_entity) #revisamos la bd
            if coordinador != None:
                return jsonify({"ok": True, "status":200,"data":coordinador.to_JSON()}) # retornamos si es correcto
            
        else:
            return jsonify({"ok": False, "status":401,"data":{"message": "no autorizado"}}),401
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500