
class Configuracion():
    def __init__(self,id = None,ciclo = None,porc1 = None,porc2 = None,porc3= None,horario_inicio = None,horario_fin = None,cuota1 = None,cuota2 = None,cuota3 = None,cuota4 = None,cuota5 = None) -> None:
        self.id = id
        self.ciclo = ciclo 
        self.porc1 = porc1
        self.porc2 = porc2
        self.porc3 = porc3
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.cuota1 = cuota1
        self.cuota2 = cuota2
        self.cuota3 = cuota3
        self.cuota4 = cuota4
        self.cuota5 = cuota5

    
    def to_JSON(self):
        return{

            "id": self.id,
            "ciclo": self.ciclo,
            "porc1": self.porc1,
            "porc2":self.porc2,
            "porc3": self.porc3,
            "horario_inicio": self.horario_inicio,
            "horario_fin": self.horario_fin,
            "cuota1": self.cuota1,
            "cuota2": self.cuota2,
            "cuota3": self.cuota3,
            "cuota4": self.cuota4,
            "cuota5": self.cuota5
        }
        