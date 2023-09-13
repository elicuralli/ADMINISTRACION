from flask import Blueprint, jsonify, request
from models.entities.pagos import Pago
from models.pagosmodel import PagoModel
from models.entities.monto import Monto
from models.mountmodel import MountModel
from models.metodomodel import MetodoModel
from models.entities.metodo import Metodo
from models.transferenciamodel import TransferenciaModel
from models.entities.transferencias import Transferencia
pago = Blueprint("pagos_blueprint", __name__)


@pago.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


@pago.route("/")
def get_pagos():
    try:
        pago = PagoModel.get_pagos()
        return jsonify({"ok": True, "status": 200, "data": pago})

    except Exception as ex:
        print(ex)
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )


@pago.route("/<id>")
def get_pago(id):
    try:
        pago = PagoModel.get_pago(id)
        if pago != None:
            return jsonify({"ok": True, "status": 200, "data": pago})
        else:
            return (
                jsonify(
                    {
                        "ok": False,
                        "status": 404,
                        "data": {"message": "Pago no encontrado"},
                    }
                ),
                404,
            )

    except Exception as ex:
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )


@pago.route("/add", methods=["POST"])
def add_pago():

    try:
        cedula_estudiante = request.json['cedula_estudiante']
        descripcion = request.json["descripcion"]
        metodo_pago = request.json['metodo']
        monto = request.json['monto']
        fecha_pago = request.json['fecha_pago']
        referencia_transferencia = request.json.get('referencia_transferencia', None)
        
        metodo = Metodo(None, metodo_pago, descripcion)
        metodo_id = MetodoModel.add_metodo(metodo)

        monto = Monto(None, descripcion, monto)
        monto_id = MountModel.add_monto(monto)
        id_trans = None
        if referencia_transferencia is not None:
            transf = Transferencia(None, str(referencia_transferencia))
            id_trans = TransferenciaModel.add_transferencia(transf)

        pago = Pago(None, cedula_estudiante, metodo_id,monto_id, fecha_pago, id_trans)
        pagos, id_pago = PagoModel.add_pago(pago)

        if pagos == 1:
             return jsonify({"ok": True, "status":200,"data":{"pagoId": id_pago}})
        else:
            return jsonify({"ok": False, "status":500,"data":None}), 500
    
    except Exception as ex:
        print(ex)
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )

@pago.route("/update/<id>", methods=["PUT"])
def update_pago(id):
    try:

        cedula_estudiante = request.json['cedula_estudiante']
        metodo_pago_id = request.json['metodo_pago_id']
        monto_id = request.json['monto_id']
        fecha_pago = request.json['fecha_pago']
        referencia_transferencia = request.json[' referencia_transferencia']
      

        pago = (str(id),cedula_estudiante,metodo_pago_id,monto_id,fecha_pago,referencia_transferencia)
        pagos = PagoModel.update_pago(pago)

        if pagos == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return (
                jsonify(
                    {
                        "ok": False,
                        "status": 500,
                        "data": {"message": "Error al actualizar, compruebe los datos ingresados"},
                    }
                ),
                500,
            )

    except Exception as ex:
        print(ex)
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )


# @pago.route("/count/month/<number>", methods=["GET"])
# def count_month(number):
#     try:
#         count = pagoModel.count_month(number)
#         return jsonify({"ok": True, "status": 200, "total": count})
#     except Exception as ex:
#         return (
#             jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
#             500,
#         )


# @pago.route("/count/day/<number>", methods=["GET"])
# def count_day(number):
#     try:
#         count = pagoModel.count_day(number)
#         return jsonify({"ok": True, "status": 200, "total": count})
#     except Exception as ex:
#         return (
#             jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
#             500,
#         )
