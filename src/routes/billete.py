# imports
from flask import Blueprint,jsonify,request
from flask_apispec import use_kwargs
from models.billetemodel import BilleteModel
from models.entities.billete import Billete
from models.entities.marshmallow_schemas import BilleteSchema

# blueprint
billete = Blueprint("billete_blueprint",__name__)

# routes
@billete.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@billete.route('/', methods=["GET"], provide_automatic_options=False)
def get_billetes():

    try:
            billete = BilleteModel.get_billetes()
            return jsonify({"ok": True, "status":200,"data": billete})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@billete.route('/<codigo>', methods=["GET"], provide_automatic_options=False)
def get_billete(codigo):
     
    try:
           
        billete = BilleteModel.get_billete(codigo)
        if billete != None:
            return jsonify({"ok": True, "status":200,"data": billete})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "billete no encontrado"}}),404
    

    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
    
@billete.route('/add', methods = ['POST'], provide_automatic_options=False)
@use_kwargs(BilleteSchema)
def add_billete():

    try:

        codigo = request.json['codigo']
        cantidad = request.json['cantidad']
        factura = request.json['factura']

        billete = Billete(str(codigo),cantidad,factura)

        affected_rows = BilleteModel.add_billete(billete)


        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
        


    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500

@billete.route('/update/<codigo>', methods = ['PUT'], provide_automatic_options=False)
@use_kwargs(BilleteSchema)
def update_billete(codigo):

    try:

        codigo = request.json['codigo']
        cantidad = request.json['cantidad']

        billete = Billete(str(codigo),cantidad)

        affected_rows = BilleteModel.update_billete(billete)


        if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
        
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500