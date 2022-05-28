from flask import Blueprint, render_template, jsonify
from database import obtener_conexion
api_bp = Blueprint('api_bp', __name__, static_folder='static', template_folder='templates')

@api_bp.route('/producto')
def productos():
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
    
            sql = "select * from producto"
            cursor.execute( sql )
            consulta = cursor.fetchall()

            print(consulta)
            return render_template('producto.html'  , productos = consulta)
        

    finally:
        miConexion.close()

@api_bp.route('/tienda')
def tienda():
    miConexion = obtener_conexion()
    try:
        with miConexion.cursor() as cursor:
    
            sql = "select nombre,categoria,precio from producto"
            cursor.execute( sql )
            consulta = cursor.fetchall()
            print(consulta)

            return render_template('tienda.html' , productos = consulta )
    finally:
        miConexion.close()