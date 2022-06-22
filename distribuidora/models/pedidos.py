from distribuidora import db
from distribuidora import ma

class Pedidos(db.Model):
    idpedidos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idclientes = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    idusuario = db.Column(db.Integer, primary_key=True)

    # def __init__(self, idpedidos, idclientes, nombre, fecha, total, idusuario):
    #     self.idpedidos = idpedidos
    #     self.idclientes = idclientes
    #     self.nombre = nombre
    #     self.fecha = fecha
    #     self.total = total
    #     self.idusuario = idusuario

    def __init__(self, idclientes, nombre, fecha, total, idusuario):
        self.idclientes = idclientes
        self.nombre = nombre
        self.fecha = fecha
        self.total = total
        self.idusuario = idusuario

class PedidosSchema(ma.Schema):
    class Meta:
        fields = ('idclientes', 'nombre', 'fecha', 'total', 'idusuario')

class PedidosIDSchema(ma.Schema):
    class Meta:
        fields = ('idpedidos', 'idclientes', 'nombre', 'fecha', 'total', 'idusuario')

pedido_schema = PedidosSchema()
pedidoID_schema = PedidosIDSchema()
pedidos_schema = PedidosIDSchema(many=True)
