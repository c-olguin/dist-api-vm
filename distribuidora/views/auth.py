from flask import (
    Blueprint, request, session, url_for
)
from flask.json import jsonify

from distribuidora import (app, db)

from distribuidora.models.usuarios import (Usuarios, user_schema, usersID_schema, userID_schema)

import bcrypt
import jwt
import datetime

semilla = bcrypt.gensalt()

auth = Blueprint('auth', __name__, url_prefix='')

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