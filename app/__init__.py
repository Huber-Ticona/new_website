from flask import Flask, render_template,session,url_for,send_file

from config import Config
from .extensiones import cache, login_manager



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

    # CARGA CONFIGURACION DE INSTANCIA
    #app.config.from_pyfile('config.py')

    from .api import api_bp
    from .auth.auth import auth_bp
    from .tienda.tienda import tienda_bp
    from .main import main_bp


    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(tienda_bp, url_prefix='/')
    
    from .modelos.ModeloUsuario import ModeloUsuario
    from .modelos.ModeloCategoria import ModeloCategoria

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    login_manager.session_protection = "strong" 

    @login_manager.user_loader
    def load_user(id):
        return ModeloUsuario().get_by_id(id)


    @cache.cached(timeout=20 , key_prefix='FUNCION_CATEGORIAS') 
    def get_all_categories():
        categorias = ModeloCategoria.rollup_categoria()
        return categorias
    
            
        
    #PROCESADOR DE CONTEXTO
    @app.context_processor
    def injectar_categorias():
        aux = get_all_categories()
        return dict(categorias = aux)

    
    return app