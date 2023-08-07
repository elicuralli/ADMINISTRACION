from database.db import get_connection 
from models.entities.students import Student
from models.entities.administracion import Administracion
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
                    student = Student(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[4],semestre=row[5],password=None,estado=row[6], carrera= row[7],edad = row[8],sexo = row[9],promedio = row[10],direccion=row[11],fecha_nac=row[12])
                    students.append(student.to_JSON())
            
            conection.close()
            return students

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_student(self, cedula: str):
        try:
            conection = get_connection()
            join = {}
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from estudiantes INNER JOIN pagos ON pagos.cedula_estudiante = estudiantes.cedula INNER JOIN monto ON pagos.id = monto.id_pago INNER JOIN metodo_pago ON metodo_pago.id_pago = pagos.id WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                if row != None:
                    join["estudiante"] = Student(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[4],semestre=row[5],password=None,estado=row[6],carrera= row[7],edad = row[9],sexo = row[8],promedio = row[10],direccion=row[11],fecha_nac=row[12]).to_JSON()
                    join["pago"] = Administracion(row[13], row[0], row[14], row[15], row[16], row[17], row[18], row[19], row[20]).to_JSON()
                    join["monto"] = Monto(row[21], row[13], row[22], row[23], row[24], row[25], row[26], row[27]).to_JSON()
                    join["metodo"] = Metodo(row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[13]).to_JSON()
                
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_student(self,student):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
               
                cursor.execute("SELECT * from estudiantes WHERE cedula =%s",(student.cedula,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'estudiante ya existe'
                cursor.execute("""INSERT INTO estudiantes (cedula,fullname,correo,telefono,semestre,password,estado, carrera,edad,sexo,promedio,direccion,fecha_nac)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,%s)""",(student.cedula,student.fullname,student.correo,student.telefono,student.semestre,student.password,student.estado,student.carrera,student.edad,student.sexo,student.direccion,student.fecha_nac))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_student(self,student):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE estudiantes SET fullname = %s,correo = %s,telefono = %s,semestre = %s, estado = %s, carrera = %s, edad = %s,sexo = %s,promedio = %s, direccion = %s, fecha_nac =%s WHERE cedula = %s""", (student.fullname,student.correo,student.telefono,student.semestre,student.estado,student.carrera,student.edad,student.sexo,student.promedio,student.direccion,student.fecha_nac,student.cedula))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_student(self,student):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM estudiantes WHERE cedula = %s", (student.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def login(self,estudiante: Student):
        try:

            conection = get_connection()
            student: Student
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM estudiantes WHERE correo=%s",(estudiante.correo,)) 
                row = cursor.fetchone()
                conection.commit()
                if row is not None:
                    student = Student(row[0], row[1], row[2], row[4], row[5], row[3], row[6], row[7],row[8],row[9],row[10],row[11],row[12])
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
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO materias_estudiantes (cod_materia, cedula_estudiante,nota1,nota2,nota3, promedio, uc) VALUES (%s, %s,0,0,0,0,0)", (materia, estudiante.cedula))
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
                """, (cedula_estudiante,config.ciclo))
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
            join = {"ciclo": "", "contenido":[]}
            with connection.cursor() as cursor:
                cursor.execute("""SELECT m.modalidad, CONCAT(m.id, ' ', m.nombre), m.ciclo FROM materias_estudiantes me INNER JOIN estudiantes e ON e.cedula = me.cedula_estudiante INNER JOIN materias m ON m.id = me.cod_materia""")

                consulta = cursor.fetchall()

                for row in consulta:
                    join["ciclo"] = row[2]
                    join["contenido"].append({"modalidad": row[0], "asignatura": row[1] })

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
                cursor.execute("""SELECT m.id, m.nombre, m.hp, m.ht, m.dia, m.hora_inicio, m.hora_fin, m.unidad_credito, d.fullname FROM materias_estudiantes me INNER JOIN estudiantes e ON e.cedula = me.cedula_estudiante INNER JOIN materias m ON m.id = me.cod_materia INNER JOIN docentes d on d.cedula = m.id_docente WHERE m.ciclo = %s""",(ciclo,))

                consulta = cursor.fetchall()

                for row in consulta:
                    join.append({"id": row[0], "nombre": row[1], "hp": row[2], "ht": row[3], "dia": row[4], "hora_inicio": row[5], "hora_fin": row[6], "unidad_credito": row[7], "id_docente": row[8]})

            return join
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_pago_by_student(self, cedula: str):
        try:
            conection = get_connection()
            
            pagos = {}
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from pagos WHERE cedula_estudiante = %s",(cedula,))
                row = cursor.fetchone()

                if row != None:
                    pagos = Administracion(id=row[0],pre_inscripcion=row[1],inscripcion=row[2],cuota1=row[3],cuota2=row[4],cuota3=row[5],cuota4=row[6],cuota5=row[7],cedula_estudiante=row[8])

                
            conection.close()
            return pagos

        except  Exception as ex:
            raise Exception(ex)