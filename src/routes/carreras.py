from flask import Blueprint,jsonify,request
from models.carreramodel import CarreraModel
from models.entities.carreras import Carrera
from werkzeug.security import generate_password_hash, check_password_hash

carrera = Blueprint('carrera_blueprint', __name__)

@carrera.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@carrera.route('/')
def get_carreras():

    try:
            carreras = CarreraModel.get_carreras()
            return jsonify({"ok": True, "status":200,"data": carreras})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@carrera.route('/<id>')
def get_carrera(id):
     
    try:
           
        carreras = CarreraModel.get_carrera(id)
        if carreras != None:
            return jsonify({"ok": True, "status":200,"data":carreras})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "carrera no encontrada"}}),404
    

    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    

@carrera.route('/add', methods = ['POST'])
def add_carrera():

    try:

        id = request.json['id']
        nombre = request.json['nombre']

        carrera = Carrera(str(id),nombre)

        affected_rows = CarreraModel.add_carrera(carrera)

        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
        
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
    
@carrera.route('/update/<id>', methods = ['PUT'])
def update_carrera(id):
     
    try:
        
        id = request.json['id']
        nombre = request.json['nombre']

        carrera = Carrera(str(id),nombre)

        affected_rows = CarreraModel.update_carrera(carrera)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data":None})
        
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
        
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@carrera.route('/delete/<id>', methods = [ 'DELETE'])
def delete_carrera(id):

    try:
        
        carrera  = Carrera(str(id))

        affected_rows = CarreraModel.delete_carrera(carrera)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "carrera no encontrada"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500