from flask import Blueprint,jsonify,request
from models.entities.administracion import Administracion
from models.adminmodel import AdminModel

admin = Blueprint('administracion_blueprint',__name__)

@admin.route('/')
def get_administracion():
    try:

        admin = AdminModel.get_administracion()
        return jsonify(admin)
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/<id>')
def get_admin(id):
    try:
        admin = AdminModel.get_administracion_id(id)
        if admin != None:
            return jsonify(admin)
        else:
            return jsonify({}),404
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/add', methods = ["POST"])
def add_student():
    try:

        id = request.json['id']
        pre_inscripcion = request.json['pre_inscripcion']
        inscripcion = request.json['inscripcion']
        cuota1 =request.json['cuota1']
        cuota2=request.json['cuota2']
        cuota3 =request.json['cuota3']
        cuota4 =request.json['cuota4']
        cuota5 =request.json['cuota5']

        
        admin = Administracion(str(id),pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = AdminModel.add_admin(admin)

        if affected_rows == 1:
            return jsonify(admin.id)
        else:
            return jsonify({'message': "Error on insert"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/update', methods = ["PUT"])
def update_admin():
    try:

        id = request.json['id']
        pre_inscripcion = request.json['pre_inscripcion']
        inscripcion = request.json['inscripcion']
        cuota1 =request.json['cuota1']
        cuota2=request.json['cuota2']
        cuota3 =request.json['cuota3']
        cuota4 =request.json['cuota4']
        cuota5 =request.json['cuota5']

        
        admin = Administracion(str(id),pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = AdminModel.update_admin(admin)

        if affected_rows == 1:
            return jsonify(admin.id)
        else:
            return jsonify({'message': "Error on insert"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@admin.route('/delete/<id>', methods = ["DELETE"])
def delete_admin(id):
    try:
        
        admin = Administracion(str(id))

        affected_rows = AdminModel.delete_admin(admin)

        if affected_rows == 1:
            return jsonify(admin.id)
        else:
            return jsonify({'message': "Does not exists!"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500