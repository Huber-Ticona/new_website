from flask import Blueprint, render_template, jsonify, send_from_directory, current_app, abort
from html import escape
api_bp = Blueprint('api_bp', __name__, static_folder='static',
                   template_folder='templates')


# OBTENER IMAGEN DE UN PRODUCTO
@api_bp.route('/imagen-producto/<string:nombre>')
def imagen_producto(nombre=None):
    try:
        nombre = escape(nombre)
        # print('nombre: ' ,nombre)
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], nombre)
    except Exception as e:
        abort(404)

# OBTENER IMAGEN DE UN PRODUCTO EN CARPETA


@api_bp.route('/imagen-producto/<string:carpeta>/<string:nombre>')
def imagen_producto_carpeta(carpeta=None, nombre=None):
    try:
        new_nombre = escape(nombre)
        print(f'Nombre: {nombre} | new nombre: {new_nombre}')
        return send_from_directory(current_app.config['UPLOAD_FOLDER'] + '/' + carpeta, new_nombre)
    except Exception as e:
        return str(e)


@api_bp.errorhandler(404)
def page_not_found(e):
    print('ERROR 404')
    return render_template('404.html')
