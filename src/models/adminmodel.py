from database.db import get_connection 
from models.entities.administracion import Administracion
from models.entities.students import Student
from models.entities.monto import Monto
from models.entities.metodo import Metodo

class AdminModel():

    @classmethod
    def get_administracion(self):
        try:
            conection = get_connection()
            join = {"pagos": [], "montos": [], "metodos":[]}

            with conection.cursor() as cursor:
                cursor.execute("SELECT * from pagos INNER JOIN monto ON monto.id_pago = pagos.id INNER JOIN metodo_pago ON metodo_pago.id = pagos.id  ORDER BY pagos.id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    admin = Administracion(id=row[0],pre_inscripcion=row[1],inscripcion=row[2],cuota1=row[3],cuota2=row[4],cuota3=row[5],cuota4=row[6],cuota5=row[7],cedula_estudiante=row[8])
                    join["pagos"].append(admin.to_JSON())
                    monto = Monto(row[9], row[0], row[10], row[11], row[12], row[13], row[14], row[15], row[16])
                    join["montos"].append(monto.to_JSON())
                    metodo = Metodo(row[17],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[18])
                    join["metodos"].append(metodo.to_JSON())
            
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_administracion_id(self,id):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from pagos INNER JOIN estudiantes est ON est.cedula = pagos.cedula_estudiante INNER JOIN monto ON monto.id_pago = pagos.id WHERE pagos.id = %s",(id,))
                row = cursor.fetchone()

                join = None
                if row != None:
                    admin = Administracion(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    student = Student(row[9], row[10], row[11], row[12], row[13], None, row[15])
                    monto = Monto(row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24])
                    metodo = Metodo(row[24],row[26],row[27],row[28],row[29],row[30],row[21],row[32],row[33])
                    join = {"pago": admin.to_JSON(), "estudiante": student.to_JSON(), "monto": monto.to_JSON(),"metodo":metodo.to_JSON()}

                
            conection.close()
            return join

        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_admin(self,administracion):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("""INSERT INTO pagos (cedula_estudiante,pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",(administracion.cedula_estudiante,administracion.pre_inscripcion,administracion.inscripcion,administracion.cuota1,administracion.cuota2,administracion.cuota3,administracion.cuota4,administracion.cuota5))
                conection.commit()
                row = cursor.fetchone()
                id_pago = row[0]

            conection.close()
            return id_pago

        except  Exception as ex:
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