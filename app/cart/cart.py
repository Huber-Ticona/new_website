from flask import Blueprint, session, request, jsonify, render_template
from ..extensiones import cache
from ..modelos.ModeloCotizacion import ModeloCotizacion

cart_bp = Blueprint('cart_bp', __name__,
                    static_folder='static', template_folder='templates')


@cart_bp.route('/agregar_al_carro', methods=['POST'])
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


@cart_bp.route('/ver_carro', methods=['POST'])
def ver_carro():
    carro = []
    if request.method == 'POST':

        if 'carro_temporal' in session:
            carro = session['carro_temporal']
            print(carro)
            print('enviando')

    return render_template('cart/carro_lista.html', carro=carro)
   # return jsonify( productos = carro )


@cart_bp.route('/vaciar-carro', methods=['GET'])
def vaciar_carro():

    if 'carro_temporal' in session:
        session.pop('carro_temporal', None)

    return jsonify(mensaje='Carrito de compras vaciado.')


@cart_bp.route('/mi-carro')
def mi_carro():
    carro = []
    if 'carro_temporal' in session:
        carro = session['carro_temporal']

    return render_template('cart/carro.html', carro=carro)


@cart_bp.route('/keys')
def cache_keys():
    claves = cache.cache._cache.keys()
    print('claves: ', claves)
    for i in claves:
        x = cache.get(i)
        print(f'CLAVE: {i} | VALOR: {x}')

    return f'<h1>VISUALIZANDO CACHE</h1>'


@cart_bp.route('/crear-cotizacion', methods=['POST'])
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
