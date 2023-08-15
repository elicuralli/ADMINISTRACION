from database.db import get_connection
from models.entities.metodo import Metodo

class MetodoModel():

    @classmethod
    def get_metodos(cls):
        try:
            conection = get_connection()
            metodos = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from metodo_pago ORDER BY id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    metodo = Metodo(row[0],row[1],row[2])
                    metodos.append(metodo.to_JSON())
            
            conection.close()
            return metodos

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_metodo(cls,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM metodo_pago WHERE id = %s",(id,))
                row = cursor.fetchone()

                if row != None:
                    metodo = Metodo(row[0],row[1],row[2])
                
            conection.close()
            return metodo

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_metodo(cls,metodo: Metodo):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO metodo_pago (id,nombre,descripcion)VALUES(%s,%s,%s)""" ,(metodo.id,metodo.nombre,metodo.descripcion))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def update_metodo(cls,metodo: Metodo):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE metodo_pago SET nombre = %s,descripcion =%s WHERE id = %s""",(metodo.nombre,metodo.descripcion,metodo.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
        