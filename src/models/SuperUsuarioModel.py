from models.entities.SuperUsuario import SuperUsuario
from database.db import get_connection


class SuperUsuarioModel():
    
    @classmethod
    def get_super_user(self,cedula: str):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM superusuario WHERE cedula =%s",(cedula,))
                result = cursor.fetchone()

                if result is not None:
                    
                        super_user = SuperUsuario(cedula=result[0],nombre=result[1],correo=result[2],password=result[3])
                        superUs = super_user.to_JSON()
                    
                else:
                    raise Exception("super usuario no existe")

            
            conection.close()
            return superUs

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_super_user(self, super_user):

        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from superusuario WHERE cedula =%s",(super_user.cedula,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'super usuario ya existe'
                cursor.execute("""INSERT INTO superusuario(cedula,nombre,correo,password)VALUES (%s,%s,%s,%s)""",(super_user.cedula,super_user.nombre,super_user.correo,super_user.password))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_super_user(self,super_user):
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                sql = cursor.execute("UPDATE superusuario SET nombre =%s,correo =%s,password=%s WHERE cedula =%s",(super_user.nombre,super_user.correo,super_user.password,super_user.cedula))
                print("SQL de actualización:", sql)
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            print( print("Error al actualizar superusuario:", ex))
            raise Exception(ex)
    
    @classmethod
    def delete_super_user(self,super_user):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM superusuario WHERE cedula = %s", (super_user.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

        

