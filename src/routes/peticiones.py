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

@peticion.route('/pendientes')
def get_peticiones_pendientes():
    try:
        peticiones_pendientes = PeticionesModel.get_peticiones_pendientes()
        return jsonify({"ok": True, "status": 200, "data": peticiones_pendientes})

    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@peticion.route('/add' ,methods = ["POST"])
def add_peticion():

    try:

        id_docente = request.json['id_docente']
        descripcion = request.json['descripcion']

        estado = request.json['estado']
        if estado not in ["Aprobado", "Denegado", "Pendiente"]:
            return jsonify({'error': 'Valor inválido para el campo estado'}), 400
        
        id_estudiante = request.json['id_estudiante']
        id_materia = request.json['id_materia']
        campo = request.json['campo']

        peticion = Peticiones(None,id_docente,descripcion,estado,id_estudiante,id_materia,campo)
        affected_rows = PeticionesModel.add_peticion(peticion)

        if affected_rows == 1:
             return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500

    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500

@peticion.route('/update/<id>', methods = ["PATCH"])
def update_peticion(id):

    try:
        data = request.json

        # Definimos una lista de campos permitidos para actualizar.
        allowed_fields = ["id_docente", "descripcion", "estado", "id_estudiante", "id_materia", "campo"]

        # Filtramos los campos proporcionados en la solicitud para asegurarnos de que solo se actualicen los campos permitidos.
        fields_to_update = {field: data[field] for field in allowed_fields if field in data}

        # Si no se proporcionan campos permitidos para actualizar, devolvemos un error con código 400.
        if not fields_to_update:
            return jsonify({"error": "No se proporcionaron campos válidos para actualizar"}), 400

        # Agregamos el ID de la solicitud a los campos a actualizar para asegurarnos de que actualicemos la solicitud correcta.
        fields_to_update["id"] = id
        peticion = Peticiones(**fields_to_update)

        # Llamamos a la función update_peticion del modelo para actualizar la solicitud en la base de datos.
        affected_rows = PeticionesModel.update_peticion(peticion)

        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500


    except Exception as ex:
        print(ex)
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