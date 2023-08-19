from database.db import get_connection 


class FacturaModel:

    @classmethod
    def get_current_number(cls):

        connection = get_connection()

        with connection.cursor() as cursor: 
            cursor.execute("SELECT id FROM factura;")
            current_number = cursor.fetchone()[0]
        connection.close()
        return current_number

    @classmethod
    def increment_number(cls):

        connection = get_connection()
        
        with connection.cursor() as cursor: 
            cursor.execute("UPDATE factura SET id = id + 1;")
            connection.commit()
        connection.close()

    @classmethod
    def get_incremented_number(cls):
        cls.increment_number()
        return cls.get_current_number()
