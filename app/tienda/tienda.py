
from flask import Blueprint, abort, jsonify, render_template, send_file, request,session,url_for
from html import escape

from ..modelos.ModeloProducto import ModeloProducto
from ..modelos.ModeloCategoria import ModeloCategoria

tienda_bp = Blueprint('tienda_bp', __name__, static_folder='static', template_folder='templates')


@tienda_bp.route('<string:enombre1>')
@tienda_bp.route('<string:enombre1>/<string:enombre2>')
@tienda_bp.route('<string:enombre1>/<string:enombre2>/<string:enombre3>')
#@tienda_bp.route('/categoria/<string:categoria_superior>/<string:categoria_inferior>')
def tienda_productos(enombre1 = None,enombre2 = None,enombre3 = None):
    miga_pan = [] # [nivel 1 , nivel 2 , nivel 3 ] 
    x = [] # LISTA PRODUCTOS A MOSTRAR 
    y = [] # LISTA DE SUBCATEGORIAS A MOSTRAR
    dicc = {} 
    if enombre1 != None and enombre2 != None and enombre3 != None:
        dnombre1 = escape(enombre1.replace('-',' '))
        dnombre2 = escape(enombre2.replace('-',' '))
        dnombre3 = escape(enombre3.replace('-',' '))
        print(f'nombre1: {dnombre1} | nombre2: {dnombre2} | nombre3: {dnombre3}')
        categoria1 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(nombre= dnombre1 , padre_id = 1 )
        if categoria1 == None:
            print('categoria lvl 1 incorrecta --> abortando busqueda')
            abort(404)

        categoria2 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(nombre= dnombre2 , padre_id= categoria1[0] )
        if categoria2 == None:
            print('categoria lvl 2 incorrecta --> abortando busqueda')
            abort(404)
        categoria3 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(nombre= dnombre3 , padre_id= categoria2[0] )
        x = ModeloProducto.obtener_productos_x_categoria(categoria3[0])    
        miga_pan = [enombre1 , enombre2, enombre3 ]


    elif enombre1 != None and enombre2 != None:
        dnombre1 , dnombre2= escape(enombre1.replace('-',' ')) , escape(enombre2.replace('-',' '))
        
        print(f'nombre1: {dnombre1} | nombre2: {dnombre2}')
        categoria1 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(nombre= dnombre1 , padre_id = 1 )
        if categoria1 == None:
            print('categoria lvl 1 incorrecta --> abortando busqueda')
            abort(404)

        categoria2 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(nombre= dnombre2 , padre_id= categoria1[0] )
        if categoria2 == None:
            print('categoria lvl 2 incorrecta --> abortando busqueda')
            abort(404)

        print('Categoria lvl 1 y 2 correcta ---> Obteniendo Productos y subcategorias')
        x = ModeloProducto.obtener_productos_x_categoria(categoria2[0])      
        y = ModeloCategoria.obtener_categorias_hijas_x_padre(categoria2[0])
        miga_pan = [enombre1 , enombre2 ]


    elif enombre1 != None:
        dnombre1 = escape(enombre1.replace('-',' '))
        print(f'nombre1: {dnombre1}')

        categoria1 = ModeloCategoria.obtener_categoria_x_nombre_y_padre(nombre=dnombre1 , padre_id = 1 )
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
    
    
    return render_template('tienda/tienda.html' , dicc = dicc  )


@tienda_bp.route('/producto/<string:nombre>' , methods=['GET'])
def vista_producto(nombre = None):
    if nombre!= None:
        print('-'*5  + f'PRODUCTO {nombre} '  + '-'*5)
        print('-'*5  + f'PRODUCTO escape {escape(nombre)} '  + '-'*5)
        consulta = ModeloProducto.obtener_producto_x_nombre(nombre)

        print(consulta)
        if consulta == None:
            abort(404)
        return render_template('tienda/producto.html'  , producto = consulta  )
        

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

    return render_template('tienda/carro.html', carro = carro)
   
@tienda_bp.errorhandler(404)
def page_not_found(e):
    print('ERROR 404')
    return render_template('404.html')