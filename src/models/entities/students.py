
class Student():

    def __init__(self,cedula,fullname= None,correo= None,telefono= None,semestre= None,password= None, estado = None) -> None:
    
        self.cedula =cedula
        self.fullname = fullname
        self.correo = correo 
        self.telefono = telefono
        self.semestre = semestre
        self.password = password
        self.estado = estado
    
    def to_JSON(self): #permite retornar los datos en json y asi no aparece error "json no serializable"
        return {

            "cedula": self.cedula,
            "nombre": self.fullname,
            "correo": self.correo, 
            "telefono": self.telefono,
            "semestre": self.semestre,
            "password": self. password,
            "estado ": self.estado

        }

        