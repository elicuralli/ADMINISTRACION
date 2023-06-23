from marshmallow import Schema, fields

class EntityToJSONField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if hasattr(value, 'to_JSON'):
            return value.to_JSON()
        return value

class BaseResponseSchema(Schema):
    ok = fields.Boolean()
    status = fields.Integer()
    data = EntityToJSONField()
  
class CoordinacionSchema(Schema):
    cedula = fields.String()
    fullname = fields.String()
    correo = fields.String()
    telefono = fields.String()
    password = fields.String()


class BilleteSchema(Schema):
    codigo = fields.String()
    cantidad = fields.Integer()
    factura = fields.String()

class CarreraSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()

class ControlSchema(Schema):
    cedula = fields.String()
    fullname = fields.String()
    correo = fields.String()
    telefono = fields.String()
    password = fields.String()
    rol = fields.String()

class DocenteSchema(Schema):
    cedula = fields.String()
    fullname = fields.String()
    correo = fields.String()
    telefono = fields.String()
    password = fields.String()

class MateriasSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()
    prelacion = fields.String()
    unidad_credito = fields.Integer()
    hp = fields.Integer()
    ht = fields.Integer()
    semestre = fields.Integer()
    id_carrera = fields.Integer()
    id_docente = fields.Integer()

class StudentSchema(Schema):
    cedula = fields.String()
    fullname = fields.String()
    correo = fields.String()
    telefono = fields.String()
    semestre = fields.Integer()
    password = fields.String()
    estado = fields.String()
    carrera = fields.String()

class BilleteResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()

class CarreraResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()

class ControlResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()

class DocenteResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()

class MateriasResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()

class StudentResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()

class CoordinacionResponseSchema(BaseResponseSchema):
    data = EntityToJSONField()
