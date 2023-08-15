from models.entities.billete import Billete
from database.db import get_connection 


class BilleteModel():

    @classmethod
    def get_billetes(cls):

        try: 
                conection = get_connection()
                billetes = []

                with conection.cursor() as cursor: 
                    cursor.execute("SELECT * from billete")
                    result = cursor.fetchall()

                    for row in result: 
                        billete = Billete(row[0],row[1], row[2])
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
                cursor.execute("SELECT *FROM billete WHERE id =%s",(id,))
                result = cursor.fetchone()

                if result is not None:
                     
                        billete = Billete(id=result[0], serial=result[1], monto=result[2])
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
                cursor.execute("INSERT INTO billete (id,serial,monto)VALUES(%s,%s,%s)",(billete.id,billete.serial,billete.monto))
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
                cursor.execute("UPDATE billete SET monto = %s WHERE id = %s ",(billete.monto,billete.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

