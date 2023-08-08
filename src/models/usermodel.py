from database.db import get_connection
from models.entities.user import User

class UserModel():

    @classmethod
    def register(self,user):
        try: 
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("""INSERT into usuarios (usuario, nombre, clave) VALUES (%s,%s,%s)""",(user.usuario,user.nombre,user.clave,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_user(self,user):
        try:

            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("SELECT usuario, clave, id, nombre FROM usuarios WHERE usuario=%s",(user.usuario,))
                row = cursor.fetchone()
                conection.commit()
                user = User(row[0], row[1],row[2], row[3])

            conection.close()
            return user
        
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self,user: User):
        try:

            conection = get_connection()
            student: User
            with conection.cursor() as cursor:
                cursor.execute("SELECT id, usuario, nombre FROM usuarios WHERE usuario=%s",(user.usuario,))
                row = cursor.fetchone()
                conection.commit()
                if row is not None:
                    user = User(row[1], None, row[0], row[2])
                else:
                    return None

            conection.close()
            return user

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_user(self,user):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                    cursor.execute("UPDATE usuarios SET usuario=%s WHERE usuario = %s",(user.usuario)) 
                    affected_rows = cursor.rowcount
                    conection.commit()

            conection.close()
            return affected_rows
        
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_clave(self,user):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                    cursor.execute("UPDATE usuarios SET clave=%s WHERE usuario = %s",(user.clave,user.usuario)) 
                    affected_rows = cursor.rowcount
                    conection.commit()

            conection.close()
            return affected_rows
        
        except Exception as ex:
            raise Exception(ex)



