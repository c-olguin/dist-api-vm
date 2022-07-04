from django.shortcuts import render
from django.http import HttpResponse
from hello import app
from flask import (
    Blueprint, request, session, url_for
)
from flask.json import jsonify

from hello import (app, db)

#Importar modelos
# from hello.models.usuarios import (Usuarios, user_schema, usersID_schema, userID_schema)
# from hello.models.clientes import (Clientes, clientes_schema,cliente_schema,clientesNew_schema)
# from hello.models.productos import (Productos, productosVendidos_schema, totalesPorFecha_schema, productos_schema, producto_schema,productoNew_schema)
# from hello.models.pedidos import (Pedidos,pedidos_schema,pedidoID_schema,pedido_schema )
# from hello.models.pedido_productos import (Pedido_productos,pedidoprodtos_schema)

from hello.models import (Usuarios, user_schema, usersID_schema, userID_schema)
from hello.models import (Clientes, clientes_schema,cliente_schema,clientesNew_schema)
from hello.models import (Productos, productosVendidos_schema, totalesPorFecha_schema, productos_schema, producto_schema,productoNew_schema)
from hello.models import (Pedidos,pedidos_schema,pedidoID_schema,pedido_schema )
from hello.models import (Pedido_productos,pedidoprodtos_schema)


import requests #
import bcrypt
import jwt
import datetime
import json

# from .models import Greeting

semilla = bcrypt.gensalt()

auth = Blueprint('auth', __name__, url_prefix='')
clientes_view = Blueprint('clientes_view', __name__, url_prefix='')
distribuidora = Blueprint('hello', __name__, url_prefix='')
productos_view = Blueprint('productos_view', __name__, url_prefix='')


# Create your views here.
# def index(requests):
#     # r = requests.get('https://httpbin.org/status/418')
#     # print(r.text)
#     # return HttpResponse('<pre>' + r.text + '</pre>')
#     # if __name__ == '__main__':
#     app.run()

#-------------
#New session
def index(request):
    try: 
        all_productos = Productos.query.all()
        results = productos_schema.dump(all_productos)
        # return jsonify(results)
        return HttpResponse(json.dumps(results), content_type="application/json")
        # return HttpResponse(jsonify(results))
    except Exception as ee:
        print(ee)
        return HttpResponse(json.dumps(ee), content_type="application/json")


def getEmpleados(request):
    all_empleados = Usuarios.query.filter_by(rol = 'EMPLEADO').all()
    results = usersID_schema.dump(all_empleados)
    # return jsonify(results)
    return HttpResponse(json.dumps(results), content_type="application/json")

#--------------


# def db(request):

#     greeting = Greeting()
#     greeting.save()

#     greetings = Greeting.objects.all()

#     return render(request, "db.html", {"greetings": greetings})


@auth.route('/registrar',methods = ['POST'])
def registrar():
    username = request.json['username']
    password = request.json['password']
    rol = request.json['rol']

    newUsername = Usuarios.query.filter_by(username = username).first()
    if newUsername != None:
        return "Este usuario ya esta registrado"
    else:
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode,semilla)

        newUser = Usuarios(username,password_encriptado,rol)
        db.session.add(newUser)
        db.session.commit()

        return user_schema.jsonify(newUser)

@auth.route('/login',methods = ['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    password_encode = password.encode("utf-8")

    newUser = Usuarios.query.filter_by(username = username).first()
    if newUser != None:
        password_encriptado_encode = newUser.password.encode()
        if (bcrypt.checkpw(password_encode,password_encriptado_encode)):
            token = jwt.encode({'public_id': newUser.idusuarios, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
            session['nombre']=username
            session['rol']=newUser.rol
            newUser.token = token
            newUser.status = 1
            return user_schema.jsonify(newUser)
        else:
            return user_schema.jsonify({'password': "", 'rol': "", 'token': "", 'username': "Contraseña Incorrecta", 'status': 0 })
            # return error_response("Contraseña Incorrecta")
    else:
        return user_schema.jsonify({'password': "", 'rol': "", 'token': "", 'username': "El usuario no esta registrado", 'status': 2 })
    
@auth.route('/getEmpleados',methods = ['GET'])
def get_empleados():
    all_empleados = Usuarios.query.filter_by(rol = 'EMPLEADO').all()
    results = usersID_schema.dump(all_empleados)
    return jsonify(results)

@auth.route('/getIdUsuario/<username>',methods = ['GET'])
def get_usuario(username):
    user = Usuarios.query.filter_by(username = username).first()
    results = userID_schema.dump(user)
    return jsonify(results)


@clientes_view.route('/getClientes/<id>',methods = ['GET'])
def get_clienteOnlyOne(id):
    cliente = Clientes.query.get(id)
    results = cliente_schema.dump(cliente)
    return jsonify(results)

@clientes_view.route('/addCliente',methods = ['POST'])
def add_cliente():
    print(request)
    nombre = request.json['nombre']
    direccion = request.json['direccion']
    cuit = request.json['cuit']
    telefono = request.json['telefono']
    zona = request.json['zona']

    cli = Clientes(nombre,direccion,cuit,telefono,zona)
    db.session.add(cli)
    db.session.commit()
    return clientesNew_schema.jsonify(cli)

@clientes_view.route('/getClientes',methods = ['GET'])
def get_clientes():
    all_clientes = Clientes.query.all()
    results = clientes_schema.dump(all_clientes)
    return jsonify(results)

    
@clientes_view.route('/deleteCli/<id>/',methods = ['DELETE'])
def delete_cli(id):
    clien = Clientes.query.get(id)
    db.session.delete(clien)
    db.session.commit()

    return cliente_schema.jsonify(clien)


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


@productos_view.route('/getProductos/<id>/',methods = ['GET'])
def get_onlyOne(id):
    producto = Productos.query.get(id)
    return producto_schema.jsonify(producto)

def update_stockProduct(id,stock):
    prod = Productos.query.get(id)
    prod.stock = stock
    db.session.commit()
    return producto_schema.jsonify(prod)

@productos_view.route('/addProducto',methods = ['POST'])
def add_producto():
    nombre = request.json['nombre']
    familia = request.json['familia']
    stock = request.json['stock']
    precio = request.json['precio']

    prod = Productos(nombre,familia,stock,precio)
    db.session.add(prod)
    db.session.commit()
    return productoNew_schema.jsonify(prod)

@productos_view.route('/updateProd/<id>/',methods = ['PUT'])
def update_prod(id):
    prod = Productos.query.get(id)

    stock = request.json['stock']
    precio = request.json['precio']
    
    prod.stock = stock
    prod.precio = precio

    db.session.commit()
    return producto_schema.jsonify(prod)
    

@productos_view.route('/getProductos',methods = ['GET'])
def get_productos():
    try: 
        all_productos = Productos.query.all()
        results = productos_schema.dump(all_productos)
        return jsonify(results)
    except Exception as ee:
        print(ee)

@productos_view.route('/deleteProd/<id>/',methods = ['DELETE'])
def delete_prod(id):
    prod = Productos.query.get(id)
    db.session.delete(prod)
    db.session.commit()

    return producto_schema.jsonify(prod)


