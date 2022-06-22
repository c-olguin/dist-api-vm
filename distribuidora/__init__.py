from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#Cargar las configuraciones
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Importar vistas
from distribuidora.views.auth import auth
app.register_blueprint(auth)

from distribuidora.views.distribuidora import distribuidora
app.register_blueprint(distribuidora)

from distribuidora.views.clientes_view import clientes_view
app.register_blueprint(clientes_view)

from distribuidora.views.productos_view import productos_view
app.register_blueprint(productos_view)

db.create_all()