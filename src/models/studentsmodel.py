from database.db import get_connection 
from models.entities.students import Student
from models.entities.administracion import Administracion
from models.entities.monto import Monto

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
                    student = Student(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[4],semestre=row[5],password=None,estado=row[6])
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
                cursor.execute("SELECT * from estudiantes INNER JOIN pagos ON pagos.cedula_estudiante = estudiantes.cedula INNER JOIN monto ON pagos.id = monto.id_pago WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                if row != None:
                    join["estudiante"] = Student(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[4],semestre=row[5],password=None,estado=row[6]).to_JSON()
                    join["pago"] = Administracion(row[7], row[0], row[8], row[9], row[10], row[11], row[12], row[13], row[14]).to_JSON()
                    join["monto"] = Monto(row[16], row[7], row[17], row[18], row[19], row[20], row[21], row[22]).to_JSON()
                
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
                cursor.execute("""INSERT INTO estudiantes (cedula,fullname,correo,telefono,semestre,password,estado)VALUES (%s,%s,%s,%s,%s,%s,%s)""",(student.cedula,student.fullname,student.correo,student.telefono,student.semestre,student.password,student.estado))
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
                cursor.execute("""UPDATE estudiantes SET fullname =%s,correo =%s,telefono=%s,semestre =%s,password=%s,estado=%s WHERE cedula =%s""", (student.fullname,student.correo,student.telefono,student.semestre,student.password,student.estado,student.cedula))
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
    def count_students(self):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM estudiantes")
                row = cursor.fetchone()
                if row != None:
                    return row[0]
        except Exception as ex:
            raise Exception(ex)
            
            


