from database.db import get_connection
from models.entities.user import User

class UserModel():

    @classmethod
    def register(self,user):
        try: 
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("""INSERT into usuarios (usuario, clave) VALUES (%s,%s)""",(user.usuario,user.clave,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def login(self,user):
        try:

            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("SELECT clave FROM usuarios WHERE usuario=%s",(user.usuario,)) 
                row = cursor.fetchone()
                conection.commit()

            conection.close()
            return row[0]
        
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



