
class MateriaEstudiante():
    def __init__(self,cod_materia = None, cedula_estudiante= None,nota1= None,porc1= None,nota2= None,porc2= None,nota3= None,porc3= None) -> None:
        self.cod_materia = cod_materia
        self.cedula_estudiante = cedula_estudiante
        self.nota1 = nota1
        self.porc1 = porc1
        self.nota2 = nota2
        self.porc2 = porc2
        self.nota3 = nota3
        self.porc3 = porc3
    
    def materiaEstudiante_toJSON(self):
        return {

        "cod_materia": self.cod_materia,
        "cedula_estudiante":self.cedula_estudiante,
        "nota1":self.nota1,
        "porc1": self.porc1,
        "nota2":self.nota2,
        "porc2": self.porc2,
        "nota3": self.nota3,
        "porc3": self.porc3
                           
        }