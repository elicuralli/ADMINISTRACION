from flask import Blueprint, jsonify, request
from models.entities.pagos import Pago
from models.pagosmodel import PagoModel
from models.entities.monto import Monto
from models.mountmodel import MountModel
from models.metodomodel import MetodoModel
from models.entities.metodo import Metodo
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
        id = request.json['id']
        cedula_estudiante = request.json['cedula_estudiante']
        metodo_pago_id = request.json['metodo_pago_id']
        monto_id = request.json['monto_id']
        fecha_pago = request.json['fecha_pago']
        referencia_transferencia = request.json[' referencia_transferencia']
        referencia_billete = request.json[' referencia_billete']

        pago = (str(id),cedula_estudiante,metodo_pago_id,monto_id,fecha_pago,referencia_transferencia,referencia_billete)
        pagos = PagoModel.add_pago(pago)

        if pagos == 1:
             return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": pagos}}), 500
    
    except Exception as ex:
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
        referencia_billete = request.json[' referencia_billete']

        pago = (str(id),cedula_estudiante,metodo_pago_id,monto_id,fecha_pago,referencia_transferencia,referencia_billete)
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
