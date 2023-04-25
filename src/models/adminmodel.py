from database.db import get_connection 
from models.entities.administracion import Administracion

class AdminModel():

    @classmethod
    def get_administracion(self):
        try:
            conection = get_connection()
            administracion = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT id,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5 from administracion ORDER BY id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    admin = Administracion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                    administracion.append(admin.to_JSON())
            
            conection.close()
            return administracion

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_administracion_id(self,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT id,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5 from administracion WHERE id = %s",(id,))
                row = cursor.fetchone()

                admin = None
                if row != None:
                    admin = Administracion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                    administracion = admin.to_JSON()

                
            conection.close()
            return administracion

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_admin(self,administracion):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO administracion (id,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(administracion.id,administracion.pre_inscripcion,administracion.inscripcion,administracion.cuota1,administracion.cuota2,administracion.cuota3,administracion.cuota4,administracion.cuota5))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

    