# IMPORTS
from flask import Blueprint, jsonify, request
from models.entities.administracion import Administracion
from models.adminmodel import AdminModel
from models.entities.monto import Monto
from models.mountmodel import MountModel
from models.metodomodel import MetodoModel
from models.entities.metodo import Metodo

# Blueprint
admin = Blueprint("administracion_blueprint", __name__)

# Routes

@admin.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


@admin.route("/", methods=["GET"], provide_automatic_options=False)
def get_administracion():
    try:
        admin = AdminModel.get_administracion()
        return jsonify({"ok": True, "status": 200, "data": admin})

    except Exception as ex:
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )


@admin.route("/<id>", methods=["GET"], provide_automatic_options=False)
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


@admin.route("/add", methods=["POST"], provide_automatic_options=False)
def add_admin():
    try:
        pre_inscripcion = request.json["pre_inscripcion"]
        metodo_pre_inscripcion = request.json["metodo_pre_inscripcion"]
        inscripcion = ""
        metodo = ""
        cedula_student = request.json["cedula_student"]
        cuota1 = ""
        metodo = ""
        cuota2 = ""
        metodo = ""
        cuota3 = ""
        metodo = ""
        cuota4 = ""
        metodo = ""
        cuota5 = ""
        metodo = ""
        monto_pre_inscripcion = request.json["monto_pre_inscripcion"]
        monto_inscripcion = 0.0
        monto_cuota1 = 0.0
        monto_cuota2 = 0.0
        monto_cuota3 = 0.0
        monto_cuota4 = 0.0
        monto_cuota5 = 0.0
        metodo_inscripcion = ""
        metodo_cuota1 = ""
        metodo_cuota2 = ""
        metodo_cuota3 = ""
        metodo_cuota4 = ""
        metodo_cuota5 = ""

        
        if "inscripcion" in request.json:
            inscripcion = request.json["inscripcion"]
            metodo_inscripcion = request.json["metodo_inscripcion"]
            monto_inscripcion = request.json["monto_inscripcion"]
            
        if "cuota1" in request.json:
            cuota1 = request.json["cuota1"]
            metodo_cuota1 = request.json["metodo_cuota1"]
            monto_cuota1 = request.json["monto_cuota1"]
        
        if "cuota2" in request.json:
            cuota2 = request.json["cuota2"]
            metodo_cuota2 = request.json["metodo_cuota2"]
            monto_cuota2 = request.json["monto_cuota2"]
            
        if "cuota3" in request.json:
            cuota3 = request.json["cuota3"]
            metodo_cuota3 = request.json["metodo_cuota3"]
            monto_cuota3 = request.json["monto_cuota3"]
        
        if "cuota4" in request.json:
            cuota4 = request.json["cuota4"]
            metodo_cuota4 = request.json["metodo_cuota4"]
            monto_cuota4 = request.json["monto_cuota4"]
        
        if "cuota5" in request.json:
            cuota5 = request.json["cuota5"]
            metodo_cuota5 = request.json["metodo_cuota5"]
            monto_cuota5 = request.json["monto_cuota5"]

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
        metodo = Metodo(None,metodo_pre_inscripcion,metodo_inscripcion,metodo_cuota1,metodo_cuota2,metodo_cuota3,metodo_cuota4,metodo_cuota5,str(id_pago))
        affected_rows = MountModel.add_monto(monto)
        affected_rows_metodo = MetodoModel.add_metodo(metodo)
        
        
        if affected_rows == 1 and affected_rows_metodo == 1:
            return jsonify({"ok": True, "status": 200, "data": id_pago})
    
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
        print(ex)
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )


@admin.route("/update/<id>", methods=["PUT"], provide_automatic_options=False)
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
        
        monto_pre_inscripcion = request.json["monto_pre_inscripcion"]
        monto_inscripcion = request.json["monto_inscripcion"]
        monto_cuota1 = request.json["monto_cuota1"]
        monto_cuota2 = request.json["monto_cuota2"]
        monto_cuota3 = request.json["monto_cuota3"]
        monto_cuota4 = request.json["monto_cuota4"]
        monto_cuota5 = request.json["monto_cuota5"]

        metodo_pre_inscripcion = request.json["metodo_pre_inscripcion"]
        metodo_inscripcion = request.json["metodo_inscripcion"]
        metodo_cuota1 = request.json["metodo_cuota1"]
        metodo_cuota2 = request.json["metodo_cuota2"]
        metodo_cuota3 = request.json["metodo_cuota3"]
        metodo_cuota4 = request.json["metodo_cuota4"]
        metodo_cuota5 = request.json["metodo_cuota5"]


        affected_rows = AdminModel.update_admin(admin)
        monto = Monto(None, str(id), monto_pre_inscripcion, monto_inscripcion, monto_cuota1, monto_cuota2, monto_cuota3, monto_cuota4, monto_cuota5)
        metodo = Metodo(str(id),metodo_pre_inscripcion,metodo_inscripcion,metodo_cuota1,metodo_cuota2,metodo_cuota3,metodo_cuota4,metodo_cuota5)
        MountModel.update_monto(monto)
        affected_rows = MetodoModel.update_metodo(metodo)

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
        print(ex)
        return (
            jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}),
            500,
        )