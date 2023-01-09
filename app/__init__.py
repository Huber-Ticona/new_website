from flask import Flask, render_template,session,url_for,send_file
import os 
from config import Config
from .extensiones import cache, login_manager
# Social Flask Dance
from flask_dance.contrib.facebook  import make_facebook_blueprint


def create_app(config_class= Config):
    
    app = Flask(__name__)
    # CACHE

    #app.config.from_mapping(config)


    # INICIALIZAMOS LAS EXTENSIONES 
    cache.init_app(app, config ={
        "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
        "CACHE_DEFAULT_TIMEOUT": 300

    })


    # CARGA CONFIGIRACION
    app.config.from_object(config_class)
    UPLOAD_FOLDER = os.path.abspath('../Productos')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc0S9ojAAAAAMQGIqpU6I8XL3yac7HpZrE5zMI6'
    app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc0S9ojAAAAAEKcEdlXwoP3g-1rEGsvaSHdDiwW'
    # CARGA CONFIGURACION DE INSTANCIA
    #app.config.from_pyfile('config.py')

    from .api import api_bp
    from .auth.auth import auth_bp
    from .tienda.tienda import tienda_bp
    from .main import main_bp



    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(tienda_bp, url_prefix='/store')

    # Social Flask Dance
    facebook_blueprint = make_facebook_blueprint(scope="email" , redirect_to="auth_bp.login_facebook")
    #app.register_blueprint(facebook_blueprint)
    
    from .modelos.ModeloUsuario import ModeloUsuario
    from .modelos.ModeloCategoria import ModeloCategoria

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    login_manager.session_protection = "strong" 

    @login_manager.user_loader
    def load_user(id):
        return ModeloUsuario().get_by_id(id)


    @cache.cached(timeout= 360 , key_prefix='FUNCION_OBT_ROLLUP_CATEGORIAS') 
    def get_all_categories():
        categorias = ModeloCategoria.rollup_categoria()
        return categorias

    @cache.cached(timeout= 360 , key_prefix='FUNCION_OBT_RUTAS_CATEGORIAS') 
    def get_all_rutas():
        rutas = ModeloCategoria.obt_rutas()
        return rutas
            
        
    #PROCESADOR DE CONTEXTO
    @app.context_processor
    def injectar_categorias():
        categorias = get_all_categories()
        rutas = get_all_rutas()
        return dict(categorias = categorias , rutas = rutas)

    
    return app