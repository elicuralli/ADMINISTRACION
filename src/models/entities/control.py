class Control():

    def __init__(self,cedula, fullname = None,correo= None,telefono= None,password= None,rol= None) -> None:

        self.cedula = cedula 
        self.fullname = fullname
        self.correo = correo
        self.telefono = telefono
        self.password = password
        self.rol = rol

    def to_JSON(self):
        return{
            
            "cedula": self.cedula,
            "fullname": self.fullname,
            "correo": self.correo, 
            "telefono": self.telefono,
            "password": self.password,
            "rol": self.rol
        }