class Billete():
    def __init__(self, id = None, serial= None, monto = None) -> None:
        self.id = id
        self.serial = serial
        self.monto = monto
    
    def to_JSON(self) -> dict:
       return {
            "id": self.id,
            "serial": self.serial,
            "monto":self.monto
        }