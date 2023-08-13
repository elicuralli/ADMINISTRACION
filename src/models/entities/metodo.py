class Metodo():

    def __init__(self, id= None, nombre = None,descripcion = None ):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

       
    def to_JSON(self):
        return {

            "id": self.id,
           "nombre": self.nombre,
           "descripcion": self.descripcion
        }
        
