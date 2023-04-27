class User:
    def __init__(self,usuario,clave,id = None,) -> None:
        self.id = id
        self.usuario = usuario
        self.clave = clave
    
    def to_JSON(self):
        return{
            "id":self.id,
            "usuario": self.usuario,
            "clave":self.clave
        }