class Docente():

    def __init__(self,cedula,fullname= None,correo= None,telefono= None,asignatura = None, password = None) -> None:
    
        self.cedula =cedula
        self.fullname = fullname
        self.correo = correo 
        self.telefono = telefono
        self.asignatura = asignatura
        self.password = password
    
    def to_JSON(self): #permite retornar los datos en json y asi no aparece error "json no serializable"
        return {

            "cedula": self.cedula,
            "nombre": self.fullname,
            "correo": self.correo, 
            "telefono": self.telefono,
            "asignatura": self.asignatura,
            "password": self.password

        }
