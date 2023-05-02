from flask import Blueprint, jsonify, request
from models.entities.administracion import Administracion
from models.adminmodel import AdminModel
from models.entities.monto import Monto
from models.mountmodel import MountModel
admin = Blueprint("administracion_blueprint", __name__)


@admin.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


@admin.route("/")
def get_administracion():
    try:
        admin = AdminModel.get_administracion()
        return jsonify({"ok": True, "status": 200, "data": admin})

    except Exception as ex:
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )


@admin.route("/<id>")
def get_admin(id):
    try:
        admin = AdminModel.get_administracion_id(id)
        if admin != None:
            return jsonify({"ok": True, "status": 200, "data": admin})
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


@admin.route("/add", methods=["POST"])
def add_admin():
    try:
        pre_inscripcion = request.json["pre_inscripcion"]
        inscripcion = ""
        cedula_student = request.json["cedula_student"]
        cuota1 = ""
        cuota2 = ""
        cuota3 = ""
        cuota4 = ""
        cuota5 = ""
        monto_pre_inscripcion = request.json["montoPreInscripcion"]
        monto_inscripcion = 0.0
        monto_cuota1 = 0.0
        monto_cuota2 = 0.0
        monto_cuota3 = 0.0
        monto_cuota4 = 0.0
        monto_cuota5 = 0.0
        
        if "inscripcion" in request.json:
            inscripcion = request.json["inscripcion"]
            monto_inscripcion = request.json["montoInscripcion"]
            
        if "cuota1" in request.json:
            cuota1 = request.json["cuota1"]
            monto_cuota1 = request.json["montoCuota1"]
        
        if "cuota2" in request.json:
            cuota2 = request.json["cuota2"]
            monto_cuota2 = request.json["montoCuota2"]
            
        if "cuota3" in request.json:
            cuota3 = request.json["cuota3"]
            monto_cuota3 = request.json["montoCuota3"]
        
        if "cuota4" in request.json:
            cuota4 = request.json["cuota4"]
            monto_cuota4 = request.json["montoCuota4"]
        
        if "cuota5" in request.json:
            cuota5 = request.json["cuota5"]
            monto_cuota5 = request.json["montoCuota5"]

        admin = Administracion(
            None,
            str(cedula_student),
            pre_inscripcion,
            inscripcion,
            cuota1,
            cuota2,
            cuota3,
            cuota4,
            cuota5,
        )

        id_pago = AdminModel.add_admin(admin)
        monto = Monto(None, str(id_pago), monto_pre_inscripcion, monto_inscripcion, monto_cuota1, monto_cuota2, monto_cuota3, monto_cuota4, monto_cuota5)
        affected_rows = MountModel.add_monto(monto)
        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": affected_rows})
        else:
            return (
                jsonify(
                    {
                        "ok": False,
                        "status": 500,
                        "data": {"message": "Error al insertar, compruebe si insertó datos correctos"},
                    }
                ),
                500,
            )

    except Exception as ex:
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": "Error al insertar, compruebe si insertó datos correctos"}}),
            500,
        )


@admin.route("/update/<id>", methods=["PUT"])
def update_admin(id):
    try:
        pre_inscripcion = request.json["pre_inscripcion"]
        inscripcion = request.json["inscripcion"]
        cedula_student = request.json["cedula_student"]
        cuota1 = request.json["cuota1"]
        cuota2 = request.json["cuota2"]
        cuota3 = request.json["cuota3"]
        cuota4 = request.json["cuota4"]
        cuota5 = request.json["cuota5"]

        admin = Administracion(
            str(id),
            str(cedula_student),
            pre_inscripcion,
            inscripcion,
            cuota1,
            cuota2,
            cuota3,
            cuota4,
            cuota5,
        )
        
        monto_pre_inscripcion = request.json["montoPreInscripcion"]
        monto_inscripcion = request.json["montoInscripcion"]
        monto_cuota1 = request.json["montoCuota1"]
        monto_cuota2 = request.json["montoCuota2"]
        monto_cuota3 = request.json["montoCuota3"]
        monto_cuota4 = request.json["montoCuota4"]
        monto_cuota5 = request.json["montoCuota5"]

        affected_rows = AdminModel.update_admin(admin)
        monto = Monto(None, str(id), monto_pre_inscripcion, monto_inscripcion, monto_cuota1, monto_cuota2, monto_cuota3, monto_cuota4, monto_cuota5)

        affected_rows = MountModel.update_monto(monto)
        if affected_rows == 1:
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
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": "Error al actualizar, compruebe los datos ingresados"}}),
            500,
        )


# @admin.route("/count/month/<number>", methods=["GET"])
# def count_month(number):
#     try:
#         count = AdminModel.count_month(number)
#         return jsonify({"ok": True, "status": 200, "total": count})
#     except Exception as ex:
#         return (
#             jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
#             500,
#         )


# @admin.route("/count/day/<number>", methods=["GET"])
# def count_day(number):
#     try:
#         count = AdminModel.count_day(number)
#         return jsonify({"ok": True, "status": 200, "total": count})
#     except Exception as ex:
#         return (
#             jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
#             500,
#         )
