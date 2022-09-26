from flask import Flask, render_template,session,url_for,send_file
from api import api_bp
from auth import auth_bp
from tienda import tienda_bp
from flask_login import LoginManager, login_user, logout_user,  login_required
from modelos.ModeloUsuario import ModeloUsuario

app = Flask(__name__)


app.secret_key = 'holabrocomoestasxd'

app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(tienda_bp, url_prefix='/')

login_manager_app = LoginManager(app)
login_manager_app.login_view = "auth_bp.login"
login_manager_app.session_protection = "strong"

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario().get_by_id(id)



@app.route('/')
@app.route('/inicio')
def inicio():
    return render_template("inicio.html")

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/servicios')
def servicios():
    if 'usuario' in session:
        usuario = session['usuario']
        print(usuario)
    return render_template('servicios.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001 , host='0.0.0.0')

