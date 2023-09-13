class Transferencia():
    def __init__(self, id = None, codigo_referencia= None) -> None:
        self.id = id
        self.codigo_referencia = codigo_referencia
    
    def to_JSON(self) -> dict:
       return {
            "id": self.id,
            "codigo_referencia": self.codigo_referencia,
        }