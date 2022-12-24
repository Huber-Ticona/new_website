from flask import Blueprint, render_template, session,jsonify

main_bp = Blueprint('main_bp', __name__, static_folder='static', template_folder='templates')

@main_bp.route('/')
@main_bp.route('/inicio')
def inicio():
    #LLAMADAS DB get_all_categories()
    return render_template("inicio.html"  )

@main_bp.route('/contacto')
#@cache.cached(timeout=50)
def contacto():
    return render_template("contacto.html" )

@main_bp.route('/servicios')
def servicios():
    if 'usuario' in session:
        usuario = session['usuario']
        print(usuario)
    return render_template('servicios.html')




@main_bp.route('/test')
def test():
    return 'testing ... '