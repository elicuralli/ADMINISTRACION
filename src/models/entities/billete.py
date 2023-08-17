class Billete():
    def __init__(self, id = None, serial= None, monto = None, metodo_pago_id = None) -> None:
        self.id = id
        self.serial = serial
        self.monto = monto
        self.metodo_pago = metodo_pago_id
    
    def to_JSON(self) -> dict:
       return {
            "id": self.id,
            "serial": self.serial,
            "monto":self.monto,
            "metodo_pago": self.metodo_pago
        }