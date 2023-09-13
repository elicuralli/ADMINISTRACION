class Monto():

    def __init__(self, id = None, concepto = None, monto= None) -> None:
        self.id = id
        self.concepto = concepto
        self.monto = monto
       
    def to_JSON(self):
        return {
            "id": self.id,
            "concepto": self.concepto,
            "monto": self.monto
        }
        
