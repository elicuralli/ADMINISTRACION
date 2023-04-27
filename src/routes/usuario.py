from flask import Blueprint,jsonify,request
from models.entities.user import User
from models.usermodel import UserModel
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user_blueprint',__name__)

@user.route('/register', methods = ["POST"])
def register():
    try:
        id = request.json["id"]
        usuario = request.json['usuario']
        clave = generate_password_hash(request.json["clave"], method="sha256")

        user = (str(id),usuario,clave)
        affected_rows = UserModel.register(user)

        
        if affected_rows == 1:
            return jsonify({"register": True})
        else:
            return jsonify({"register": False}), 500

    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@user.route('/login',methods = ["GET"])
def login():
    try: 
        usuario = request.json['usuario']
        clave = request.json['clave']
        hashed_clave = UserModel.login(user)
 
        user = (usuario,clave,hashed_clave)

        if user:
            if check_password_hash(hashed_clave, clave):
                return jsonify({"login":True})
        
            else:
                return jsonify({"login": False})
        else:
            return f'usuario o clave incorrecta'


    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@user.route('/update<usuario>',methods = ["PUT"])
def update_user():
    try: 
        usuario = request.json['usuario']
        

        affected_rows = UserModel.update_user()


        if affected_rows == 1:
                return jsonify()
        else:
            return jsonify({'message': "Error on update"}), 500
        
    except Exception as ex:
        return jsonify({"message": str(ex)}),500