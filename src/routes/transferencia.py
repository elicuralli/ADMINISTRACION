from flask import Blueprint,jsonify,request
from models.transferenciamodel import TransferenciaModel
from models.entities.transferencias import Transferencia

transf = Blueprint("transf_blueprint",__name__)

@transf.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@transf.route('/')
def get_transferencias():

    try:
            transferencia = TransferenciaModel.get_transferencias()
            return jsonify({"ok": True, "status":200,"data":transferencia})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@transf.route('/<id>')
def get_transferencia(id):
     
    try:
           
        transferencia = TransferenciaModel.get_transferencia(id)
        if transferencia != None:
            return jsonify({"ok": True, "status":200,"data": transferencia})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "transferencia no encontrada"}}),404
    

    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@transf.route('/add', methods = ['POST'])
def add_transferencia():

    try:

        id = request.json['id']
        codigo_referencia = request.json['codigo_referencia']
        metodo_pago = request.json[' metodo_pago']

        transferencia = (str(id),codigo_referencia,metodo_pago)

        affected_rows = TransferenciaModel.add_transferencia(transferencia)


        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
        


    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500

@transf.route('/update/<id>', methods = ['PUT'])
def update_transferencia(id):

    try:

        
        codigo_referencia = request.json['codigo_referencia']
        metodo_pago = request.json[' metodo_pago']

        transferencia = (codigo_referencia,metodo_pago)

        affected_rows = TransferenciaModel.update_transferencia(transferencia)


        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
        
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

    