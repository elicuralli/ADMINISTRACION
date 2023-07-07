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
                        peticion = Peticiones(id = row[0],id_docente= row[1],descripcion= row[2],destino= row[3],estado = row[4],id_estudiante=row[5],id_materia=row[6],campo= row[7])
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
                        peticion = Peticiones(id = row[0],id_docente= row[1],descripcion= row[2],destino= row[3],estado = row[4],id_estudiante=row[5],id_materia=row[6],campo= row[7])
                        peticiones = peticion.to_JSON()
                
            conection.close()
            return peticiones 

         except  Exception as ex:
            raise Exception(ex)
         
    @classmethod
    def add_peticion(self,peticion):
         
        try:
             
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO peticiones(id,id_docente ,descripcion ,destino ,estado ,id_estudiante ,id_materia ,campo)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(peticion.id,peticion.id_docente ,peticion.descripcion ,peticion.destino ,peticion.estado ,peticion.id_estudiante ,peticion.id_materia ,peticion.campo))
                affected_rows = cursor.rowcount
                conection.commit()
              
            conection.close()
            return affected_rows
        

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_peticion(self,peticion):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE peticiones SET id_docente=%s ,descripcion=%s ,destino=%s ,estado=%s ,id_estudiante=%s ,id_materia=%s ,campo=%s WHERE id = %s",(peticion.id_docente ,peticion.descripcion ,peticion.destino ,peticion.estado ,peticion.id_estudiante ,peticion.id_materia ,peticion.campo,peticion.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
            
    
        except  Exception as ex:
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