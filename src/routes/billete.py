from flask import Blueprint,jsonify,request
from models.billetemodel import BilleteModel
from models.entities.billete import Billete


billete = Blueprint("billete_blueprint",__name__)

@billete.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@billete.route('/')
def get_billetes():

    try:
            billete = BilleteModel.get_billetes()
            return jsonify({"ok": True, "status":200,"data": billete})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@billete.route('/<id>')
def get_billete(id):
     
    try:
           
        billete = BilleteModel.get_billete(id)
        if billete != None:
            return jsonify({"ok": True, "status":200,"data": billete})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "billete no encontrado"}}),404
    

    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@billete.route('/add', methods = ['POST'])
def add_billete():

    try:

        id = request.json['id']
        serial = request.json['serial']
        monto = request.json['monto']

        billete = Billete(str(id),serial,monto)

        affected_rows = BilleteModel.add_billete(billete)


        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
        


    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500

@billete.route('/update/<id>', methods = ['PUT'])
def update_billete(id):

    try:

       
        serial = request.json['serial']
        monto = request.json['monto']

        billete = Billete(serial,monto)

        affected_rows = BilleteModel.update_billete(billete)


        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
        
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

    