from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from settings import settings
from routes import students, admin, usuario, docente, carreras, materias, billete, coordinacion, control, peticiones, \
    config, files,generar,SuperUsuario,transferencia

app = Flask(__name__)

t = 0
def create_app(config_filename):
    app.config.from_object(config_filename)
    global t
    if t == 0:
        # blueprints
        jwt = JWTManager(app)
        app.register_blueprint(students.main, url_prefix='/api/students')
        app.register_blueprint(admin.admin, url_prefix='/api/admin')
        app.register_blueprint(usuario.user, url_prefix='/api/usuario')
        app.register_blueprint(docente.doc, url_prefix='/api/docente')
        app.register_blueprint(carreras.carrera, url_prefix='/api/carreras')
        app.register_blueprint(materias.materia, url_prefix='/api/materias')
        app.register_blueprint(billete.billete, url_prefix='/api/billetes')
        app.register_blueprint(coordinacion.coordinacion, url_prefix='/api/coordinacion')
        app.register_blueprint(control.control, url_prefix='/api/control')
        app.register_blueprint(peticiones.peticion, url_prefix='/api/peticiones')
        app.register_blueprint(config.config, url_prefix='/api/config')
        app.register_blueprint(files.files, url_prefix='/api/archivos')
        app.register_blueprint(generar.generar_pdf,url_prefix = '/api/generar_ficha')
        app.register_blueprint(SuperUsuario.superUs,url_prefix = '/api/superUsuario')
        app.register_blueprint(transferencia.transf, url_prefix = 'api/transferencias')
        # manejador de errores
        app.register_error_handler(404, page_not_found)
        t = 1
    return app


def page_not_found(error):
    return jsonify({"ok": False, "status": 404, "data": {"message": "Page not found"}}), 404


PresentConfig = settings['development']
app = create_app(PresentConfig)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
