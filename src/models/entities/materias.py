class Materias():
    def __init__(self,id,nombre = None,prelacion= None,unidad_credito= None,hp= None,ht= None,semestre= None,id_carrera= None, id_docente = None,dia = None, hora_inicio = None, hora_fin = None, dia2 = None, hora_inicio2 = None, hora_fin2 = None, cantidad_estudiantes = None,ciclo = None,modalidad = None, maximo = None) -> None:
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
        self.dia2 = dia2
        self.hora_inicio2 = hora_inicio2
        self.hora_fin2 = hora_fin2
        self.cantidad_estudiantes = cantidad_estudiantes
        self.maximo = maximo
        self.ciclo = ciclo
        self.modalidad = modalidad
    
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
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "dia2": self.dia2,
            "hora_inicio2": self.hora_inicio2,
            "hora_fin2": self.hora_fin2,
            "maximo": self.maximo,
            "ciclo": self.ciclo,
            "modalidad": self.modalidad
        }
    
    def to_JSON_with_quantity(self):
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
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "dia2": self.dia2,
            "hora_inicio2": self.hora_inicio2,
            "hora_fin2": self.hora_fin2,
            "cantidad_estudiantes": self.cantidad_estudiantes,
            "maximo": self.maximo,
            "ciclo": self.ciclo,
            "modalidad": self.modalidad
        }
        