from database.db import get_connection
from models.entities.user import User

class UserModel():

    @classmethod
    def register(self,user):
        try: 
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("""INSERT into usuario (id,usuario,clave)VALUES(%s,%s,%s)""",(user.id,user.usuario,user.clave))
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
                cursor.execute("SELECT usuario,clave FROM usuario WHERE usuario=%s, clave=%s",(user.usuario,user.clave)) 
                row = cursor.fetchone()
                conection.commit()

            conection.close()
            return row
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_user(self,user):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                    cursor.execute("UPDATE usuario SET usuario=%s WHERE usuario = %s",(user.usuario)) 
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
                    cursor.execute("UPDATE usuario SET clave=%s WHERE clave = %s",(user.clave)) 
                    affected_rows = cursor.rowcount
                    conection.commit()

            conection.close()
            return affected_rows
        
        except Exception as ex:
            raise Exception(ex)



