
class Peticiones():
    def __init__(self,id,id_docente = None,descripcion = None,estado = None,id_estudiante = None,id_materia = None,campo =None) -> None:
        self.id = id
        self.id_docente = id_docente
        self.descripcion = descripcion
        self.estado = estado 
        self.id_estudiante = id_estudiante
        self.id_materia = id_materia
        self.campo = campo

    def to_JSON(self):
        return {

            "id": self.id,
            "id_docente": self.id_docente,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "id_estudiante":self.id_estudiante,
            "id_materia": self.id_materia,
            "campo": self.campo

        }