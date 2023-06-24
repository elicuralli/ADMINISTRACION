from flask import Blueprint,jsonify,request
from models.entities.docente import Docente
from models.docentemodel import DocenteModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

doc = Blueprint('docentes_blueprint',__name__)

@doc.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@doc.route('/')
def get_docentes():
    try:

        docentes = DocenteModel.get_docentes()
        return jsonify({"ok": True, "status":200,"data": docentes})
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@doc.route('/<cedula>')
def get_docente(cedula):
    try:
        docentes = DocenteModel.get_docente(cedula)
        if docentes != None:
            return jsonify({"ok": True, "status":200,"data":docentes})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "docente no encontrado"}}),404
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@doc.route('/add', methods = ["POST"])
def add_docente():
    try:

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        password = generate_password_hash(request.json["password"], method="sha256")

        docente  = Docente(str(cedula),fullname,correo,telefono,password)

        affected_rows = DocenteModel.add_docente(docente)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
    
@doc.route('/update/<cedula>', methods = ["PUT"])
def update_docente(cedula):
    try:
    
        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']

        password = generate_password_hash(request.json["password"], method="sha256")
 
        docente = Docente(str(cedula),fullname,correo,telefono,password)

        affected_rows = DocenteModel.update_docente(docente)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@doc.route('/delete/<cedula>', methods = ["DELETE"])
def delete_docente(cedula):
    try:
        
        docente  = Docente(str(cedula))

        affected_rows = DocenteModel.delete_docente(docente)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "docente no encontrado"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500

@doc.route('/login',methods = ["POST"])
def login():
    try: 
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        docente = Docente(correo=usuario)
        docente = DocenteModel.login(docente)
        if docente is not None:
            if check_password_hash(docente.password, clave): # comprobamos que el hash sea igual a la clave ingrasada
                access_token = create_access_token(identity=docente.correo, expires_delta=timedelta(hours=1), additional_claims={'rol': 'D'}) # creamos el token que vive una hora
                return jsonify({"ok":True, "status": 200, "data": {"docente": docente.to_JSON(), "access_token": f"Bearer {access_token}"}})
        
            else:
                return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok":False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401


    except Exception as ex:
        return jsonify({"ok":False, "status": 500, "data": {"message": str(ex)}}), 500

@doc.route('/refresh')
@jwt_required()
def jwt_docente():
    try:
        correo_docente = get_jwt_identity() # esto obtiene la identidad del token, en este caso, un correo
        student: Docente | None # declaramos sin iniciar la variable del docente
        if correo_docente is not None:
            student_entity = Docente(correo=correo_docente) # creamos la entidad del docente
            student = DocenteModel.login(student_entity) #revisamos la bd
            if student != None:
                return jsonify({"ok": True, "status":200,"data":student.to_JSON()}) # retornamos si es correcto
            
        else:
            return jsonify({"ok": False, "status":401,"data":{"message": "no autorizado"}}),401
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500