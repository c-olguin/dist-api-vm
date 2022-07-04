class Config:
    DEBUG = True
    TESTING = True

    #Configuracion base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://u276789818_distribuidora:HostCami2021@212.1.208.1:3306/u276789818_distHostinger"
    POOL_PRE_PING = True

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    # SECRET_KEY = 'dev'
    DEBUG = True
    TESTING = True