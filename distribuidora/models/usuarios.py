from distribuidora import db
from distribuidora import ma

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
