class Transferencia():
    def __init__(self, id = None, codigo_referencia= None, metodo_pago = None) -> None:
        self.id = id
        self.codigo_referencia = codigo_referencia
        self.metodo_pago = metodo_pago
    
    def to_JSON(self) -> dict:
       return {
            "id": self.id,
            "codigo_referencia": self.codigo_referencia,
            "metodo_pago":self.metodo_pago
        }