class Student():

    def __init__(self,cedula = None,fullname= None,correo= None,telefono= None,semestre= None,password= None, estado = None,carrera = None,edad = None,sexo = None, promedio = None,direccion = None,fecha_nac = None) -> None:
    
        self.cedula =cedula
        self.fullname = fullname
        self.correo = correo 
        self.telefono = telefono
        self.semestre = semestre
        self.password = password
        self.estado = estado
        self.carrera = carrera
        self.edad = edad 
        self.sexo = sexo
        self.promedio = promedio 
        self.direccion = direccion
        self.fecha_nac = fecha_nac
    
    def to_JSON(self): #permite retornar los datos en json y asi no aparece error "json no serializable"
        return {

            "cedula": self.cedula,
            "nombre": self.fullname,
            "correo": self.correo, 
            "telefono": self.telefono,
            "semestre": self.semestre,
            "estado": self.estado,
            "carrera": self.carrera,
            "edad": self.edad,
            "sexo": self.sexo,
            "promedio": self.promedio,
            "direccion":self.direccion,
            "fecha_nac": self.fecha_nac

        }

        