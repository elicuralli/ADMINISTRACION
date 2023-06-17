from database.db import get_connection
from models.entities.coordinacion import Coordinacion

class CoordinacionModel():

    @classmethod
    def get_coordinadores(self):

        try:
            conection = get_connection()
            coordinadores = []

            with conection.cursor()  as cursor:
                cursor.execute("SELECT *FROM coordinacion")
                result = cursor.fetchall()

                if result is not None:
                    for row in result:
                        coordinador = Coordinacion(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                        coordinadores.append(coordinador.to_JSON())

            conection.close()
            return coordinadores

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_coordinador(self,cedula: str):

        try:
            conection = get_connection()
            coordinador =  None

            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM coordinacion WHERE cedula= %s",(cedula,))
                row = cursor.fetchone()

                if row is not None:
                    coordinador = Coordinacion(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                    
            conection.close()
            return coordinador 


        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_coordinador(self,coordinador):

        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
               
                cursor.execute("SELECT * from coordinacion WHERE cedula =%s",(coordinador.cedula,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'coordinador ya existe'
                cursor.execute("""INSERT INTO coordinacion(cedula,fullname,correo,telefono,password)VALUES (%s,%s,%s,%s,%s)""",(coordinador.cedula,coordinador.fullname,coordinador.correo,coordinador.telefono,coordinador.password))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_coordinador(self,coordinador):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE coordinacion SET fullname =%s,correo =%s,telefono=%s,password=%s WHERE cedula =%s",coordinador.fullname,coordinador.correo,coordinador.telefono,coordinador.password,coordinador.cedula)
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_coordinador(self,coordinador):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM coordinacion WHERE cedula = %s", (coordinador.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self,coordinador: Coordinacion) -> Coordinacion:
        try:

            conection = get_connection()
            coord: Coordinacion
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from coordinacion WHERE coordinacion.correo =%s",(coordinador.correo,))
                row = cursor.fetchone()

                if row is not None:
                    coord = Coordinacion(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                else:
                    return None

            conection.close()
            return coord
        
        except Exception as ex:
            raise Exception(ex)