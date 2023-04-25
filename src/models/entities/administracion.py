class Administracion():

    def __init__(self, id,pre_inscripcion = None, inscripcion = None, cuota1= None,cuota2= None,cuota3= None,cuota4= None,cuota5= None) -> None:
        self.id = id
        self.pre_inscripcion = pre_inscripcion
        self.inscripcion = inscripcion
        self.cuota1 = cuota1
        self.cuota2 = cuota2
        self.cuota3= cuota3
        self.cuota4= cuota4
        self.cuota5 = cuota5
    
    def to_JSON(self):
        return {
            "id": self.id,
            "pre_inscripcion":self.pre_inscripcion,
            "inscripcion": self.inscripcion,
            "cuota 1": self.cuota1,
            "cuota 2": self.cuota2,
            "cuota 3": self.cuota3,
            "cuota 4": self.cuota4,
            "cuota 5": self.cuota5
        }
        
