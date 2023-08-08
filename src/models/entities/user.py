class User:
    def __init__(self,usuario,clave=None,id = None,nombre=None) -> None:
        self.id = id
        self.usuario = usuario
        self.clave = clave
        self.nombre = nombre
    
    def to_JSON(self):
        return{
            "id":self.id,
            "usuario": self.usuario,
            "nombre": self.nombre
        }