from database.db import get_connection
from models.configmodel import ConfigModel
from models.entities.carreras import Carrera
from models.entities.materias import Materias
from models.entities.docente import Docente


class MateriaModel():

    @classmethod
    def get_materias(self):

        try:

            conection = get_connection()
            join = {"materias": [], "carreras": []}

            with conection.cursor() as cursor:
                cursor.execute(
                    "SELECT * from materias RIGHT JOIN carreras ON materias.id_carrera = carreras.id")
                result = cursor.fetchall()

                for row in result:
                    materias = Materias(id=row[0], nombre=row[1], prelacion=row[2], unidad_credito=row[3], hp=row[4],
                                        ht=row[5],
                                        semestre=row[6], id_carrera=row[7], id_docente=row[8], dia=row[9],
                                        hora_inicio=row[10], hora_fin=row[11], dia2=row[14], hora_inicio2=row[15], hora_fin2=row[16], ciclo=row[12], modalidad=row[13], maximo=row[17])
                    join["materias"].append(materias.to_JSON())
                    carrera = Carrera(id=row[18], nombre=row[19])
                    join["carreras"].append(carrera.to_JSON())

            conection.close()
            return join

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_materia(self, id: str):
        try:
            conection = get_connection()
            join = {"ciclo": ConfigModel.get_configuracion("1").ciclo, "materia": {"id": "", "nombre": "",
                                                                                   "estudiantes": [], "carrera": ""}}
            with conection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.id, m.nombre, me.cedula_estudiante, es.fullname, me.nota1, me.nota2,  me.nota3, me.promedio, c.nombre
                    FROM materias m
                    LEFT JOIN carreras c ON m.id_carrera = c.id
                    LEFT JOIN materias_estudiantes me ON m.id = me.cod_materia
                    LEFT JOIN estudiantes es ON es.cedula = me.cedula_estudiante
                    WHERE m.id = %s
                    """,
                    (id,)
                )
                rows = cursor.fetchall()
                for row in rows:
                    estudiante = {
                        "cedula": row[2],
                        "nombre": row[3],
                        "nota1": row[4],
                        "nota2": row[5],
                        "nota3": row[6],
                        "promedio": row[7]
                    }
                    materia = {
                        "id": row[0],
                        "nombre": row[1],
                    }
                    carrera = row[8]

                    join["materia"]["id"] = materia["id"]
                    join["materia"]["nombre"] = materia["nombre"]
                    join["materia"]["estudiantes"].append(estudiante)
                    join["materia"]["carrera"] = carrera
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
                cursor.execute(
                    "INSERT INTO materias(id,nombre,prelacion,unidad_credito,hp,ht,semestre,id_carrera,id_docente,dia,hora_inicio,hora_fin,dia2,hora_inicio2,hora_fin2,ciclo,modalidad,maximo)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (materia.id,
                     materia.nombre, materia.prelacion, materia.unidad_credito, materia.hp, materia.ht,
                     materia.semestre, materia.id_carrera, materia.id_docente, materia.dia, materia.hora_inicio,
                     materia.hora_fin, materia.dia2, materia.hora_inicio2, materia.hora_fin2, materia.ciclo, materia.modalidad, materia.maximo))
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
                cursor.execute(
                    "UPDATE materias SET nombre= %s,prelacion= %s,unidad_credito= %s,hp= %s,ht= %s,semestre= %s,id_carrera=%s, id_docente=%s, dia = %s,hora_inicio=%s, hora_fin= %s,dia2 = %s,hora_inicio2=%s, hora_fin2= %s,ciclo = %s,modalidad =%s, maximo = %s WHERE id=%s ",
                    (
                        materia.nombre, materia.prelacion, materia.unidad_credito, materia.hp, materia.ht,
                        materia.semestre, materia.id_carrera, materia.id_docente, materia.dia,
                        materia.hora_inicio, materia.hora_fin, materia.dia2, materia.hora_inicio2, materia.hora_fin2, materia.ciclo, materia.modalidad, materia.maximo, materia.id))
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
            ciclo = ConfigModel.get_configuracion("1").ciclo

            with conection.cursor() as cursor:
                # Obtenemos el estado y el semestre del estudiante

                cursor.execute("SELECT COUNT(*) FROM materias_estudiantes WHERE cedula_estudiante = %s AND ciclo = %s",
                               (cedula_estudiante, ciclo))
                row = cursor.fetchone()
                if (row[0] > 0):
                    raise Exception(
                        "Usted ya tiene inscrito su horario, no puede inscribir más materias o modificarlo")

                cursor.execute(
                    "SELECT estado, semestre, carrera FROM estudiantes WHERE cedula = %s", (cedula_estudiante,))
                student = cursor.fetchone()
                if student is None:
                    raise Exception("Estudiante no encontrado")

                estado, semestre, carrera = student

                if estado == "nuevo ingreso" or semestre == 1:
                    cursor.execute(
                        "SELECT * FROM materias WHERE semestre = '1' AND id_carrera = %s", (carrera,))
                    materias = cursor.fetchall()
                    materias_obj = []
                    for materia in materias:
                        materias_obj.append(Materias(
                            id=materia[0], nombre=materia[1], prelacion=materia[2], unidad_credito=materia[3], hp=materia[4], ht=materia[5], semestre=materia[6], id_carrera=materia[7], id_docente=materia[8], dia=materia[9], hora_inicio=materia[10], hora_fin=materia[11], ciclo=materia[12], modalidad=materia[13], dia2=materia[14], hora_inicio2=materia[15], hora_fin2=materia[16], maximo=materia[17]))
                    return materias_obj

                else:
                    # Obtenemos todas las materias
                    cursor.execute(
                        "SELECT * FROM materias WHERE id_carrera = %s AND ciclo = %s", (carrera, ciclo))
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
                            materia_obj = Materias(
                                id=materia[0], nombre=materia[1], prelacion=materia[2], unidad_credito=materia[3], hp=materia[4], ht=materia[5], semestre=materia[6], id_carrera=materia[7], id_docente=materia[8], dia=materia[9], hora_inicio=materia[10], hora_fin=materia[11], ciclo=materia[12], modalidad=materia[13], dia2=materia[14], hora_inicio2=materia[15], hora_fin2=materia[16], maximo=materia[17])
                            cursor.execute("SELECT COUNT(*) FROM materias_estudiantes WHERE cod_materia = %s AND ciclo = %s",
                                           (materia_obj.id, ciclo))
                            row = cursor.fetchone()
                            # Creamos un nuevo objeto de la clase Materias y lo agregamos a la lista
                            if row:
                                materia_obj.cantidad_estudiantes = row[0]
                            materias_validas.append(materia_obj)

            conection.close()

            return materias_validas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def modificar_materia_estudiante(self, cod_materia, cedula_estudiante, nombre_campo, valor):
        global conection
        try:
            conection = get_connection()

            with conection.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE materias_estudiantes
                    SET {campo} = %s
                    WHERE cedula_estudiante = %s
                    """.format(campo=nombre_campo),
                    (valor, cedula_estudiante)
                )
                affected_rows = cursor.rowcount

                conection.commit()

                if affected_rows > 0:
                    cursor.execute(
                        """
                        SELECT nota1, nota2, nota3 FROM materias_estudiantes
                        WHERE cedula_estudiante = %s AND cod_materia = %s
                        """,
                        (cedula_estudiante, cod_materia)
                    )

                    res = cursor.fetchone()
                    config = ConfigModel.get_configuracion("1")

                    promedio = res[0] * (config.porc1 / 100) + res[1] * (config.porc2 / 100) + res[2] * (
                        config.porc3 / 100)

                    cursor.execute(
                        """
                        UPDATE materias_estudiantes
                        SET promedio = %s
                        WHERE cedula_estudiante = %s AND cod_materia = %s
                        """,
                        (promedio, cedula_estudiante, cod_materia)
                    )

                    conection.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conection.close()

    @classmethod
    def get_docenteria(self):
        try:
            conection = get_connection()
            join = {"contenido": {"materia": []}}
            ciclo = ConfigModel.get_configuracion("1").ciclo

            with conection.cursor() as cursor:
                cursor.execute("""
                SELECT m.*, c.*, d.*
                FROM materias m
                LEFT JOIN carreras c ON m.id_carrera = c.id
                LEFT JOIN docentes d ON m.id_docente = d.cedula WHERE ciclo = %s
                """,(ciclo,))
                result = cursor.fetchall()

                for row in result:
                    materia = Materias(id=row[0], nombre=row[1], prelacion=row[2], unidad_credito=row[3], hp=row[4], ht=row[5], semestre=row[6], id_carrera=row[7], id_docente=row[8],
                                       dia=row[9], hora_inicio=row[10], hora_fin=row[11], ciclo=row[12], modalidad=row[13], dia2=row[14], hora_inicio2=row[15], hora_fin2=row[16], maximo=row[17])
                    carrera = Carrera(nombre=row[19])
                    docente = Docente(cedula=row[20], fullname=row[21])

                    join["contenido"]["materia"].append({
                        "id": materia.id,
                        "nombre": materia.nombre,
                        "prelacion": materia.prelacion,
                        "unidad_credito": materia.unidad_credito,
                        "hp": materia.hp,
                        "ht": materia.ht,
                        "semestre": materia.semestre,
                        "id_carrera": materia.id_carrera,
                        "id_docente": materia.id_docente,
                        "dia": materia.dia,
                        "hora_inicio": materia.hora_inicio,
                        "hora_fin": materia.hora_fin,
                        "dia2": materia.dia2,
                        "hora_inicio2": materia.hora_inicio2,
                        "hora_fin2": materia.hora_fin2,
                        "maximo": materia.maximo,
                        "ciclo": materia.ciclo,
                        "modalidad": materia.modalidad,
                        "carrera": materia.id_carrera,
                        "nombre_docente": docente.fullname,
                    })

            conection.close()
            return join

        except Exception as ex:
            raise Exception(ex)
