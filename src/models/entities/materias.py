class Materias():
    def __init__(self,id,nombre = None,prelacion= None,unidad_credito= None,hp= None,ht= None,semestre= None,id_carrera= None, id_docente = None,dia = None, hora_inicio = None, hora_fin = None) -> None:
        self.id = id
        self.nombre = nombre 
        self.prelacion = prelacion 
        self.unidad_credito = unidad_credito
        self.hp = hp
        self.ht = ht
        self.semestre = semestre
        self.id_carrera = id_carrera
        self.id_docente = id_docente
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
    
    def to_JSON(self):
        return {
            
            "id": self.id,
            "nombre": self.nombre,
            "prelacion": self.prelacion,
            "unidad_credito": self.unidad_credito,
            "hp": self.hp,
            "ht": self.ht,
            "semestre": self.semestre,
            "id_carrera": self.id_carrera,
            "id_docente": self.id_docente,
            "dia": self.dia,
            "hora inicio": self.hora_inicio,
            "hora fin": self.hora_fin
        }
        