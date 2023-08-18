class Factura:
    def __init__(self, id):
        self.id = id
    
    def to_JSON(self):
        return{
            "id": self.id
        }