from models.entities.billete import Billete
from database.db import get_connection 


class BilleteModel():

    @classmethod
    def get_billetes(self):

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
    def get_billete(self,codigo: str):
         
        try:
            
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM billete WHERE codigo =%s",(codigo,))
                result = cursor.fetchone()

                if result is not None:
                     
                        billete = Billete(codigo=result[0], cantidad=result[1], factura=result[2])
                        billetes = billete.to_JSON()
                    
                        
                else:
                    raise Exception("Billete no existe")

            
            conection.close()
            return billetes

             
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_billete(self,billete: Billete):
         
        try:
            
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO billete (codigo,cantidad,factura)VALUES(%s,%s,%s)",(billete.codigo,billete.cantidad,billete.factura))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_billete(self, billete):
    
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE billete SET cantidad = %s WHERE codigo = %s ",(billete.cantidad,billete.codigo))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

