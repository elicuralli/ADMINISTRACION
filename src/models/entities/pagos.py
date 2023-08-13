class Pago():
    def __init__(self, id=None, cedula_estudiante=None, metodo_pago_id=None, monto_id=None,
                 fecha_pago=None, referencia_transferencia=None, referencia_billete=None):
        self.id = id
        self.cedula_estudiante = cedula_estudiante
        self.metodo_pago_id = metodo_pago_id
        self.monto_id = monto_id
        self.fecha_pago = fecha_pago
        self.referencia_transferencia = referencia_transferencia
        self.referencia_billete = referencia_billete
    
    def to_JSON(self):
        return {
            "id": self.id,
            "estudiante": self.estudiante.to_JSON(),  
            "metodo_pago_id": self.metodo_pago_id.to_JSON(),
            "monto_id": self.monto_id.to_JSON(),
            "fecha_pago": self.fecha_pago,
            "referencia_transferencia": self.referencia_transferencia.to_JSON() if self.referencia_transferencia else None,
            "referencia_billete": self.referencia_billete.to_JSON() if self.referencia_billete else None
        }
