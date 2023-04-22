
class Student():

    def __init__(self,id,cedula,fullname,correo,telefono,semestre,password) -> None:
        self.id = id
        self.cedula =cedula
        self.fullname = fullname
        self.correo = correo 
        self.telefono = telefono
        self.semestre = semestre
        self.password = password
    
    def to_JSON(self): #permite retornar los datos en json y asi no aparece error "json no serializable"
        return {

            "id": self.id,
            "cedula": self.cedula,
            "fullname": self.fullname,
            "correo": self.correo, 
            "telefono": self.telefono,
            "semestre": self.semestre,
            "password": self. password

        }

        