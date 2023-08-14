import os


class Config:
    SECRET_KEY = 'madenco_web_2022'
    UPLOAD_FOLDER = os.path.abspath('../Productos')
    COTIZACION_FOLDER = os.path.abspath('../Cotizaciones')
    DOCS_FOLDER = os.path.abspath('./app/static/docs')

    # CACHE CONFIG
    CACHE_TYPE = "SimpleCache"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300


class ConfigDevelop(Config):
    DEBUG = True

    # BASE DE DATOS
    HOST = os.getenv('DEV_HOST')
    USER = os.getenv('DEV_USER')
    PASSWORD = os.getenv('DEV_PASSWORD')
    DB = os.getenv('DEV_DB')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # RECAPTCHA DEVELOP
    RECAPTCHA_PUBLIC_KEY = os.getenv('DEV_CAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('DEV_CAPTCHA_PRIVATE_KEY')

    # Google Analitics DEVELOP
    GOOGLE_ANALYTICS_ID = os.getenv('DEV_GOOGLE_ANALYTICS_ID')

    # CONFIGURACION MAIL
    MAIL_SERVER = 'smtp.gmail.com'

    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('DEV_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('DEV_MAIL_PASSWORD')

    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # FACEBOOK KEYS
    FACEBOOK_OAUTH_CLIENT_ID = 505647538341736
    FACEBOOK_OAUTH_CLIENT_SECRET = "f441e0e2531524489ae37ff6d53eb4bb"


class ConfigProduction(Config):
    DEBUG = False

    # BASE DE DATOS
    HOST = os.getenv('PROD_HOST')
    USER = os.getenv('PROD_USER')
    PASSWORD = os.getenv('PROD_PASSWORD')
    DB = os.getenv('PROD_DB')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # RECAPTCHA DEVELOP
    RECAPTCHA_PUBLIC_KEY = os.getenv('DEV_CAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('DEV_CAPTCHA_PRIVATE_KEY')
    # Google Analitics DEVELOP
    GOOGLE_ANALYTICS_ID = os.getenv('PROD_GOOGLE_ANALYTICS_ID')
    # CONFIGURACION MAIL
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('PROD_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('PROD_MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # CACHE CONFIG
    # CACHE_TYPE = "SimpleCache"  # Flask-Caching related configs
    # CACHE_DEFAULT_TIMEOUT = 300
