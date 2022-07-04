from django.db import models
from hello import db
from hello import ma

# Create your models here.
# class Greeting(models.Model):
#     when = models.DateTimeField("date created", auto_now_add=True)


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


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    idusuarios = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, rol):
        self.username = username
        self.password = password
        self.rol = rol

    # def __init__(self, idusuarios, username, password, rol):
    #     self.idusuarios = idusuarios
    #     self.username = username
    #     self.password = password
    #     self.rol = rol

class UsuariosSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password', 'rol', 'token', 'status')

class UsuariosIDSchema(ma.Schema):
    class Meta:
        fields = ('idusuarios', 'username', 'password', 'rol', 'token', 'status')

user_schema = UsuariosSchema()
userID_schema = UsuariosIDSchema()
usersID_schema = UsuariosIDSchema(many=True)
