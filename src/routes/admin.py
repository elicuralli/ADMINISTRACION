from flask import Blueprint,jsonify,request
from flask_cors import CORS
from models.entities.administracion import Administracion
from models.adminmodel import AdminModel

admin = Blueprint('administracion_blueprint',__name__)
CORS(admin)

@admin.route('/')
def get_administracion():
    try:

        admin = AdminModel.get_administracion()
        return jsonify({"ok": True, "status":200,"data":admin})

    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/<id>')
def get_admin(id):
    try:
        admin = AdminModel.get_administracion_id(id)
        if admin != None:
            return jsonify({"ok": True, "status":200,"data":admin})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Pago no encontrado"}}),404
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/add', methods = ["POST"])
def add_admin():
    try:

        id = request.json['id']
        pre_inscripcion = request.json['pre_inscripcion']
        inscripcion = request.json['inscripcion']
        cedula_student = request.json['cedula_student']
        cuota1 =request.json['cuota1']
        cuota2=request.json['cuota2']
        cuota3 =request.json['cuota3']
        cuota4 =request.json['cuota4']
        cuota5 =request.json['cuota5']

        
        admin = Administracion(str(id),str(cedula_student),pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = AdminModel.add_admin(admin)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":admin})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al insertar"}}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/update/<id>', methods = ["PUT"])
def update_admin(id):
    try:

        id = request.json['id']
        pre_inscripcion = request.json['pre_inscripcion']
        inscripcion = request.json['inscripcion']
        cedula_student = request.json['cedula_student']
        cuota1 =request.json['cuota1']
        cuota2=request.json['cuota2']
        cuota3 =request.json['cuota3']
        cuota4 =request.json['cuota4']
        cuota5 =request.json['cuota5']

        
        admin = Administracion(str(id),str(cedula_student),pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = AdminModel.update_admin(admin)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":admin})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al insertar"}}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/delete/<id>', methods = ["DELETE"])
def delete_admin(id):
    try:
        
        admin = Administracion(str(id))

        affected_rows = AdminModel.delete_admin(admin)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al insertar"}}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route("/count/month/<number>", methods = ["GET"])
def count_month(number):
    try:
        count = AdminModel.count_month(number)
        return jsonify({"ok": True, "status": 200, "total": count})
    except Exception as ex:
        return jsonify({"message": str(ex)})

@admin.route("/count/day/<number>", methods = ["GET"])
def count_day(number):
    try:
        count = AdminModel.count_day(number)
        return jsonify({"ok": True, "status": 200, "total": count})
    except Exception as ex:
        return jsonify({"message": str(ex)})