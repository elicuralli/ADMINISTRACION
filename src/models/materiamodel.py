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
                cursor.execute(
                    "SELECT * from materias INNER JOIN carreras ON materias.id_carrera = carreras.id")
                result = cursor.fetchall()

                for row in result:
                    materias = Materias(id=row[0], nombre=row[1], prelacion=row[2], unidad_credito=row[3], hp=row[4], ht=row[5],
                                        semestre=row[6], id_carrera=row[7], id_docente=row[8], dia=row[9], hora_inicio=row[10], hora_fin=row[11])
                    join["materias"].append(materias.to_JSON())
                    carrera = Carrera(id=row[12], nombre=row[13])
                    join["carreras"].append(carrera.to_JSON())

            conection.close()
            return join

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_materia(self, id: str):

        try:

            conection = get_connection()
            join = {"materias": [], "carreras": []}

            with conection.cursor() as cursor:
                cursor.execute(
                    "SELECT * from materias INNER JOIN carreras ON materias.id_carrera = carreras.id WHERE materias.id =%s", (id,))
                row = cursor.fetchone()

                if row is not None:
                    materias = Materias(id=row[0], nombre=row[1], prelacion=row[2], unidad_credito=row[3], hp=row[4], ht=row[5],
                                        semestre=row[6], id_carrera=row[7], id_docente=row[8], dia=row[9], hora_inicio=row[10], hora_fin=row[11])
                    carrera = Carrera(id=row[12], nombre=row[13])
                    join = {"carreras": carrera.to_JSON(
                    ), "materias": materias.to_JSON()}

                else:
                    return 'no existe'

            conection.close()
            return join

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_materia(self, materia):

        try:

            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute(
                    "SELECT *from materias WHERE id=%s", (materia.id,))
                result = cursor.fetchone()
                if result is not None:
                    return 'materia ya existe'
                cursor.execute("INSERT INTO materias(id,nombre,prelacion,unidad_credito,hp,ht,semestre,id_carrera,id_docente,dia,hora_inicio,hora_fin)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (materia.id,
                               materia.nombre, materia.prelacion, materia.unidad_credito, materia.hp, materia.ht, materia.semestre, materia.id_carrera, materia.id_docente, materia.dia, materia.hora_inicio, materia.hora_fin))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_materia(self, materia):

        try:

            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE materias SET nombre= %s,prelacion= %s,unidad_credito= %s,hp= %s,ht= %s,semestre= %s,id_carrera=%s, id_docente=%s, dia = %s,hora_inicio=%s, hora_fin= %s WHERE id=%s ", (
                    materia.nombre, materia.prelacion, materia.unidad_credito, materia.hp, materia.ht, materia.semestre, materia.id_carrera, materia.id, materia.id_docente, materia.dia, materia.hora_inicio, materia.hora_fin))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_materia(self, materia):

        try:

            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute(
                    "DELETE from materias WHERE id=%s", (materia.id,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_materias_validas(self, cedula_estudiante: str):
        try:
            conection = get_connection()
            materias_validas = []

            with conection.cursor() as cursor:
                # Obtenemos el estado y el semestre del estudiante
                cursor.execute("SELECT estado, semestre, carrera FROM estudiantes WHERE cedula = %s", (cedula_estudiante,))
                student = cursor.fetchone()
                if student is None:
                    raise Exception("Estudiante no encontrado")

                estado, semestre, carrera = student
                
                if estado == "nuevo ingreso" or semestre == 1:
                    cursor.execute("SELECT * FROM materias WHERE semestre = '1' AND id_carrera = %s", (carrera,))
                    materias = cursor.fetchall()
                    materias_obj = [Materias(*materia) for materia in materias]
                    return materias_obj
                
                else:
                # Obtenemos todas las materias
                    cursor.execute("SELECT * FROM materias WHERE id_carrera = %s", (carrera,))
                    materias = cursor.fetchall()

                    # Para cada materia, verificamos si el estudiante ha aprobado las materias pre-requisito
                    for materia in materias:
                        cursor.execute("""
                            SELECT m.prelacion
                            FROM materias m
                            WHERE m.id = %s
                            AND m.id_carrera = %s
                            AND NOT EXISTS (
                                SELECT 1
                                FROM materias_estudiantes me
                                WHERE me.cod_materia = m.prelacion
                                AND me.cedula_estudiante = %s
                                AND me.promedio < 50
                            )
                        """, (materia[0], carrera, cedula_estudiante))
                        result = cursor.fetchone()

                        # Si la consulta devuelve un resultado, significa que el estudiante ha aprobado todas las materias pre-requisito
                        if result is not None:
                            # Creamos un nuevo objeto de la clase Materias y lo agregamos a la lista
                            materia_obj = Materias(*materia)
                            materias_validas.append(materia_obj)

            conection.close()

            return materias_validas
        except Exception as ex:
            raise Exception(ex)
