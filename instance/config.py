import os

class Config:
    SECRET_KEY = 'madenco_web_2022'
    UPLOAD_FOLDER = os.path.abspath('../Productos')

    # CACHE CONFIG
    CACHE_TYPE = "SimpleCache"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300

class ConfigDevelop(Config):
    DEBUG = True

    # BASE DE DATOS
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'huber123'
    DB = 'madenco_web'

    # RECAPTCHA
    RECAPTCHA_PUBLIC_KEY = '6Lc0S9ojAAAAAMQGIqpU6I8XL3yac7HpZrE5zMI6'
    RECAPTCHA_PRIVATE_KEY = '6Lc0S9ojAAAAAEKcEdlXwoP3g-1rEGsvaSHdDiwW'
    
    # CONFIGURACION MAIL
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'xmundial.streameryt1998@gmail.com'
    MAIL_PASSWORD = 'pkoenqywblyinssq'
    MAIL_USE_TLS = False
    MAIL_USE_SSL= True
    
    # FACEBOOK KEYS
    #FACEBOOK_OAUTH_CLIENT_ID = 904937283850756
    #FACEBOOK_OAUTH_CLIENT_SECRET = "8669b4001196541e776aee527a76eeb3"
    

class ConfigProduction(Config):
    DEBUG = False 

    # BASE DE DATOS
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'Enco$0011'
    DB = 'madenco_web'
    
    # CACHE CONFIG
    #CACHE_TYPE = "SimpleCache"  # Flask-Caching related configs
    #CACHE_DEFAULT_TIMEOUT = 300
