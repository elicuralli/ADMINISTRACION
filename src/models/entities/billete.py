class Billete():
    def __init__(self, codigo = None, cantidad= None, factura = None) -> None:
        self.codigo = codigo
        self.cantidad = cantidad
        self.factura = factura
    
    def to_JSON(self) -> dict:
       return {
            "codigo": self.codigo, 
            "cantidad": self.cantidad,
            "factura": self.factura
        }