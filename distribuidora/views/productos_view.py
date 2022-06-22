from flask import (Blueprint,request)
from flask.json import jsonify

from distribuidora import (app, db)

from distribuidora.models.productos import (Productos, productos_schema, producto_schema,productoNew_schema)

productos_view = Blueprint('productos_view', __name__, url_prefix='')

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