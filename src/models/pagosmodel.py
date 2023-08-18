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
                    SELECT p.id, p.cedula_estudiante, p.fecha_pago, m.descripcion,
                           m.id, m.nombre, mo.id, mo.concepto, mo.monto, t.codigo_referencia
                    FROM pagos p
                    INNER JOIN metodo_pago m ON p.metodo_pago_id = m.id
                    LEFT JOIN transferencias t ON p.referencia_transferencias = t.id
                    LEFT JOIN billetes b ON b.pago_id = p.id
                    INNER JOIN montos mo ON p.monto_id = mo.id
                    ORDER BY p.id ASC
                """)
                resultset = cursor.fetchall()

                for row in resultset:
                    print(row)
                    metodo = Metodo(row[4], row[5], row[3])
                    monto = Monto(row[6], row[7], row[8])
                    pago = Pago(
                        id=row[0],
                        cedula_estudiante=row[1],
                        metodo_pago_id=metodo,
                        monto_id=monto,
                        fecha_pago=row[2],
                        referencia_transferencia=row[9]
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
                    SELECT p.id, p.cedula_estudiante, p.fecha_pago, m.descripcion,
                           m.id, m.nombre, mo.id, mo.concepto, mo.monto,
                           t.codigo_referencia
                    FROM pagos p
                    INNER JOIN metodo_pago m ON p.metodo_pago_id = m.id
                    LEFT JOIN transferencias t ON p.referencia_transferencias = t.id
                    LEFT JOIN billetes b ON b.pago_id = p.id
                    INNER JOIN montos mo ON p.monto_id = mo.id
                    WHERE p.id = %s
                """, (id,))
                row = cursor.fetchone()

                if row is not None:
                    metodo = Metodo(row[4], row[5], row[3])
                    monto = Monto(row[6], row[7], row[8])
                    pago = Pago(
                        id=row[0],
                        cedula_estudiante=row[1],
                        metodo_pago_id=metodo,
                        monto_id=monto,
                        fecha_pago=row[2],
                        referencia_transferencia=row[9]
                    ).to_JSON()
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
                cursor.execute("INSERT INTO pagos(cedula_estudiante,metodo_pago_id,monto_id,fecha_pago,referencia_transferencias)VALUES(%s,%s,%s,%s,%s) RETURNING id", (pago.cedula_estudiante,pago.metodo_pago_id,pago.monto_id,pago.fecha_pago,pago.referencia_transferencia))
                id_inserted = cursor.fetchone()[0]
                affected_rows = cursor.rowcount
                
                conection.commit()


            conection.close()
            return affected_rows, id_inserted
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
        