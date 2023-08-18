from database.db import get_connection 
from models.entities.monto import Monto
from models.entities.pagos import Pago

class MountModel():

    @classmethod
    def get_montos(cls):
        try:
            conection = get_connection()
            montos = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from monto ORDER BY id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    monto = Monto(row[0],row[1],row[2])
                    montos.append(monto.to_JSON())
            
            conection.close()
            return montos

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_monto(cls,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM montos WHERE id = %s",(id,))
                row = cursor.fetchone()

                montos = None
                if row != None:
                    monto = Monto(row[0],row[1],row[2])
                    montos.to_Json(monto)
                    
                
            conection.close()
            return montos

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_monto(cls,monto: Monto):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO montos (concepto,monto) VALUES (%s,%s) RETURNING id""",(monto.concepto,monto.monto))
                inserted_id = cursor.fetchone()[0]
            
                conection.commit()

            conection.close()
            
            # Devolver el ID recién insertado
            return inserted_id

        except  Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def update_monto(cls,monto: Monto):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE monto SET concepto =%s,monto=%s WHERE id =%s """,(monto.concepto,monto.monto,monto.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
        