from flask import Blueprint,jsonify,request
from models.entities.user import User
from models.usermodel import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user_blueprint',__name__)

@user.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@user.route('/register', methods = ["POST"])
def register():
    try:
        usuario = request.json['usuario']
        clave = generate_password_hash(request.json["clave"], method="sha256")

        user = User(id=None,usuario=usuario,clave=clave)
        affected_rows = UserModel.register(user)

        
        if affected_rows == 1:
            return jsonify({"register": True})
        else:
            return jsonify({"register": False}), 500

    except Exception as ex:
        return jsonify({"register": False}),500
    
@user.route('/login',methods = ["POST"])
def login():
    try: 
        usuario = request.json['usuario']
        clave = request.json['clave']
        user = User(usuario,clave)
        hashed_clave = UserModel.login(user)

        if user:
            if check_password_hash(hashed_clave, clave):
                return jsonify({"login":True})
        
            else:
                return jsonify({"login": False}), 401
        else:
            return jsonify({"login": False}), 401


    except Exception as ex:
        return jsonify({"login": False}), 500
    
# @user.route('/update/usuario/',methods = ["PUT"])
# def update_user():
#     try: 
#         usuario = request.json['usuario']
#         nuevo = request.json['nuevo']
#         clave = request.json['clave']
#         user = User(usuario, clave)
#         hashed_clave = UserModel.login(user)
#         if hashed_clave:
#             if check_password_hash(hashed_clave, clave):
#                 user.usuario = nuevo
#                 affected_rows = UserModel.update_user(user)
#                 if affected_rows == 1:
#                     return jsonify({"successful":True})
#                 else:
#                     return jsonify({"successful": False})
#             else:
#                 return jsonify({"message": "clave incorrecta"})
#         else:
#             return jsonify({"message": "el usuario no existe"})
        
#     except Exception as ex:
#         return jsonify({"message": str(ex)}),500
    
# @user.route('/update/clave/',methods = ["PUT"])
# def update_clave():
#     try: 
#         usuario = request.json['usuario']
#         clave = request.json['clave']
#         nuevo = request.json['nuevo']
#         nuevo = generate_password_hash(nuevo, "sha256")
#         user = User(usuario, clave)
#         hashed_clave = UserModel.login(user)
#         if hashed_clave:
#             if check_password_hash(hashed_clave, clave):
#                 user = User(usuario, nuevo)
#                 affected_rows = UserModel.update_user(user)
#                 if affected_rows == 1:
#                     return jsonify({"successful":True})
#                 else:
#                     return jsonify({"successful": False})
#             else:
#                 return jsonify({"message": "clave incorrecta"})
#         else:
#             return jsonify({"message": "el usuario no existe"})
        
#     except Exception as ex:
#         return jsonify({"message": str(ex)}),500