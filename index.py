from flask import Flask, render_template,session,url_for,send_file
from api import api_bp
from auth import auth_bp
from productos import productos_bp


app = Flask(__name__)


app.secret_key = 'holabrocomoestasxd'

app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(productos_bp, url_prefix='/')

@app.route('/')
@app.route('/inicio')
def home():
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




if __name__ == '__main__':
    app.run(debug=True, port=5000 , host='0.0.0.0')

