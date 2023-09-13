class Docente():

    def __init__(self,cedula = None,fullname= None,correo= None,telefono= None, password = None) -> None:
    
        self.cedula =cedula
        self.fullname = fullname
        self.correo = correo 
        self.telefono = telefono
        self.password = password
    
    def to_JSON(self): #permite retornar los datos en json y asi no aparece error "json no serializable"
        return {

            "cedula": self.cedula,
            "nombre": self.fullname,
            "correo": self.correo, 
            "telefono": self.telefono,
         

        }
