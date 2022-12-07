from flask import Blueprint, render_template, jsonify,send_file
api_bp = Blueprint('api_bp', __name__, static_folder='static', template_folder='templates')


# OBTENER IMAGEN DE UN PRODUCTO
@api_bp.route('/imagen-producto/<string:nombre>')
def imagen_producto(nombre = None):
	try:
		return send_file('Productos/'+ nombre , download_name = nombre)
	except Exception as e:
		return str(e)
