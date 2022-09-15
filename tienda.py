
import json
from flask import Blueprint, abort, jsonify, render_template, send_file, request,session
from markupsafe import escape
from database import obtener_conexion
from modelos.ModeloProducto import ModeloProducto
from modelos.ModeloCategoria import ModeloCategoria


tienda_bp = Blueprint('tienda_bp', __name__, static_folder='static', template_folder='templates')

@tienda_bp.route('/categoria')
@tienda_bp.route('/categoria/<string:categoria_superior>')
@tienda_bp.route('/categoria/<string:categoria_superior>/<string:categoria_inferior>')
def tienda_productos(categoria_superior = None, categoria_inferior= None):
    productos = []
    dicc = {}

    if categoria_superior != None and categoria_inferior != None:
    # MOSTRAR PRODUCTOS ASOCIADOS A CATEGORIA INFERIOR.
        print('------ SOLO CATEGORIA SUPERIOR E INFERIOR --------')
        print(f'Mostrar todos los productos de: {categoria_superior} con {categoria_inferior}')
        dicc['superior'] = categoria_superior.upper()
        dicc['inferior'] = categoria_inferior.upper()

        superior_id = ModeloCategoria.obtener_superior_id(categoria_superior)
        if superior_id != None:
            lista_inferiores = ModeloCategoria.obtener_inferiores(superior_id)
            dicc['categorias_inferiores'] = lista_inferiores
        print('-'*5)
        categoria_id = ModeloCategoria.obtener_categoria_id(categoria_inferior)
        if categoria_id != None: #SI EXISTE LA CATEGORIA
            productos = ModeloProducto.obtener_productos_x_categoria(categoria_id)
            print('todos los productos')
            print(productos)
            dicc['productos'] = productos

        print('-'*10)

    elif categoria_superior != None:
        print('------ SOLO CATEGORIA SUPERIOR --------')
        print('Categoria superior: ', categoria_superior)
        
        dicc['superior'] = categoria_superior.upper()
        
        superior_id = ModeloCategoria.obtener_superior_id(categoria_superior)
        if superior_id != None:
            lista_inferiores = ModeloCategoria.obtener_inferiores(superior_id)
            dicc['categorias_inferiores'] = lista_inferiores
            productos = ModeloProducto.obtener_todos_x_cat_superior(superior_id)
            print('todos los productos de ', superior_id)
            print(productos)
            dicc['productos'] = productos 
        print('-'*10)

    else:
        abort(404, description="Resource not found")
        #retornar todos los productos o los mas vendidos ,etc...
    
    return render_template('tienda.html' , dicc = dicc )


@tienda_bp.route('/producto/<string:nombre>' , methods=['GET'])
def vista_producto(nombre = None):
    print('-'*5  + f'PRODUCTO {nombre} '  + '-'*5)
    dicc = {} 
    consulta = ModeloProducto.obtener_producto_x_nombre(nombre)
    print(consulta)
    id = consulta[1]
    dicc = ModeloProducto.obtener_cat_inferior_superior(id)
    print(dicc)
    print('vista PRODUCTO v2')
    print(consulta)
    return render_template('producto.html'  , productos = consulta , dicc = dicc)
        

@tienda_bp.route('/agregar_al_carro' , methods=['POST'])
def agregar_al_carro():
    
    if request.method == 'POST':
        print('------ AGREGANDO AL CARRO ---------')
        dato = request.json
        print(dato)
        mensaje = ''
        if 'carro_temporal' in session:
            print('existe el carro temporal')
            carro = session['carro_temporal']
            print('Carro antes: ',carro)
            #analizar mismo producto
            lista_id = [ x[0] for x in carro]
            print(lista_id)
            
            if dato['producto_id'] in lista_id:
                print('existe el item en el carro, aumentando cantidades ...')
                index = lista_id.index(dato['producto_id'])
                print('prodcto en la posicion ' , index)
                carro[index][3] = carro[index][3]  + dato['cantidad']
                mensaje = 'Producto actualizado'
                
            else:
                print('NO existe el item en el carro')
                carro.append([ dato['producto_id'] , dato['url_imagen'],dato['nombre_producto'], dato['cantidad'] ])
                mensaje = 'Producto agregado'

            
            session['carro_temporal'] = carro
            print('Carro despues: ' ,carro)
            print('producto agregado al carro, carro actualizado')

        else:
            print('no existe el carro temporal, creando carro ...')
            carro = []
            mensaje = 'Producto agregado al carro'
            carro.append([ dato['producto_id'] , dato['url_imagen'],dato['nombre_producto'], dato['cantidad'] ])
            session['carro_temporal'] = carro
            print('producto agregado al carro, carro creado')
        print('-'*10)
        return jsonify(mensaje = mensaje , producto = dato )

@tienda_bp.route('/ver_carro' , methods=['POST'])
def ver_carro():
    carro = []
    if request.method == 'POST':
        
        if 'carro_temporal' in session:
            carro = session['carro_temporal']
            print(carro)
            print('enviando')

    return jsonify( productos = carro )
    
@tienda_bp.route('/vaciar-carro' , methods = ['POST'])
def vaciar_carro():

    if 'carro_temporal' in session:
        session.pop('carro_temporal', None)
        session.pop('categoria_superior', None)
        session.pop('categoria_inferior', None)

    return jsonify(mensaje = 'Carrito de compras vaciado.' )

@tienda_bp.route('/mi-carro')
def mi_carro():
    carro = []
    if 'carro_temporal' in session:
        carro = session['carro_temporal']

    return render_template('carro.html', carro = carro)
   
