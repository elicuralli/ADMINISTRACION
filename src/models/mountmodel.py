from database.db import get_connection 
from models.entities.monto import Monto
from models.entities.administracion import Administracion

class MountModel():

    @classmethod
    def get_montos(self):
        try:
            conection = get_connection()
            montos = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from monto ORDER BY id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    monto = Monto(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    montos.append(monto.to_JSON())
            
            conection.close()
            return montos

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_monto(self,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM monto INNER JOIN pagos ON pagos.id = monto.id_pago WHERE monto.id = %s",(id,))
                row = cursor.fetchone()

                join = None
                if row != None:
                    monto = Monto(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    pagos = Administracion(row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17])
                    join = {"pagos":pagos.to_JSON(), "montos": monto.to_JSON()}

                
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_monto(self,monto: Monto):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO monto (id_pago,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(monto.id_pago,monto.pre_inscripcion,monto.inscripcion,monto.cuota1,monto.cuota2,monto.cuota3,monto.cuota4,monto.cuota5))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def update_monto(self,monto: Monto):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE monto SET id_pago=%s,pre_inscripcion=%s,inscripcion=%s,cuota1=%s,cuota2=%s,cuota3=%s,cuota4=%s,cuota5=%s WHERE id_pago=%s""",(monto.id_pago,monto.pre_inscripcion,monto.inscripcion,monto.cuota1,monto.cuota2,monto.cuota3,monto.cuota4,monto.cuota5, monto.id_pago))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
        