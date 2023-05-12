from models.entities.materias import Materias
from database.db import get_connection 
from models.entities.carreras import Carrera

class MateriaModel():
   
    @classmethod
    def get_materias(self):

        try: 

            conection = get_connection()
            join = {"materias": [], "carreras": []}

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from materias INNER JOIN carreras ON materias.id_carrera = carreras.id")
                result = cursor.fetchall()
                print(result)

                for row in result:
                    materias = Materias(id = row[0], nombre = row[1],prelacion= row[2], unidad_credito=row[3],hp=row[4],ht=row[5],semestre=row[6],id_carrera=row[7])
                    join["materias"].append(materias.to_JSON())
                    carrera = Carrera(id=row[8],nombre=row[9])
                    join["carreras"].append(carrera.to_JSON())
            
            conection.close()
            return join 
            
        except  Exception as ex:
                raise Exception(ex)
    
    @classmethod
    def get_materia(self, id: str): 
         
        try: 
                conection = get_connection()
                
                with conection.cursor() as cursor:
                        cursor.execute("SELECT * from materias INNER JOIN carreras ON materias.id_carrera = carreras.id WHERE materias.id =%s",(id,))
                        row = cursor.fetchone()
                        
                        if row is not None:
                            materias = Materias(id = row[0], nombre = row[1],prelacion= row[2], unidad_credito=row[3],hp=row[4],ht=row[5],semestre=row[6],id_carrera=row[7])
                            carrera = Carrera(id=row[8],nombre=row[9])
                            join = {"carreras": carrera.to_JSON()," materias": materias.to_JSON()}
                        else: 
                             return 'no existe'
                    
                conection.close()
                return join
        
        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_materia(self,materia):
         
        try:

            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT *from materias WHERE id=%s", (materia.id,))
                result = cursor.fetchone()
                if result is not None:
                    return 'materia ya existe'
                cursor.execute("INSERT INTO materias(id,nombre,prelacion,unidad_credito,hp,ht,semestre,id_carrera)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(materia.id,materia.nombre,materia.prelacion,materia.unidad_credito,materia.hp,materia.ht,materia.semestre,materia.id_carrera))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows


        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_materia(self,materia):
         
        try: 
             
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE materias SET nombre= %s,prelacion= %s,unidad_credito= %s,hp= %s,ht= %s,semestre= %s,id_carrera=%s WHERE id=%s ",(materia.nombre,materia.prelacion,materia.unidad_credito,materia.hp,materia.ht,materia.semestre,materia.id_carrera,materia.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def delete_materia(self,materia):

        try:    
         
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("DELETE from materias WHERE id=%s", (materia.id,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)



         