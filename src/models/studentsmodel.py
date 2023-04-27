from database.db import get_connection 
from models.entities.students import Student


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
                    student = Student(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    students.append(student.to_JSON())
            
            conection.close()
            return students

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_student(cedula: str):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from estudiantes WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                student = None
                if row != None:
                    student = Student(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    student = student.to_JSON()

                
            conection.close()
            return student

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_student(self,student):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
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
            
            


