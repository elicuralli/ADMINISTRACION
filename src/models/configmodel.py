from models.entities.config import Configuracion
from database.db import get_connection

class ConfigModel():
    
    @classmethod
    def get_configuraciones(self):

        try:
            conection = get_connection()
            configuraciones = {}

            with conection.cursor() as cursor:
                    cursor.execute("SELECT * from configuracion LIMIT 1")
                    resultset = cursor.fetchall()

                    for row in resultset:
                        config = Configuracion(id = row[0],ciclo= row[1],porc1= row[2],porc2= row[3],porc3 = row[4],horario_inicio=row[5],horario_fin=row[6],cuota1= row[7],cuota2= row[8],cuota3= row[9],cuota4= row[10],cuota5= row[11])
                        configuraciones = config.to_JSON()
                
            conection.close()
            return configuraciones 

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_configuracion(self,id: str):
         
         try:
            
            conection = get_connection()
            configuracion = None

            with conection.cursor() as cursor:
                    cursor.execute("SELECT * from configuracion WHERE id=%s",(id,))
                    row = cursor.fetchone()

                    if row is not None:
                        config = Configuracion(id = row[0],ciclo= row[1],porc1= row[2],porc2= row[3],porc3 = row[4],horario_inicio=row[5],horario_fin=row[6],cuota1= row[7],cuota2= row[8],cuota3= row[9],cuota4= row[10],cuota5= row[11])
                        configuracion = config
                
            conection.close()
            return configuracion

         except  Exception as ex:
            raise Exception(ex)
         
    @classmethod
    def add_configuracion(self,config):
         
        try:
             
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO configuracion(ciclo,porc1,porc2,porc3,horario_inicio,horario_fin,cuota1,cuota2,cuota3,cuota4,cuota5)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(config.ciclo,config.porc1,config.porc2,config.porc3,config.horario_inicio,config.horario_fin,config.cuota1,config.cuota2,config.cuota3,config.cuota4,config.cuota5))
                affected_rows = cursor.rowcount
                conection.commit()
              
            conection.close()
            return affected_rows
        

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_configuracion(self,config):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE configuracion SET ciclo = %s,porc1 = %s,porc2= %s,porc3 =%s,horario_inicio = %s,horario_fin = %s,cuota1 = %s,cuota2 = %s,cuota3 = %s, cuota4 =%s,cuota5 =%s WHERE id = %s",(config.ciclo,config.porc1,config.porc2,config.porc3,config.horario_inicio,config.horario_fin,config.cuota1,config.cuota2,config.cuota3,config.cuota4,config.cuota5,config.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
            
    
        except  Exception as ex:
            raise Exception(ex)