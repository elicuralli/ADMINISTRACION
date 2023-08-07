from flask import Blueprint,jsonify,render_template,send_file
from models.studentsmodel import StudentModel
from models.carreramodel import CarreraModel
from datetime import date
import pdfkit
import io

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
            notas = StudentModel.get_materias_inscritas(student["estudiante"]["cedula"])
            print(student["estudiante"])
            carrera = CarreraModel.get_carrera(student["estudiante"]["carrera"])
            config = pdfkit.configuration(wkhtmltopdf=BINPATH)

            student["estudiante"]["carrera"] = carrera["carrera"]["nombre"]
            fecha_actual = date.today().strftime("%d/%m/%Y")
            res = render_template('fichaEstudiantes.html',student=student["estudiante"],materias=notas["contenido"], fecha_actual = fecha_actual)
            pdf = pdfkit.from_string(res, configuration=config, options={"enable-local-file-access": True})
            # Crear un objeto BytesIO y establecer el PDF generado como su contenido
            pdf_blob = io.BytesIO(pdf)

            # Establecer las cabeceras de la respuesta
            return send_file(path_or_file=pdf_blob, download_name="ficha_estudiantil.pdf", as_attachment=True)
            
        
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "Estudiante no encontrado"}}),404
        
    
    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}),500
