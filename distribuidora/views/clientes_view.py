from flask import (Blueprint,request)
from flask.json import jsonify

from distribuidora import (app, db)

from distribuidora.models.clientes import (Clientes, clientes_schema,cliente_schema,clientesNew_schema)

clientes_view = Blueprint('clientes_view', __name__, url_prefix='')

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
