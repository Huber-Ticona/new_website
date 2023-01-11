from flask_caching import Cache
import pymysql
from flask_login import LoginManager
from flask import current_app
from flask_mail import Mail

login_manager = LoginManager()

cache = Cache()

mail = Mail()

def obtener_conexion():
    return pymysql.connect(
        host=current_app.config['HOST'],
        user=current_app.config['USER'],
        password=current_app.config['PASSWORD'], 
        db=current_app.config['DB'])


