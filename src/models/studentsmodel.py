from database.db import get_connection
from models.entities.students import Student
from models.entities.pagos import Pago
from models.entities.monto import Monto
from models.entities.metodo import Metodo
from models.configmodel import ConfigModel


class StudentModel():

    @classmethod
    def get_students(self):
        try:
            conection = get_connection()
            students = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from estudiantes ORDER BY cedula")
                resultset = cursor.fetchall()

                for row in resultset:
                    student = Student(cedula=row[0], fullname=row[1], correo=row[2], telefono=row[4], semestre=row[5], password=None,
                                      estado=row[6], carrera=row[7], edad=row[8], sexo=row[9], promedio=row[10], direccion=row[11], fecha_nac=row[12])
                    students.append(student.to_JSON())

            conection.close()
            return students

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_student(self, cedula: str):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.cedula, e.fullname, e.correo, e.telefono, e.semestre, e.estado, e.carrera, e.edad, e.sexo, e.promedio, e.direccion, e.fecha_nac FROM estudiantes e
                    WHERE e.cedula = %s
                """, (cedula,))
                row = cursor.fetchone()

                if row is not None:
                    student = Student(
                        cedula=row[0], fullname=row[1], correo=row[2], telefono=row[3], semestre=row[4],
                        estado=row[5], carrera=row[6], edad=row[7], sexo=row[8], promedio=row[9],
                        direccion=row[10], fecha_nac=row[11]
                    ).to_JSON()

            connection.close()
            return student

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_student(self, student):
        try:
            conection = get_connection()

            with conection.cursor() as cursor:

                cursor.execute(
                    "SELECT * from estudiantes WHERE cedula =%s", (student.cedula,))
                result = cursor.fetchone()
                if result is not None:
                    return 'estudiante ya existe'
                cursor.execute("""INSERT INTO estudiantes (cedula,fullname,correo,telefono,semestre,password,estado, carrera,edad,sexo,promedio,direccion,fecha_nac)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,%s)""", (
                    student.cedula, student.fullname, student.correo, student.telefono, student.semestre, student.password, student.estado, student.carrera, student.edad, student.sexo, student.direccion, student.fecha_nac))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_student(self, student):
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("""UPDATE estudiantes SET fullname = %s,correo = %s,telefono = %s,semestre = %s, estado = %s, carrera = %s, edad = %s,sexo = %s,promedio = %s, direccion = %s, fecha_nac =%s WHERE cedula = %s""", (
                    student.fullname, student.correo, student.telefono, student.semestre, student.estado, student.carrera, student.edad, student.sexo, student.promedio, student.direccion, student.fecha_nac, student.cedula))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_student(self, student):
        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM estudiantes WHERE cedula = %s", (student.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self, estudiante: Student):
        try:

            conection = get_connection()
            student: Student
            with conection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM estudiantes WHERE correo=%s", (estudiante.correo,))
                row = cursor.fetchone()
                conection.commit()
                if row is not None:
                    student = Student(row[0], row[1], row[2], row[4], row[5], row[3],
                                      row[6], row[7], row[8], row[9], row[10], row[11], row[12])
                else:
                    return None

            conection.close()
            return student

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_materia(self, estudiante: Student, materia: str):
        try:
            connection = get_connection()
            affected_rows: int = 0
            ciclo = ConfigModel.get_configuracion("1").ciclo
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO materias_estudiantes (cod_materia, cedula_estudiante,nota1,nota2,nota3, promedio, uc, ciclo) VALUES (%s, %s,0,0,0,0,0, %s)", (materia, estudiante.cedula, ciclo))
                connection.commit()
                affected_rows = cursor.rowcount

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_notas_estudiante(cls, cedula_estudiante: str):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                config = ConfigModel.get_configuracion("1")

                cursor.execute("""
                    SELECT m.nombre, m.id, me.nota1, me.nota2, me.nota3, me.promedio
                    FROM materias_estudiantes me
                    JOIN materias m ON me.cod_materia = m.id
                    WHERE me.cedula_estudiante = %s AND m.ciclo = %s
                """, (cedula_estudiante, config.ciclo))
                notas = cursor.fetchall()

                notas_obj = [{
                    "materia": nota[0],
                    "id": nota[1],
                    "nota1": nota[2],
                    "nota2": nota[3],
                    "nota3": nota[4],
                    "promedio": nota[5]
                } for nota in notas]
                connection.close()
                return {"notas": notas_obj, "ciclo": config.ciclo}

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_historico(cls, cedula_estudiante: str):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT m.nombre, m.id, m.ciclo, m.semestre, me.nota1, me.nota2, me.nota3, me.promedio
                    FROM materias_estudiantes me
                    JOIN materias m ON me.cod_materia = m.id
                    WHERE me.cedula_estudiante = %s
                """, (cedula_estudiante,))
                notas = cursor.fetchall()

                notas_obj = [{
                    "materia": nota[0],
                    "id": nota[1],
                    "ciclo": nota[2],
                    "semestre": nota[3],
                    "nota1": nota[4],
                    "nota2": nota[5],
                    "nota3": nota[6],
                    "promedio": nota[7]
                } for nota in notas]
                connection.close()
                return {"notas": notas_obj}

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_materias_inscritas(self, cedula: str):
        try:
            connection = get_connection()
            join = {"ciclo": "", "contenido": []}
            with connection.cursor() as cursor:
                cursor.execute("""SELECT m.modalidad, CONCAT(m.id, ' ', m.nombre), m.ciclo FROM materias_estudiantes me INNER JOIN estudiantes e ON e.cedula = me.cedula_estudiante INNER JOIN materias m ON m.id = me.cod_materia WHERE me.cedula_estudiante = %s""", (cedula,))

                consulta = cursor.fetchall()

                for row in consulta:
                    join["ciclo"] = row[2]
                    join["contenido"].append(
                        {"modalidad": row[0], "asignatura": row[1]})

            return join
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_inscritas(self, cedula: str):
        try:
            connection = get_connection()
            join = []
            with connection.cursor() as cursor:
                ciclo = ConfigModel.get_configuracion("1").ciclo
                cursor.execute("""SELECT m.id, m.nombre, m.hp, m.ht, CONCAT(m.dia, ', ', m.dia2), CONCAT(m.hora_inicio, ', ', m.hora_inicio2), CONCAT(m.hora_fin, ', ', m.hora_fin2), m.unidad_credito, d.fullname FROM materias_estudiantes me INNER JOIN estudiantes e ON e.cedula = me.cedula_estudiante INNER JOIN materias m ON m.id = me.cod_materia INNER JOIN docentes d on d.cedula = m.id_docente WHERE m.ciclo = %s AND me.cedula_estudiante = %s""", (ciclo,cedula))

                consulta = cursor.fetchall()

                for row in consulta:
                    join.append({"id": row[0], "nombre": row[1], "hp": row[2], "ht": row[3], "dia": row[4],
                                "hora_inicio": row[5], "hora_fin": row[6], "unidad_credito": row[7], "id_docente": row[8]})

            return join
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_pago_by_student(self, cedula: str):
        try:
            conection = get_connection()

            pagos = []

            with conection.cursor() as cursor:
                query = """
            SELECT p.*, m.concepto, m.monto, mp.nombre, mp.descripcion
            FROM pagos p
            JOIN montos m ON p.monto_id = m.id
            JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
            WHERE p.cedula_estudiante = %s
            """

                cursor.execute(query, (cedula,))
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        pago = Pago(
                            id=row[0],
                            cedula_estudiante=row[1],
                            metodo_pago_id=Metodo(
                                id=row[2], nombre=row[8], descripcion=row[9]),
                            monto_id=Monto(
                                id=row[3], concepto=row[7], monto=row[10]),
                            fecha_pago=row[4],
                            referencia_transferencia=row[5],
                            ciclo=row[6]
                        )
                        pagos.append(pago)

            conection.close()
            return pagos

        except Exception as ex:
            raise Exception(ex)
