from flask import Blueprint,jsonify,render_template,send_file
from models.studentsmodel import StudentModel
from models.carreramodel import CarreraModel
from models.materiamodel import MateriaModel
from datetime import date
import pdfkit
import io
import traceback

generar_pdf = Blueprint('generar_blueprint',__name__)
@generar_pdf.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response



@generar_pdf.route('/<cedula>')
def generar(cedula):

    BINPATH = "/usr/bin/wkhtmltopdf"

    try:
        student = StudentModel.get_student(cedula)
        if student != None:
            notas = StudentModel.get_materias_inscritas(cedula)
            carrera = CarreraModel.get_carrera(student["carrera"])
            print(carrera)
            config = pdfkit.configuration(wkhtmltopdf=BINPATH)

            student["carrera"] = carrera["nombre"]
            fecha_actual = date.today().strftime("%d/%m/%Y")
            res = render_template('fichaEstudiantes.html',student=student,materias=notas["contenido"], fecha_actual = fecha_actual)
            pdf = pdfkit.from_string(res, configuration=config, options={"enable-local-file-access": True})
            # Crear un objeto BytesIO y establecer el PDF generado como su contenido
            pdf_blob = io.BytesIO(pdf)

            # Establecer las cabeceras de la respuesta
            return send_file(path_or_file=pdf_blob, download_name="ficha_estudiantil.pdf", as_attachment=True)
            
        
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Estudiante no encontrado"}}),404
        
    
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}),500

@generar_pdf.route('/docenteria')
def docenteria():

    BINPATH = "/usr/bin/wkhtmltopdf"

    try:
        join = MateriaModel.get_docenteria()
        if join != None:
            config = pdfkit.configuration(wkhtmltopdf=BINPATH)
            fecha_actual = date.today().strftime("%d/%m/%Y")
            res = render_template('docenteria.html',materias=join, fecha_actual = fecha_actual)
            pdf = pdfkit.from_string(res, configuration=config, options={"enable-local-file-access": True})
            # Crear un objeto BytesIO y establecer el PDF generado como su contenido
            pdf_blob = io.BytesIO(pdf)

            # Establecer las cabeceras de la respuesta
            return send_file(path_or_file=pdf_blob, download_name="docentes_materias.pdf", as_attachment=True)
            
        
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Estudiante no encontrado"}}),404
        
    
    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": str(ex)}),500