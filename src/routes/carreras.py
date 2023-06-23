from flask import Blueprint,jsonify,request
from flask_apispec import use_kwargs
from models.carreramodel import CarreraModel
from models.entities.carreras import Carrera
from models.entities.marshmallow_schemas import CarreraSchema

carrera = Blueprint('carrera_blueprint', __name__)

@carrera.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@carrera.route('/', methods=["GET"], provide_automatic_options=False)
def get_carreras():

    try:
            carreras = CarreraModel.get_carreras()
            return jsonify({"ok": True, "status":200,"data": carreras})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@carrera.route('/<id>', methods=["GET"], provide_automatic_options=False)
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
    

@carrera.route('/add', methods = ['POST'], provide_automatic_options=False)
@use_kwargs(CarreraSchema)
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
    
@carrera.route('/update/<id>', methods = ['PUT'], provide_automatic_options=False)
@use_kwargs(CarreraSchema)
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

@carrera.route('/delete/<id>', methods = [ 'DELETE'], provide_automatic_options=False)
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