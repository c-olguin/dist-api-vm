from distribuidora import db
from distribuidora import ma

class Productos(db.Model):
    idproductos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    familia = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)


    # def __init__(self,idproductos ,nombre, familia, stock, precio):
    #     self.idproductos = idproductos
    #     self.nombre = nombre
    #     self.familia = familia
    #     self.stock = stock
    #     self.precio = precio
    
    def __init__(self ,nombre, familia, stock, precio):
        self.nombre = nombre
        self.familia = familia
        self.stock = stock
        self.precio = precio



class ProductosSchema(ma.Schema):
    class Meta:
        fields = ('idproductos','nombre', 'familia', 'stock', 'precio')

class NewProductosSchema(ma.Schema):
    class Meta:
        fields = ('nombre', 'familia', 'stock', 'precio')

class ProductosVendidos(ma.Schema):
    class Meta:
        fields = ('nombre', 'familia', 'cantidad')

class TotalesPorFechas(ma.Schema):
    class Meta:
        fields = ('fecha', 'total')

producto_schema = ProductosSchema()
productoNew_schema = NewProductosSchema()
productos_schema = ProductosSchema(many=True)
productosVendidos_schema = ProductosVendidos(many=True)
totalesPorFecha_schema = TotalesPorFechas(many=True)

