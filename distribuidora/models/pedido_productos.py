from distribuidora import db
from distribuidora import ma

class Pedido_productos(db.Model):
    idpedido = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unidad = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    familia = db.Column(db.String(100), nullable=False)

    def __init__(self, idpedido, idproducto, cantidad, precio_unidad, nombre, familia):
        self.idpedido = idpedido
        self.idproducto = idproducto
        self.cantidad = cantidad
        self.precio_unidad = precio_unidad
        self.nombre = nombre
        self.familia = familia
       

class PedidosProdSchema(ma.Schema):
    class Meta:
        fields = ('idpedido', 'idproducto', 'cantidad', 'precio_unidad', 'nombre', 'familia')

pedidoprod_schema = PedidosProdSchema()
pedidoprodtos_schema = PedidosProdSchema(many=True)
