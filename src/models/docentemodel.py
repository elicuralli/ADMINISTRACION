from database.db import get_connection 
from models.entities.docente import Docente

class DocenteModel():

    @classmethod
    def get_docentes(self):
        try:
            conection = get_connection()
            docentes = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from docentes ORDER BY cedula ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    docente = Docente(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],asignatura=row[4],password= row[5])
                    docentes.append(docente.to_JSON())
            
            conection.close()
            return docentes

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_docente(self,cedula :str):
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from docentes WHERE cedula =%s",(cedula,))
                row = cursor.fetchone()

                if row is not None:
                    docente = Docente(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],asignatura=row[4],password=row[5])
                    docentes = docente.to_JSON()
                else: 
                    return 'no existe'
                    
            
            conection.close()
            return docentes

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_docente(self,docente):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
               
                cursor.execute("SELECT * from docentes WHERE cedula =%s",(docente.cedula,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'docente ya existe'
                cursor.execute("""INSERT INTO docentes(cedula,fullname,correo,telefono,asignatura,password)VALUES (%s,%s,%s,%s,%s,%s)""",(docente.cedula,docente.fullname,docente.correo,docente.telefono,docente.asignatura,docente.password))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_docente(self,docente):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE docentes SET fullname =%s,correo =%s,telefono=%s,asignatura =%s,password=%s WHERE cedula =%s""", (docente.fullname,docente.correo,docente.telefono,docente.asignatura,docente.password,docente.cedula))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_docente(self,docente):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM docentes WHERE cedula = %s", (docente.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)