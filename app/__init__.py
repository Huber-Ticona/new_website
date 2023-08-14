from flask import Flask
from .config import ConfigDevelop, ConfigProduction
from dotenv import load_dotenv


def create_app():

    load_dotenv()  # Carga las variables de entorno desde el archivo .env
    app = Flask(__name__)

    # CARGA CONFIGURACION
    if app.config['ENV'] == 'development':
        app.config.from_object(ConfigDevelop)
    else:
        app.config.from_object(ConfigProduction)

    # INICIALIZAMOS LAS EXTENSIONES
    from .extensiones import cache, login_manager, mail, db
    cache.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    from .api import api_bp
    from .auth.auth import auth_bp
    from .tienda.tienda import tienda_bp
    from .main import main_bp
    from .cart.cart import cart_bp
    # Registramos Blueprints
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(tienda_bp, url_prefix='/store')
    app.register_blueprint(cart_bp, url_prefix='')

    # Social Flask Dance
    from flask_dance.contrib.facebook import make_facebook_blueprint
    facebook_blueprint = make_facebook_blueprint(
        scope="email", redirect_to='/login-facebook')
    app.register_blueprint(facebook_blueprint)

    from .modelos.ModeloUsuario import ModeloUsuario
    from .modelos.ModeloCategoria import ModeloCategoria

    login_manager.login_view = "auth_bp.login"
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    @cache.cached(timeout=60)
    def load_user(id):
        return ModeloUsuario().get_by_id(id)

    @cache.cached(timeout=600, key_prefix='FUNCION_OBT_ROLLUP_CATEGORIAS')
    def get_all_categories():
        categorias = ModeloCategoria.rollup_categoria()
        return categorias

    @cache.cached(timeout=600, key_prefix='FUNCION_OBT_RUTAS_CATEGORIAS')
    def get_all_rutas():
        rutas = ModeloCategoria.obt_rutas()
        return rutas

    # PROCESADOR DE CONTEXTO: Permite que las variables se puedan ver en todas las rutas.
    @app.context_processor
    def injectar_categorias():
        categorias = get_all_categories()
        rutas = get_all_rutas()
        google_analitics_id = app.config['GOOGLE_ANALYTICS_ID']
        return dict(categorias=categorias, rutas=rutas, google_analitics_id=google_analitics_id)

    return app
