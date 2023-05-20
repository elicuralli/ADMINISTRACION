from database.db import get_connection
from models.entities.metodo import Metodo

class MetodoModel():

    @classmethod
    def get_metodos(self):
        try:
            conection = get_connection()
            metodos = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from metodo_pago ORDER BY id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    metodo = Metodo(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
                    metodos.append(metodo.to_JSON())
            
            conection.close()
            return metodos

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_metodo(self,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM metodo_pago WHERE id = %s",(id,))
                row = cursor.fetchone()

                if row != None:
                    metodo = Metodo(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
                
            conection.close()
            return metodo

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_metodo(self,metodo: Metodo):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO metodo_pago (pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5,id_pago) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(metodo.id_pago,metodo.pre_inscripcion,metodo.inscripcion,metodo.cuota1,metodo.cuota2,metodo.cuota3,metodo.cuota4,metodo.cuota5))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def update_metodo(self,metodo: Metodo):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE metodo_pago SET pre_inscripcion=%s,inscripcion=%s,cuota1=%s,cuota2=%s,cuota3=%s,cuota4=%s,cuota5=%s,id_pago = %s WHERE id = %s""",(metodo.pre_inscripcion,metodo.inscripcion,metodo.cuota1,metodo.cuota2,metodo.cuota3,metodo.cuota4,metodo.cuota5, metodo.id_pago,metodo.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
        