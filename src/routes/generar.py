from flask import Blueprint,jsonify,request,url_for,make_response,render_template,send_file
from models.entities.students import Student
from models.studentsmodel import StudentModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, date
import pdfkit

generar_pdf = Blueprint('generar_blueprint',__name__)
@generar_pdf.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@generar_pdf.route('/<cedula>')
def generar(cedula):

    BINPATH = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

    try:
        student = StudentModel.get_student(cedula)
        if student != None:
            print("Datos del estudiante:", student)
            
            config = pdfkit.configuration(wkhtmltopdf=BINPATH)
            fecha_actual = date.today().strftime("%d/%m/%Y")
            res = render_template('fichaEstudiantes.html',student =student,fecha_actual = fecha_actual)
            pdf = pdfkit.from_string(res, configuration=config)
            respuesta = make_response(pdf)
            respuesta.headers['Content-Type'] = 'application/pdf'
            respuesta.headers['Content-Disposition'] = f'inline; filename=FichaEstudiantil.pdf'

       
            return respuesta
            
        
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Estudiante no encontrado"}}),404
        
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
