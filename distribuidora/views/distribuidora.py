from flask import (
    Blueprint, request, session, url_for
)
from flask.json import jsonify

from distribuidora import (app, db)

#Importar modelos
from distribuidora.models.pedidos import (Pedidos,pedidos_schema,pedidoID_schema,pedido_schema )
from distribuidora.models.productos import (Productos,productosVendidos_schema,totalesPorFecha_schema)
from distribuidora.models.usuarios import (Usuarios)
from distribuidora.models.pedido_productos import (Pedido_productos,pedidoprodtos_schema)
from distribuidora.models.clientes import (Clientes)

#Importar funciones de las diferentes vistas
from distribuidora.views.clientes_view import get_clienteOnlyOne
from distribuidora.views.auth import get_usuario
from distribuidora.views.productos_view import (get_onlyOne, update_stockProduct)



distribuidora = Blueprint('distribuidora', __name__, url_prefix='')

   
@distribuidora.route('/getProductosDelPedido/<id>',methods = ['GET'])
def get_productosDelPedido(id):
    all_productos = Pedido_productos.query.filter_by(idpedido = id)
    results = pedidoprodtos_schema.dump(all_productos)
    return jsonify(results) 

@distribuidora.route('/getPedidos',methods = ['GET'])
def get_pedidos():
    all_pedidos =  Pedidos.query.all()
    results = pedidos_schema.dump(all_pedidos)
    return jsonify(results)

@distribuidora.route('/getPedido/<idusuario>',methods = ['GET'])
def get_pedidosdelempleado(idusuario):
    all_pedidos = Pedidos.query.filter_by(idusuario = idusuario).all()
    results = pedidos_schema.dump(all_pedidos)
    return jsonify(results)

@distribuidora.route('/addPedido',methods = ['POST'])
def add_pedido():
    idclientes = request.json['idcliente']
    cli = get_clienteOnlyOne(idclientes)
    nombre = cli.json['nombre'] +" "+request.json['fecha']
 
    idusuario = get_usuario(request.json['usuario']).json['idusuarios']

    fecha = request.json['fecha']
    total = request.json['total']
    listaProd = request.json['productos']
    pedido = Pedidos(idclientes,nombre,fecha,total,idusuario)
    db.session.add(pedido)
    db.session.commit()
    idpedido = pedidoID_schema.jsonify(pedido).json['idpedidos']
    
    for x in listaProd:
        cantidad = x['cantidad']
        idproducto = x['idproductos']
        precio_unidad = x['precio']
        nombre = x['nombre']
        familia = x['familia']
        producto = Pedido_productos(idpedido,idproducto,cantidad,precio_unidad,nombre,familia)
        db.session.add(producto)
        db.session.commit()
    
    for x in listaProd:
        idproducto = x['idproductos']
        oldStock = get_onlyOne(idproducto)
        newStock = oldStock.json['stock'] - x['cantidad']
        update_stockProduct(idproducto,newStock)

    return pedido_schema.jsonify(pedido)

@distribuidora.route('/getPedidoPorFecha/<idusuario>/<fecha1>/<fecha2>',methods = ['GET'])
def get_pedidosPorFecha(idusuario,fecha1,fecha2):
    all_pedidos = Pedidos.query.filter(Pedidos.idusuario == idusuario, Pedidos.fecha >= fecha1, Pedidos.fecha <= fecha2).all()    
    results = pedidos_schema.dump(all_pedidos)
    return jsonify(results)
    
@distribuidora.route('/getTotalesPorFecha/<fecha1>/<fecha2>',methods = ['GET'])
def get_totalesPorFecha(fecha1,fecha2):
    all_totales = db.session.query(Usuarios.username, Pedidos.fecha, Clientes.zona, db.func.sum(Pedidos.total).label("total")).select_from(Pedidos).join(Usuarios, Usuarios.idusuarios == Pedidos.idusuario).join(Clientes, Clientes.idclientes == Pedidos.idclientes).filter(Pedidos.fecha >= fecha1, Pedidos.fecha <= fecha2).group_by(Usuarios.username, Pedidos.fecha, Clientes.zona).all()
    results = totalesPorFecha_schema.dump(all_totales)
    return jsonify(results)

@distribuidora.route('/getProdVendidosPorFecha/<fecha>',methods = ['GET'])
def getProductosVendidosPorFecha(fecha):
    all_productos = db.session.query(Productos.nombre, Productos.familia, db.func.sum(Pedido_productos.cantidad).label("cantidad")).select_from(Productos).join(Pedido_productos, Productos.idproductos == Pedido_productos.idproducto).join(Pedidos, Pedido_productos.idpedido == Pedidos.idpedidos).filter_by(fecha = fecha).group_by(Productos.idproductos).all()
    results = productosVendidos_schema.dump(all_productos)
    return jsonify(results)


