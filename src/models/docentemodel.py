from database.db import get_connection 
from models.entities.docente import Docente
from models.entities.materias import Materias
from models.entities.peticiones import Peticiones


class DocenteModel():

    @classmethod
    def get_docentes(self):
        try:
            conection = get_connection()
            join = {"docente": [], "materias": []}

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from docentes LEFT JOIN materias ON docentes.cedula = materias.id_docente")
                result = cursor.fetchall()

                if result is not None:
                    for row in result:

                        docente = Docente(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                        materias = Materias(id = row[5], nombre = row[6],prelacion= row[7], unidad_credito=row[8],hp=row[9],ht=row[10],semestre=row[11],id_carrera=row[12],id_docente=row[13],dia = row[14], hora_inicio=row[15],hora_fin=row[16])
                        join["docente"].append(docente.to_JSON())
                        join["materias"].append(materias.to_JSON())
                
                else: 
                    return 'no existe'

            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_docente(self,cedula :str):
        
        try:
            conection = get_connection()
            join = {"docente": {}, "materias": []}

            with conection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT d.cedula, d.fullname, d.correo, d.telefono, d.password, m.id, m.nombre, m.prelacion, m.unidad_credito, m.hp, m.ht, m.semestre, m.id_carrera, m.id_docente, m.dia, m.hora_inicio, m.hora_fin, COUNT(me.cedula_estudiante) AS cantidad_estudiantes
                    FROM docentes d
                    INNER JOIN materias m ON d.cedula = m.id_docente
                    LEFT JOIN materias_estudiantes me ON m.id = me.cod_materia
                    WHERE d.cedula = %s
                    GROUP BY d.cedula, d.fullname, d.correo, d.telefono, d.password, m.id, m.nombre, m.prelacion, m.unidad_credito, m.hp, m.ht, m.semestre, m.id_carrera, m.id_docente, m.dia, m.hora_inicio, m.hora_fin
                    """,
                    (cedula,)
                )
                result = cursor.fetchall()

                for row in result:
                    if row is not None:
                        docente = Docente(cedula=row[0], fullname=row[1], correo=row[2], telefono=row[3], password=row[4])
                        materias = Materias(id=row[5], nombre=row[6], prelacion=row[7], unidad_credito=row[8], hp=row[9], ht=row[10], semestre=row[11], id_carrera=row[12], id_docente=row[13], dia=row[14], hora_inicio=row[15], hora_fin=row[16], cantidad_estudiantes=row[17])
                        join["docente"] = docente.to_JSON()
                        join["materias"].append(materias.to_JSON_with_quantity())

                    else:
                        return 'no existe'
                    
            
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_peticiones_por_docente(cls, cedula_docente):
        try:
            conection = get_connection()
            peticiones = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM peticiones WHERE id_docente = %s", (cedula_docente,))
                result = cursor.fetchall()

                if result is not None:
                    for row in result:
                        peticion = Peticiones(id=row[0], fecha=row[1], descripcion=row[2], id_docente=row[3])
                        peticiones.append(peticion.to_JSON())
                else:
                    return 'no existen peticiones para el docente'

            conection.close()
            return peticiones

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_docente(self,docente):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
               
                cursor.execute("SELECT * from docentes WHERE cedula =%s",(docente.cedula,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'docente ya existe'
                cursor.execute("""INSERT INTO docentes(cedula,fullname,correo,telefono,password)VALUES (%s,%s,%s,%s,%s)""",(docente.cedula,docente.fullname,docente.correo,docente.telefono,docente.password))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_docente(self,docente):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE docentes SET fullname =%s,correo =%s,telefono=%s,password=%s WHERE cedula =%s""", (docente.fullname,docente.correo,docente.telefono,docente.password,docente.cedula))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_docente(self,docente):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM docentes WHERE cedula = %s", (docente.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def login(self,docente: Docente):
        try:

            conection = get_connection()
            doc: Docente
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from docentes WHERE docentes.correo =%s",(docente.correo,))
                row = cursor.fetchone()

                if row is not None:
                    doc = Docente(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                else:
                    return None

            conection.close()
            return doc
        
        except Exception as ex:
            raise Exception(ex)