# Imports
from flask import Flask
from flask_jwt_extended import JWTManager
from config import config
from routes import students,admin,usuario,docente,carreras,materias,billete,coordinacion,control
from flask_apispec.extension import FlaskApiSpec

# Flask essentials
app = Flask(__name__)
app.config.from_object(config['development'])

jwt = JWTManager(app)
docs = FlaskApiSpec(app)

def page_not_found(error):
    return '<h1>page not found!</h1>',404

if __name__ == '__main__':
    
    # api docs
    
    # acceso fuera desde otras url

    # blueprints
    app.register_blueprint(students.main, url_prefix = '/api/students')
    app.register_blueprint(admin.admin, url_prefix = '/api/admin')
    app.register_blueprint(usuario.user, url_prefix = '/api/usuario')
    app.register_blueprint(docente.doc, url_prefix ='/api/docente' )
    app.register_blueprint(carreras.carrera, url_prefix = '/api/carreras')
    app.register_blueprint(materias.materia, url_prefix = '/api/materias')
    app.register_blueprint(billete.billete, url_prefix = '/api/billetes')
    app.register_blueprint(coordinacion.coordinacion, url_prefix = '/api/coordinacion')
    app.register_blueprint(control.control, url_prefix = '/api/control')
    
    # admin docs
    docs.register(admin.get_administracion, blueprint="administracion_blueprint")
    docs.register(admin.get_admin, blueprint="administracion_blueprint")
    docs.register(admin.add_admin, blueprint="administracion_blueprint")
    docs.register(admin.update_admin, blueprint="administracion_blueprint")
    
    # billetes docs
    docs.register(billete.get_billetes, blueprint="billete_blueprint")
    docs.register(billete.get_billete, blueprint="billete_blueprint")
    docs.register(billete.add_billete, blueprint="billete_blueprint")
    docs.register(billete.update_billete, blueprint="billete_blueprint")
    
    # carreras docs
    docs.register(carreras.get_carreras, blueprint="carrera_blueprint")
    docs.register(carreras.get_carrera, blueprint="carrera_blueprint")
    docs.register(carreras.add_carrera, blueprint="carrera_blueprint")
    docs.register(carreras.update_carrera, blueprint="carrera_blueprint")
    docs.register(carreras.delete_carrera, blueprint="carrera_blueprint")
    
    # control de estudio docs
    docs.register(control.get_todo_control, blueprint="control_es_blueprint")
    docs.register(control.get_control, blueprint="control_es_blueprint")
    docs.register(control.add_control, blueprint="control_es_blueprint")
    docs.register(control.update_control, blueprint="control_es_blueprint")
    docs.register(control.delete_control, blueprint="control_es_blueprint")
    
    # coordinacion docs
    docs.register(coordinacion.get_coordinadores,blueprint="coordinacion_blueprint")
    docs.register(coordinacion.get_coordinador,blueprint="coordinacion_blueprint")
    docs.register(coordinacion.add_coordinador,blueprint="coordinacion_blueprint")
    docs.register(coordinacion.update_coordinador,blueprint="coordinacion_blueprint")
    docs.register(coordinacion.delete_coordinador,blueprint="coordinacion_blueprint")
    docs.register(coordinacion.login,blueprint="coordinacion_blueprint")
    docs.register(coordinacion.jwt_coordinador,blueprint="coordinacion_blueprint")
    
    # docente docs
    docs.register(docente.get_docentes,blueprint="docentes_blueprint")
    docs.register(docente.get_docente,blueprint="docentes_blueprint")
    docs.register(docente.add_docente,blueprint="docentes_blueprint")
    docs.register(docente.update_docente,blueprint="docentes_blueprint")
    docs.register(docente.delete_docente,blueprint="docentes_blueprint")
    docs.register(docente.login,blueprint="docentes_blueprint")
    docs.register(docente.jwt_docente,blueprint="docentes_blueprint")
    
    # materias docs
    docs.register(materias.get_materias, blueprint="materia_blueprint")
    docs.register(materias.get_materia, blueprint="materia_blueprint")
    docs.register(materias.add_materia, blueprint="materia_blueprint")
    docs.register(materias.update_materia, blueprint="materia_blueprint")
    docs.register(materias.delete_materia, blueprint="materia_blueprint")
    
    # students docs
    docs.register(students.get_students,blueprint="students_blueprint")
    docs.register(students.get_student,blueprint="students_blueprint")
    docs.register(students.add_student,blueprint="students_blueprint")
    docs.register(students.update_student,blueprint="students_blueprint")
    docs.register(students.delete_student,blueprint="students_blueprint")
    docs.register(students.login,blueprint="students_blueprint")
    docs.register(students.jwt_student,blueprint="students_blueprint")

    #manejador de errores
    app.register_error_handler(404,page_not_found)
    app.run(host="0.0.0.0", debug=True)
    
    