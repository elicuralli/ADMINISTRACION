from models.entities.billete import Billete
from database.db import get_connection 


class BilleteModel():

    @classmethod
    def get_billetes(cls):

        try: 
                conection = get_connection()
                billetes = []

                with conection.cursor() as cursor: 
                    cursor.execute("SELECT * from billetes")
                    result = cursor.fetchall()

                    for row in result: 
                        billete = Billete(row[3],row[0], row[1], row[2])
                        billetes.append(billete.to_JSON())
                        
                
                conection.close()
                return billetes

        except Exception as ex:
                raise Exception(ex)
    
    @classmethod
    def get_billete(cls,id: str):
         
        try:
            
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM billetes WHERE id =%s",(id,))
                result = cursor.fetchone()

                if result is not None:
                     
                        billete = Billete(id=result[3], serial=result[0], monto=result[1], pago_id=result[2])
                        billetes = billete.to_JSON()
                    
                        
                else:
                    raise Exception("Billete no existe")

            
            conection.close()
            return billetes

             
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_billete(cls,billete: Billete):
         
        try:
            
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO billetes (serial,monto,pago_id)VALUES(%s,%s,%s)",(billete.serial,billete.monto,billete.pago))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_billete(cls, billete):
    
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE billetes SET monto = %s WHERE id = %s ",(billete.monto,billete.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

