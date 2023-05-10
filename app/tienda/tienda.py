
from flask import Blueprint, abort, jsonify, render_template, send_file, request, session, url_for
from html import escape
import json
from ..extensiones import cache
from ..modelos.ModeloProducto import ModeloProducto
from ..modelos.ModeloCategoria import ModeloCategoria
from ..modelos.ModeloCotizacion import ModeloCotizacion

tienda_bp = Blueprint('tienda_bp', __name__,
                      static_folder='static', template_folder='templates')


@tienda_bp.route('')
@tienda_bp.route('<string:enombre1>')
@tienda_bp.route('<string:enombre1>/<string:enombre2>')
@tienda_bp.route('<string:enombre1>/<string:enombre2>/<string:enombre3>')
# @cache.cached(timeout=30)
def tienda_productos(enombre1=None, enombre2=None, enombre3=None):
    miga_pan = []  # [nivel 1 , nivel 2 , nivel 3 ]
    x = []  # LISTA PRODUCTOS A MOSTRAR
    y = []  # LISTA DE SUBCATEGORIAS A MOSTRAR
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
        x = ModeloProducto.obtener_productos_x_categoria(categoria3[0])
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
        x = ModeloProducto.obtener_productos_x_categoria(categoria2[0])
        y = ModeloCategoria.obtener_categorias_hijas_x_padre(categoria2[0])
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
        x = ModeloProducto.obtener_productos_x_categoria(categoria1[0])
        y = ModeloCategoria.obtener_categorias_hijas_x_padre(categoria1[0])
        miga_pan = [enombre1]

    dicc['productos'] = x
    dicc['subcategorias'] = y
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


@tienda_bp.route('/agregar_al_carro', methods=['POST'])
def agregar_al_carro():

    if request.method == 'POST':
        print('------ AGREGANDO AL CARRO ---------')
        dato = request.json
        print('PRODUCTO: ', dato)
        mensaje = ''
        if 'carro_temporal' in session:
            carro = session['carro_temporal']
            productos = carro['productos']
            existe = False
            for producto in productos:
                if producto['producto_id'] == dato['producto_id']:
                    existe = True
                    producto['cantidad'] = producto['cantidad'] + \
                        dato['cantidad']
                    break
            if not existe:
                carro['productos'].append(dato)
            # actualiza el carro
            mensaje = 'Carro Actualizado'
            session['carro_temporal'] = carro
        else:
            carro = {
                "productos": [dato]
            }
            mensaje = 'Producto agregado al carro'
            # crea el carro
            session['carro_temporal'] = carro
        print('carro despues: ', session['carro_temporal'])
        print('-'*10)

        return jsonify(mensaje=mensaje, producto=dato)


@tienda_bp.route('/ver_carro', methods=['POST'])
def ver_carro():
    carro = []
    if request.method == 'POST':

        if 'carro_temporal' in session:
            carro = session['carro_temporal']
            print(carro)
            print('enviando')

    return render_template('tienda/carro_lista.html', carro=carro)
   # return jsonify( productos = carro )


@tienda_bp.route('/vaciar-carro', methods=['GET'])
def vaciar_carro():

    if 'carro_temporal' in session:
        session.pop('carro_temporal', None)

    return jsonify(mensaje='Carrito de compras vaciado.')


@tienda_bp.route('/mi-carro')
def mi_carro():
    carro = []
    if 'carro_temporal' in session:
        carro = session['carro_temporal']

    return render_template('tienda/carro.html', carro=carro)


@tienda_bp.route('/keys')
def cache_keys():
    claves = cache.cache._cache.keys()
    print('claves: ', claves)
    for i in claves:
        x = cache.get(i)
        print(f'CLAVE: {i} | VALOR: {x}')

    return f'<h1>VISUALIZANDO CACHE</h1>'


@tienda_bp.route('/crear-cotizacion', methods=['POST'])
def crear_cotizacion():
    data = request.get_json()
    usuario_id = int(data["usuario_id"])
    if 'carro_temporal' in session:
        carro = session['carro_temporal']
        productos = carro['productos']
        if not productos:
            return 'error'
        dato = {
            "usuario_id": usuario_id,
            "productos": productos
        }
        respuesta = ModeloCotizacion.registrar(dato)

        if respuesta['estado']:
            session.pop('carro_temporal', None)

        return respuesta


@tienda_bp.errorhandler(404)
def page_not_found(e):
    print('ERROR 404')
    return render_template('404.html')
