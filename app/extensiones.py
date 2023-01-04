from flask_caching import Cache
import pymysql
from flask_login import LoginManager

login_manager = LoginManager()

cache = Cache()

def obtener_conexion():
    return pymysql.connect(host='localhost',user='root',password='huber123', db='madenco_web')

#def obtener_conexion():
#    return pymysql.connect(host='localhost',user='root',password='Enco$0011',db='madenco_web')
