from flask import Flask
from .extensiones import cache, login_manager, mail

# Social Flask Dance
from flask_dance.contrib.facebook  import make_facebook_blueprint


def create_app():
    
    app = Flask(__name__, instance_relative_config=True)

    # CARGA INSTANCIA CONFIGURACION
    if app.config['ENV'] == 'development':
        app.config.from_object('instance.config.ConfigDevelop')
    else:
        app.config.from_object('instance.config.ConfigProduction')
        
    # CARGA CONFIGURACION DE INSTANCIA
    #app.config.from_pyfile('config.py')

    # INICIALIZAMOS LAS EXTENSIONES 
    cache.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from .api import api_bp
    from .auth.auth import auth_bp
    from .tienda.tienda import tienda_bp
    from .main import main_bp


    #Registramos Blueprints
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(tienda_bp, url_prefix='/store')

    # Social Flask Dance
    facebook_blueprint = make_facebook_blueprint(scope="email" , redirect_to="auth_bp.login_facebook")
    #app.register_blueprint(facebook_blueprint)
    
    from .modelos.ModeloUsuario import ModeloUsuario
    from .modelos.ModeloCategoria import ModeloCategoria

    
    login_manager.login_view = "auth_bp.login"
    login_manager.session_protection = "strong" 

    @login_manager.user_loader
    def load_user(id):
        return ModeloUsuario().get_by_id(id)


    @cache.cached(timeout= 10 , key_prefix='FUNCION_OBT_ROLLUP_CATEGORIAS') 
    def get_all_categories():
        categorias = ModeloCategoria.rollup_categoria()
        return categorias

    @cache.cached(timeout= 15 , key_prefix='FUNCION_OBT_RUTAS_CATEGORIAS') 
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