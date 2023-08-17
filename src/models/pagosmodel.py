from models.entities.metodo import Metodo
from models.entities.monto import Monto
from models.entities.pagos import Pago
from database.db import get_connection 


class PagoModel():
    @classmethod
    def get_pagos(cls):
        try:
            connection = get_connection()
            pagos = []

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.cedula_estudiante, p.fecha_pago,
                           m.id AS metodo_id, m.nombre AS metodo_nombre,
                           mo.id AS monto_id, mo.concepto AS monto_concepto, mo.monto AS monto_monto
                    FROM pagos p
                    INNER JOIN metodo_pago m ON p.metodo_pago_id = m.id
                    LEFT JOIN transferencias t ON m.id = t.metodo_pago_id
                    LEFT JOIN billetes b ON b.metodo_pago_id = m.id
                    INNER JOIN montos mo ON p.monto_id = mo.id
                    ORDER BY p.id ASC
                """)
                resultset = cursor.fetchall()

                for row in resultset:
                    metodo = Metodo(row['metodo_id'], row['metodo_nombre'])
                    monto = Monto(row['monto_id'], row['monto_concepto'], row['monto_monto'])
                    pago = Pago(
                        id=row['id'],
                        cedula_estudiante=row['cedula_estudiante'],
                        metodo_pago=metodo,
                        monto=monto,
                        fecha_pago=row['fecha_pago']
                    )
                    pagos.append(pago.to_JSON())
            
            connection.close()
            return pagos

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_pago(cls, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.cedula_estudiante, p.fecha_pago,
                           m.id AS metodo_id, m.nombre AS metodo_nombre,
                           mo.id AS monto_id, mo.concepto AS monto_concepto, mo.monto AS monto_monto
                    FROM pagos p
                    INNER JOIN metodo_pago m ON p.metodo_pago_id = m.id
                    INNER JOIN montos mo ON p.monto_id = mo.id
                    WHERE p.id = %s
                """, (id,))
                row = cursor.fetchone()

                if row is not None:
                    metodo = Metodo(row['metodo_id'], row['metodo_nombre'])
                    monto = Monto(row['monto_id'], row['monto_concepto'], row['monto_monto'])
                    pago = Pago(
                        id=row['id'],
                        cedula_estudiante=row['cedula_estudiante'],
                        metodo_pago=metodo,
                        monto=monto,
                        fecha_pago=row['fecha_pago']
                    )
                else:
                    pago = None
                
            connection.close()
            return pago

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_pago(cls,pago):

        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("INSERT INTO pagos(id,cedula_estudiante,metodo_pago_id,monto_id,fecha_pago,referencia_transferencia)VALUES(%s,%s,%s,%s,%s,%s)"(pago.id,pago.cedula_estudiante,pago.metodo_pago_id,pago.monto_id,pago.fecha_pago,pago.referencia_transferencia))
                affected_rows = cursor.rowcount
                conection.commit()


            conection.close()
            return affected_rows
        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_pago(cls,pago):
        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
                cursor.execute("UPDATE pagos SET cedula_estudiante=%s,metodo_pago_id=%s,monto_id=%s,fecha_pago=%s,referencia_transferencia=%s WHERE id = %s",(pago.cedula_estudiante,pago.metodo_pago_id,pago.monto_id,pago.fecha_pago,pago.referencia_transferencia,pago.id) )
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)
        