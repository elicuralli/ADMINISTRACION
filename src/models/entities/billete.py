

class Billete():
    def __init__(self, codigo = None, cantidad= None) -> None:
        self.codigo = codigo
        self.cantidad = cantidad 
    
    def to_JSON(self):
        {
            "codigo": self.codigo, 
            "cantidad": self.cantidad
        }