from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#Cargar las configuraciones
app.config.from_object('config.DevelopmentConfig')
# db = SQLAlchemy(app)
ma = Marshmallow(app)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

#Importar vistas
from hello.views import (auth, distribuidora, clientes_view, productos_view)
from hello.models import (Productos, productosVendidos_schema, totalesPorFecha_schema, productos_schema, producto_schema,productoNew_schema)
from flask.json import jsonify

app.register_blueprint(auth)
app.register_blueprint(distribuidora)
app.register_blueprint(clientes_view)
app.register_blueprint(productos_view)

db.create_all()

@app.route('/getProductos',methods = ['GET'])
def get_productos():
    try: 
        all_productos = Productos.query.all()
        results = productos_schema.dump(all_productos)
        return jsonify(results)
    except Exception as ee:
        print(ee)

@app.route('/hello',methods = ['GET'])
def hello():
    return print("Entrooooooooo")