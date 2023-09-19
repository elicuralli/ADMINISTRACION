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
                    coordinador = coordinador.to_JSON()
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
                cursor.execute("UPDATE coordinacion SET fullname =%s,correo =%s,telefono=%s,password=%s WHERE cedula =%s",(coordinador.fullname,coordinador.correo,coordinador.telefono,coordinador.password,coordinador.cedula))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            print(ex)
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
    def login(self,coordinador: Coordinacion):
        try:

            conection = get_connection()
            coord: Coordinacion
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from coordinacion WHERE correo =%s",(coordinador.correo,))
                row = cursor.fetchone()

                if row is not None:
                    coord = Coordinacion(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                else:
                    return None

            conection.close()
            return coord
        
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def calcular_promedio_ponderado_estudiante(cls, cedula_estudiante):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                # Obtener todas las materias cursadas por el estudiante
                cursor.execute("SELECT nota, unidad_credito FROM notas WHERE cedula_estudiante = %s", (cedula_estudiante,))
                registros = cursor.fetchall()

                if registros:
                    total_puntos = 0.0
                    total_unidades_credito = 0.0

                    for nota, unidad_credito in registros:
                        total_puntos += nota * unidad_credito
                        total_unidades_credito += unidad_credito

                    if total_unidades_credito > 0:
                        promedio_ponderado = total_puntos / total_unidades_credito
                    else:
                        promedio_ponderado = 0  # Evitar división por cero si el estudiante no tiene notas

                    conection.close()
                    return promedio_ponderado

                else:
                    conection.close()
                    return None  # El estudiante no tiene notas registradas

        except Exception as ex:
            raise Exception(ex)