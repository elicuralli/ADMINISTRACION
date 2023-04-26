from flask import Flask
from config import config
from routes import students,admin, monto

app = Flask(__name__)

def page_not_found(error):
    return '<h1>page not found!</h1>',404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    
    # acceso fuera desde otras url

    # blueprints
    app.register_blueprint(students.main, url_prefix = '/api/students')
    app.register_blueprint(admin.admin, url_prefix = '/api/admin')
    app.register_blueprint(monto.montos, url_prefix = '/api/monto')
    #manejador de errores
    app.register_error_handler(404,page_not_found)
    app.run()