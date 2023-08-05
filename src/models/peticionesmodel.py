from models.entities.peticiones import Peticiones
from database.db import get_connection 

class PeticionesModel():

    @classmethod
    def get_peticiones(self):

        try:
            conection = get_connection()
            peticiones = []

            with conection.cursor() as cursor:
                    cursor.execute("SELECT * from peticiones")
                    resultset = cursor.fetchall()

                    for row in resultset:
                        peticion = Peticiones(id = row[0],id_docente= row[1],descripcion= row[2],estado = row[3],id_estudiante=row[4],id_materia=row[5],campo= row[6])
                        peticiones.append(peticion.to_JSON())
                
            conection.close()
            return peticiones 

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_peticion(self,id: str):
         
         try:
            
            conection = get_connection()
            peticiones = None

            with conection.cursor() as cursor:
                    cursor.execute("SELECT * from peticiones WHERE id=%s",(id,))
                    row = cursor.fetchone()

                    if row is not None:
                        peticion = Peticiones(id = row[0],id_docente= row[1],descripcion= row[2],estado = row[3],id_estudiante=row[4],id_materia=row[5],campo= row[6])
                        peticiones = peticion.to_JSON()
                
            conection.close()
            return peticiones 

         except  Exception as ex:
            raise Exception(ex)
         
    
    @classmethod
    def get_peticiones_pendientes(cls):
        try:
            connection = get_connection()
            peticiones_pendientes = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM peticiones WHERE estado = 'Pendiente'")
                resultset = cursor.fetchall()

                for row in resultset:
                    peticion = Peticiones(id=row[0], id_docente=row[1], descripcion=row[2],estado=row[3], id_estudiante=row[4], id_materia=row[5], campo=row[6])
                    peticiones_pendientes.append(peticion.to_JSON())

            connection.close()
            return peticiones_pendientes

        except Exception as ex:
            raise Exception(ex)
    
         
    @classmethod
    def add_peticion(self,peticion):
         
        try:
             
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO peticiones(id_docente ,descripcion ,estado ,id_estudiante ,id_materia ,campo)VALUES(%s,%s,%s,%s,%s,%s)",(peticion.id_docente ,peticion.descripcion ,peticion.estado ,peticion.id_estudiante ,peticion.id_materia ,peticion.campo))
                affected_rows = cursor.rowcount
                conection.commit()
              
            conection.close()
            return affected_rows
        

        except  Exception as ex:
            raise Exception(ex)

    # En el modelo Peticiones, modificamos la función update_peticion para permitir actualizaciones dinámicas basadas en los campos proporcionados en la solicitud.
    @classmethod
    def update_peticion(cls, peticion):
        try:
            connection = get_connection()
            fields_to_update = []
            values_to_update = []

            if peticion.id_docente:
                fields_to_update.append("id_docente = %s")
                values_to_update.append(peticion.id_docente)
            if peticion.descripcion:
                fields_to_update.append("descripcion = %s")
                values_to_update.append(peticion.descripcion)
            if peticion.estado:
                fields_to_update.append("estado = %s")
                values_to_update.append(peticion.estado)
            if peticion.id_estudiante:
                fields_to_update.append("id_estudiante = %s")
                values_to_update.append(peticion.id_estudiante)
            if peticion.id_materia:
                fields_to_update.append("id_materia = %s")
                values_to_update.append(peticion.id_materia)
            if peticion.campo:
                fields_to_update.append("campo = %s")
                values_to_update.append(peticion.campo)

            if not fields_to_update:
                return 0

            fields_to_update = ", ".join(fields_to_update)
            query = "UPDATE peticiones SET " + fields_to_update + " WHERE id = %s"
            values_to_update.append(peticion.id)

            with connection.cursor() as cursor:
                cursor.execute(query, tuple(values_to_update))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_peticion(self,peticion):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM peticiones WHERE id = %s", (peticion.id,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)