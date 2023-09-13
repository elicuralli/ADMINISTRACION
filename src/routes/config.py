from models.entities.config import Configuracion
from models.configmodel import ConfigModel
from flask import Blueprint,jsonify,request

config = Blueprint('config_blueprint', __name__)

@config.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@config.route('/')
def get_configuraciones():

    try:

        configuraciones = ConfigModel.get_configuraciones()
        return jsonify({"ok": True, "status":200,"data": configuraciones})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@config.route('/<id>')
def get_configuracion(id):

    try:

        configuracion = ConfigModel.get_configuracion(id)
        if configuracion != None:
            return jsonify({"ok": True, "status":200,"data":configuracion.to_JSON()})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "config no disponible"}}),404
    
    except Exception as ex:
        print(str(ex))
        return jsonify({"message": str(ex)}),500

@config.route('/add' ,methods = ["POST"])
def add_configuracion():

    try:
        
        ciclo = request.json['ciclo']
        porc1 = request.json['porc1']
        porc2 = request.json['porc2']
        porc3 = request.json['porc3']
        horario_inicio = request.json['horario_inicio']
        horario_fin = request.json['horario_fin']
        cuota1 = request.json['cuota1']
        cuota2 = request.json['cuota2']
        cuota3 = request.json['cuota3']
        cuota4 = request.json['cuota4']
        cuota5 = request.json['cuota5']

        config = Configuracion(None,ciclo,porc1,porc2,porc3,horario_inicio,horario_fin,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = ConfigModel.add_configuracion(config)

        if affected_rows == 1:
             return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500

    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500

@config.route('/update/<id>', methods = ["PUT"])
def update_configuracion(id):
    
    try:
        ciclo = request.json['ciclo']
        porc1 = request.json['porc1']
        porc2 = request.json['porc2']
        porc3 = request.json['porc3']
        horario_inicio = request.json['horario_inicio']
        horario_fin = request.json['horario_fin']
        cuota1 = request.json['cuota1']
        cuota2 = request.json['cuota2']
        cuota3 = request.json['cuota3']
        cuota4 = request.json['cuota4']
        cuota5 = request.json['cuota5']

        config = Configuracion(str(id),ciclo,porc1,porc2,porc3,horario_inicio,horario_fin,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = ConfigModel.update_configuracion(config)

        if affected_rows == 1:
             return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500

    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
    

@config.route('/delete/<id>', methods = [ 'DELETE'])
def delete_peticion(id):

    try:
        
        config = Configuracion(str(id))

        affected_rows = ConfigModel.delete_configuracion(config)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "confi no encontrada"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500