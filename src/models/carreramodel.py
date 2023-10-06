from models.entities.carreras import Carrera
from database.db import get_connection 
from models.entities.materias import Materias

class CarreraModel():

    @classmethod
    def get_carreras(self):

        try:
            conection = get_connection()
            join = {"carreras":[]}

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from carreras")
                result = cursor.fetchall()

                for row in result:
                    carreras = Carrera(id = row[0], nombre = row[1])
                    join["carreras"].append(carreras.to_JSON())

            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_carrera(self,id: str):

        try:

            conection = get_connection()
            join = {"carrera":{},"materias": []}
                

            with conection.cursor() as cursor:
                cursor.execute("SELECT *from carreras INNER JOIN materias ON carreras.id = materias.id_carrera WHERE carreras.id=%s", (id,))
                result = cursor.fetchall()


                if result is not None:
                    
                    for row in result:
                        carreras = Carrera(id = row[0], nombre= row[1])
                        materias = Materias(id = row[2], nombre = row[3],prelacion= row[4], unidad_credito=row[5],hp=row[6],ht=row[7],semestre=row[8],id_carrera=row[9],dia = row[10],hora_inicio = row[11],hora_fin = row[12])
                        join["carrera"] = carreras.to_JSON()
                        join["materias"].append(materias.to_JSON())
                
                else: 
                    return 'no existe'
                    
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)


    @classmethod
    def add_carrera(self,carrera):

        try:

            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera.id,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'carrera ya existe'
                cursor.execute("INSERT INTO carreras(id, nombre)VALUES(%s,%s)",(carrera.id,carrera.nombre))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_carrera(self, carrera):
    
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE carreras SET nombre = %s WHERE id = %s ", (carrera.nombre,carrera.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_carrera(self,carrera):
        try:
                
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute(" DELETE FROM carreras WHERE id =%s", (carrera.id,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
                
        except  Exception as ex:
                    raise Exception(ex)
