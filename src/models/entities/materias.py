class Materias():
    def __init__(self,id,nombre = None,prelacion= None,unidad_credito= None,hp= None,ht= None,semestre= None,id_carrera= None) -> None:
        self.id = id
        self.nombre = nombre 
        self.prelacion = prelacion 
        self.unidad_credito = unidad_credito
        self.hp = hp
        self.ht = ht
        self.semestre = semestre
        self.id_carrera = id_carrera
    
    def to_JSON(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "prelacion": self.prelacion,
            "unidad_credito": self.unidad_credito,
            "hp": self.hp,
            "ht": self.ht,
            "semestre": self.semestre,
            "id_carrera": self.id_carrera
        }
        