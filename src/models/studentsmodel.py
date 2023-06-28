from database.db import get_connection 
from models.entities.students import Student
from models.entities.administracion import Administracion
from models.entities.monto import Monto
from models.entities.metodo import Metodo

class StudentModel():

    @classmethod
    def get_students(self):
        try:
            conection = get_connection()
            students = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from estudiantes ORDER BY cedula ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    student = Student(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[4],semestre=row[5],password=None,estado=row[6], carrera= row[7])
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
                    join["estudiante"] = Student(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[4],semestre=row[5],password=None,estado=row[6],carrera= row[7]).to_JSON()
                    join["pago"] = Administracion(row[8], row[0], row[9], row[10], row[11], row[12], row[13], row[14], row[15]).to_JSON()
                    join["monto"] = Monto(row[17], row[8], row[18], row[19], row[20], row[21], row[22], row[23]).to_JSON()
                    join["metodo"] = Metodo(row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[8]).to_JSON()
                
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
                cursor.execute("""INSERT INTO estudiantes (cedula,fullname,correo,telefono,semestre,password,estado, carrera)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(student.cedula,student.fullname,student.correo,student.telefono,student.semestre,student.password,student.estado,student.carrera))
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
                cursor.execute("""UPDATE estudiantes SET fullname =%s,correo =%s,telefono=%s,semestre =%s,password=%s,estado=%s, carrera = %s WHERE cedula =%s""", (student.fullname,student.correo,student.telefono,student.semestre,student.password,student.estado,student.carrera,student.cedula))
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
    def login(self,estudiante: Student) -> Student:
        try:

            conection = get_connection()
            student: Student
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM estudiantes WHERE correo=%s",(estudiante.correo,)) 
                row = cursor.fetchone()
                conection.commit()
                if row is not None:
                    print(row)
                    student = Student(row[0], row[1], row[2], row[4], row[5], row[3], row[6], row[7])
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
                cursor.execute("INSERT INTO materias_estudiantes (cod_materia, cedula_estudiante) VALUES (%s, %s)", (materia, estudiante.cedula))
                connection.commit()
                affected_rows = cursor.rowcount
            
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

