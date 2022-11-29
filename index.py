
from flask import Flask, render_template,session,url_for,send_file
from flask_login import LoginManager, login_user, logout_user,  login_required
from cache import cache

from api import api_bp
from auth import auth_bp
from tienda import tienda_bp


from modelos.ModeloUsuario import ModeloUsuario
from modelos.ModeloCategoria import ModeloCategoria

app = Flask(__name__, instance_relative_config=True)
# CACHE

#app.config.from_mapping(config)

cache.init_app(app, config={'CACHE_TYPE': 'redis',
                               'CACHE_REDIS_HOST': 'localhost',
                               'CACHE_REDIS_PORT': '6379',
                               'CACHE_REDIS_URL': 'redis://localhost:6379',
                                "CACHE_OPTIONS": {
                                "socket_connect_timeout": 5,    # connection timeout in seconds
                                "socket_timeout": 3,            # send/recv timeout in seconds
                            }})


# CARGA CONFIGIRACION
app.config.from_object('config') 
# CARGA CONFIGURACION DE INSTANCIA
app.config.from_pyfile('config.py')



app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(tienda_bp, url_prefix='/')

login_manager_app = LoginManager(app)
login_manager_app.login_view = "auth_bp.login"
login_manager_app.session_protection = "strong"

@login_manager_app.user_loader
#@cache.cached(timeout=30)
def load_user(id):
    return ModeloUsuario().get_by_id(id)


@cache.cached(timeout=50 , key_prefix='FUNCION_CATEGORIAS') 
def get_all_categories():
    try:
        categorias = cache.get("CATEGORIAS")
        if categorias == None:
            print('ALMACENANDO categorias en CACHE')
            categorias = ModeloCategoria.rollup_categoria()
            cache.set("CATEGORIAS", categorias) # ALMACENA Y ACTUALIZA LAS CATEGORIAS
            
        return categorias
    except:
        print('error redis')
        return None
        
    
#PROCESADOR DE CONTEXTO
@app.context_processor
def injectar_categorias():
    print('categorias para todas las vistas')
    aux = get_all_categories()
    print(aux)
    return dict(categorias = aux)

@app.route('/')
@app.route('/inicio')
def inicio():
    #LLAMADAS DB get_all_categories()
    return render_template("inicio.html"  )

@app.route('/contacto')
def contacto():
    return render_template("contacto.html" )

@app.route('/servicios')
@cache.cached(timeout=50)
def servicios():
    if 'usuario' in session:
        usuario = session['usuario']
        print(usuario)

    return render_template('servicios.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5001 , host='0.0.0.0')

