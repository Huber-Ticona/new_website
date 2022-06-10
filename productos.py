
from flask import Blueprint, render_template, send_file
from markupsafe import escape
from database import obtener_conexion
productos_bp = Blueprint('productos_bp', __name__, static_folder='static', template_folder='templates')

@productos_bp.route('/producto/categorias' , methods=['GET'])
def obt_categorias(nombre = None):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
    
            
            '''cursor.execute( nombre )
            consulta = cursor.fetchall()
            print(consulta)'''

            return nombre
    finally:
        miConexion.close()

@productos_bp.route('/mejores_productos' , methods=['GET'])
def obt_mejores_productos():
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
    
            sql = "select * from producto"
            cursor.execute( sql )
            consulta = cursor.fetchall()

            print(consulta)
            return "hola mejores productos"

    finally:
        miConexion.close()

@productos_bp.route('/producto/<string:nombre>' , methods=['GET'])
def obt_producto(nombre = None):
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
    
            
            '''cursor.execute( nombre )
            consulta = cursor.fetchall()
            print(consulta)'''

            return nombre
    finally:
        miConexion.close()

@productos_bp.route('/imagen-producto/<string:nombre>')
def imagen_producto(nombre = None):
	try:
		return send_file('Productos\\'+ nombre , download_name = nombre)
	except Exception as e:
		return str(e)