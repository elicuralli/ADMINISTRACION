from models.entities.peticiones import Peticiones
from models.peticionesmodel import PeticionesModel
from flask import Blueprint,jsonify,request

peticion = Blueprint('peticion_blueprint', __name__)

@peticion.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@peticion.route('/')
def get_peticiones():

    try:

        peticiones = PeticionesModel.get_peticiones()
        return jsonify({"ok": True, "status":200,"data": peticiones})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@peticion.route('/<id>')
def get_peticion(id):

    try:

        peticiones = PeticionesModel.get_peticion(id)
        if peticiones != None:
            return jsonify({"ok": True, "status":200,"data":peticiones})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "peticion no disponible"}}),404
    
    except Exception as ex:
            return jsonify({"message": str(ex)}),500

@peticion.route('/add' ,methods = ["POST"])
def add_peticion():

    try:

        id = request.json['id']
        id_docente = request.json['id_docente']
        descripcion = request.json['descripcion']
        destino = request.json['destino']

        estado = request.json['estado']
        if estado not in ["Aprobado", "Denegado", "Pendiente"]:
            return jsonify({'error': 'Valor inválido para el campo estado'}), 400
        
        id_estudiante = request.json['id_estudiante']
        id_materia = request.json['id_materia']
        campo = request.json['campo']

        peticion = Peticiones(str(id),id_docente,descripcion,destino,estado,id_estudiante,id_materia,campo)
        affected_rows = PeticionesModel.add_peticion(peticion)

        if affected_rows == 1:
             return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500

    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500

@peticion.route('/update/<id>', methods = ["PUT"])
def update_peticion(id):

    try:

            id = request.json['id']
            id_docente = request.json['id_docente']
            descripcion = request.json['descripcion']
            destino = request.json['destino']

            estado = request.json['estado']
            if estado not in ["Aprobado", "Denegado", "Pendiente"]:
                return jsonify({'error': 'Valor inválido para el campo estado'}), 400
            
            id_estudiante = request.json['id_estudiante']
            id_materia = request.json['id_materia']
            campo = request.json['campo']

            peticion = Peticiones(str(id),id_docente,descripcion,destino,estado,id_estudiante,id_materia,campo)
            affected_rows = PeticionesModel.update_peticion(peticion)

            if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
            else:
                return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500

    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500

@peticion.route('/delete/<id>', methods = [ 'DELETE'])
def delete_peticion(id):

    try:
        
        peticion  = Peticiones(str(id))

        affected_rows = PeticionesModel.delete_peticion(peticion)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "peticion no encontrada"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500