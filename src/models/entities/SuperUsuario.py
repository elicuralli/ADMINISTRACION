class SuperUsuario:
    def __init__(self,cedula = None,nombre = None,correo = None,password = None) -> None:
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.password = password
    

    def to_JSON(self):
        return {
            
            "cedula": self.cedula,
            "nombre": self.nombre,
            "correo": self.correo,
            "password": self.password
        }