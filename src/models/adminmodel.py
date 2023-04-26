from database.db import get_connection 
from models.entities.administracion import Administracion
from models.entities.students import Student
class AdminModel():

    @classmethod
    def get_administracion(self):
        try:
            conection = get_connection()
            administracion = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT id,cedula_estudiante,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5 from pagos ORDER BY id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    admin = Administracion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    administracion.append(admin.to_JSON())
            
            conection.close()
            return administracion

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_administracion_id(self,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT admin.id, admin.cedula_estudiante, admin.pre_inscripcion, admin.inscripcion, admin.cuota1, admin.cuota2, admin.cuota3, admin.cuota4, admin.cuota5, est.cedula,est.fullname,est.correo,est.telefono,est.semestre,est.estado from pagos admin INNER JOIN estudiantes est ON est.cedula = admin.cedula_estudiante WHERE admin.id = %s",(id,))
                row = cursor.fetchone()

                join = None
                if row != None:
                    admin = Administracion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    student = Student(row[9], row[10], row[11], row[12], row[13], None, row[14])
                    join = {"pago": admin.to_JSON(), "estudiante": student.to_JSON()}

                
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_admin(self,administracion):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO pagos (id,cedula_estudiante,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(administracion.id,administracion.cedula_estudiante,administracion.pre_inscripcion,administracion.inscripcion,administracion.cuota1,administracion.cuota2,administracion.cuota3,administracion.cuota4,administracion.cuota5))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_admin(self,administracion):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""UPDATE pagos SET cedula_estudiante=%s,pre_inscripcion=%s,inscripcion=%s,cuota1=%s,cuota2=%s,cuota3=%s,cuota4=%s,cuota5=%s WHERE id=%s""", (administracion.cedula_estudiante,administracion.pre_inscripcion,administracion.inscripcion,administracion.cuota1,administracion.cuota2,administracion.cuota3,administracion.cuota4,administracion.cuota5,administracion.id))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_admin(self,admin):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM pagos WHERE id = %s", (admin.id,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def count_month(self, number):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pagos WHERE inscripcion LIKE %(date)s", {'date': "%-{}-%".format(number)})
                row = cursor.fetchone()
                if row != None:
                    return row[0]
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def count_day(self, number):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pagos WHERE inscripcion LIKE %(date)s", {'date': "%-{}%".format(number)})
                row = cursor.fetchone()
                if row != None:
                    return row[0]
        except Exception as ex:
            raise Exception(ex)