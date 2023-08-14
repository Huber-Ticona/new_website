
from flask import Blueprint, abort, jsonify, render_template, send_file, request, session, url_for
from html import escape
import json

from ..modelos.ModeloProducto import ModeloProducto
from ..modelos.ModeloCategoria import ModeloCategoria

tienda_bp = Blueprint('tienda_bp', __name__,
                      static_folder='static', template_folder='templates')


@tienda_bp.route('')
@tienda_bp.route('<string:enombre1>')
@tienda_bp.route('<string:enombre1>/<string:enombre2>')
@tienda_bp.route('<string:enombre1>/<string:enombre2>/<string:enombre3>')
# @cache.cached(timeout=30)
def tienda_productos(enombre1=None, enombre2=None, enombre3=None):
    precio_min = request.args.get('precio_min')  # Pueden ser None
    precio_max = request.args.get('precio_max')  # Pueden ser None
    marcas = request.args.getlist('marca')
    marcas = [int(marca_id) for marca_id in marcas]
    orden = request.args.get('orden')
    print(f'rango precio | min: {precio_min} | max: {precio_max}')
    print(f'marcas: {marcas} ')
    print(f'ordenamiento: {orden}')
    miga_pan = []  # [nivel 1 , nivel 2 , nivel 3 ]
    x = []  # LISTA PRODUCTOS A MOSTRAR
    y = []  # LISTA DE SUBCATEGORIAS A MOSTRAR
    z = []
    dicc = {}
    if enombre1 != None and enombre2 != None and enombre3 != None:
        dnombre1 = escape(enombre1.replace('-', ' '))
        dnombre2 = escape(enombre2.replace('-', ' '))
        dnombre3 = escape(enombre3.replace('-', ' '))
        print(
            f'nombre1: {dnombre1} | nombre2: {dnombre2} | nombre3: {dnombre3}')
        categoria1 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(
            nombre=dnombre1, padre_id=1)
        if categoria1 == None:
            print('categoria lvl 1 incorrecta --> abortando busqueda')
            abort(404)

        categoria2 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(
            nombre=dnombre2, padre_id=categoria1[0])
        if categoria2 == None:
            print('categoria lvl 2 incorrecta --> abortando busqueda')
            abort(404)
        categoria3 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(
            nombre=dnombre3, padre_id=categoria2[0])
        x = ModeloProducto.obtener_productos_x_categoria(
            categoria3[0], orden)
        z = ModeloProducto.obtener_distintas_marcas_x_categoria(categoria2[0])
        miga_pan = [enombre1, enombre2, enombre3]

    elif enombre1 != None and enombre2 != None:
        dnombre1, dnombre2 = escape(enombre1.replace(
            '-', ' ')), escape(enombre2.replace('-', ' '))

        print(f'nombre1: {dnombre1} | nombre2: {dnombre2}')
        categoria1 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(
            nombre=dnombre1, padre_id=1)
        if categoria1 == None:
            print('categoria lvl 1 incorrecta --> abortando busqueda')
            abort(404)

        categoria2 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(
            nombre=dnombre2, padre_id=categoria1[0])
        if categoria2 == None:
            print('categoria lvl 2 incorrecta --> abortando busqueda')
            abort(404)

        print('Categoria lvl 1 y 2 correcta ---> Obteniendo Productos y subcategorias')
        # x = ModeloProducto.obtener_productos_x_categoria(categoria2[0], orden)
        x = ModeloProducto.obtener_productos_x_categoria(
            categoria2[0], orden, marcas, precio_min, precio_max)
        y = ModeloCategoria.obtener_categorias_hijas_x_padre(categoria2[0])
        z = ModeloProducto.obtener_distintas_marcas_x_categoria(categoria2[0])
        miga_pan = [enombre1, enombre2]

    elif enombre1 != None:
        dnombre1 = escape(enombre1.replace('-', ' '))
        print(f'nombre1: {dnombre1}')

        categoria1 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(
            nombre=dnombre1, padre_id=1)
        if categoria1 == None:
            print('categoria lvl 1 incorrecta --> abortando busqueda')
            abort(404)
        print('Categoria lvl 1 correcta ---> Obteniendo Productos y subcategorias 1 y 2')
        x = ModeloProducto.obtener_productos_x_categoria(
            categoria1[0], orden, marcas, precio_min, precio_max)
        y = ModeloCategoria.obtener_categorias_hijas_x_padre(categoria1[0])
        z = ModeloProducto.obtener_distintas_marcas_x_categoria(categoria1[0])
        miga_pan = [enombre1]
    else:
        x = ModeloProducto.todos_los_productos()

    dicc['productos'] = x
    dicc['subcategorias'] = y
    dicc['marcas'] = z
    dicc['miga_pan'] = miga_pan
    print('miga_pan: ', miga_pan)

    return render_template('tienda/tienda.html', dicc=dicc)


@tienda_bp.route('/producto/<string:nombre>', methods=['GET', 'POST'])
def vista_producto(nombre=None):
    if nombre != None:
        print('-'*5 + f'PRODUCTO {nombre} ' + '-'*5)
        print('-'*5 + f'PRODUCTO escape {escape(nombre)} ' + '-'*5)
        consulta = ModeloProducto.obtener_producto_x_nombre(nombre)

        print(consulta)
        if consulta == None:
            abort(404)
        return render_template('tienda/producto.html', producto=consulta)


@tienda_bp.route('/buscar-producto', methods=['POST'])
def search():
    data = request.json
    print(data)
    nombre_producto = data['producto']
    x = ModeloProducto.buscador_de_productos(nombre_producto)
    return jsonify({
        "productos": x
    })


@tienda_bp.route('/arbol/<int:id>')
def arbol(id=None):
    # Obtener los hijos de nivel 2 y subhijos de nivel 3 de la categoría con ID 1
    hijos_nivel2, subhijos_nivel3 = ModeloCategoria.obtener_hijos_subhijos(id)
    print('HIJOS LVL 2:', hijos_nivel2)
    print('SUBHIJOS LVL 3:', subhijos_nivel3)
    return 'EXITO'


@tienda_bp.errorhandler(404)
def page_not_found(e):
    print('ERROR 404 tienda_bp')
    return render_template('404.html')
