from flask import Flask
from config import config
from routes import students,admin,usuario,docente,carreras,materias,billete

app = Flask(__name__)

def page_not_found(error):
    return '<h1>page not found!</h1>',404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    
    # acceso fuera desde otras url

    # blueprints
    app.register_blueprint(students.main, url_prefix = '/api/students')
    app.register_blueprint(admin.admin, url_prefix = '/api/admin')
    app.register_blueprint(usuario.user, url_prefix = '/api/usuario')
    app.register_blueprint(docente.doc, url_prefix ='/api/docente' )
    app.register_blueprint(carreras.carrera, url_prefix = '/api/carreras')
    app.register_blueprint(materias.materia, url_prefix = '/api/materias')
    app.register_blueprint(billete.billete, url_prefix = '/api/billetes')
    #manejador de errores
    app.register_error_handler(404,page_not_found)
    app.run(host="0.0.0.0", debug=True)