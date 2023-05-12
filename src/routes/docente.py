from flask import Blueprint,jsonify,request
from models.entities.docente import Docente
from models.docentemodel import DocenteModel
from werkzeug.security import generate_password_hash, check_password_hash

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
        asignatura = request.json['asignatura']
        password = generate_password_hash(request.json["password"], method="sha256")

        docente  = Docente(str(cedula),fullname,correo,telefono,asignatura,password)

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
        asignatura = request.json['asignatura']

        password = generate_password_hash(request.json["password"], method="sha256")
 
        docente = Docente(str(cedula),fullname,correo,telefono,asignatura,password)

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