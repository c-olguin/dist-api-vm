from distribuidora import db
from distribuidora import ma

class Clientes(db.Model):
    idclientes = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    cuit = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(50), nullable=False)
    zona = db.Column(db.String(50), nullable=False)

    # def __init__(self, idclientes,nombre, direccion, cuit, telefono, zona):
    #     self.idclientes = idclientes
    #     self.nombre = nombre
    #     self.direccion = direccion
    #     self.cuit = cuit
    #     self.telefono = telefono
    #     self.zona = zona

    def __init__(self,nombre, direccion, cuit, telefono, zona):
        self.nombre = nombre
        self.direccion = direccion
        self.cuit = cuit
        self.telefono = telefono
        self.zona = zona

class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('idclientes','nombre', 'direccion', 'cuit', 'telefono', 'zona')

class NewClientesSchema(ma.Schema):
    class Meta:
        fields = ('nombre', 'direccion', 'cuit', 'telefono', 'zona')

cliente_schema = ClientesSchema()
clientesNew_schema = NewClientesSchema()
clientes_schema = ClientesSchema(many=True)
