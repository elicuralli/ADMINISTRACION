from models.entities.transferencias import Transferencia
from database.db import get_connection

class TransferenciaModel():

    @classmethod
    def get_transferencias(self):

        try: 
                conection = get_connection()
                transferencias = []

                with conection.cursor() as cursor: 
                    cursor.execute("SELECT * from transferencias")
                    result = cursor.fetchall()

                    for row in result: 
                        transferencia = Transferencia(row[0],row[1], row[2])
                        transferencias.append(transferencia.to_JSON())
                        
                
                conection.close()
                return transferencias

        except Exception as ex:
                raise Exception(ex)
    
    @classmethod
    def get_transferencia(self,id: str):
         
        try:
            
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM transferencias WHERE id =%s",(id,))
                result = cursor.fetchone()

                if result is not None:
                     
                       transferencia = Transferencia(id=result[0],codigo_referencia=result[1], metodo_pago=result[2])
                       transferencias = transferencia.to_JSON()
                    
                        
                else:
                    raise Exception("transferencia no existe")

            
            conection.close()
            return transferencias

             
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_transferencia(self,transferencia: Transferencia):
         
        try:
            
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO transferencias (id,codigo_referencia,metodo_pago)VALUES(%s,%s,%s)",(transferencia.id,transferencia.codigo_referencia,transferencia.metodo_pago))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_transferencia(self, transferencia):
    
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE transferencias SET codigo_referencia = %s,metodo_pago = %s WHERE id = %s ",(transferencia.codigo_referencia,transferencia.metodo_pago,transferencia.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

