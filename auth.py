from flask import Blueprint, render_template, session , request, redirect , url_for ,flash
from flask_login import login_required, login_user, logout_user

from cache import cache

from modelos.ModeloUsuario import ModeloUsuario
from modelos.entidades.Usuario import Usuario


auth_bp = Blueprint('auth_bp', __name__ ,static_folder='static', template_folder='templates')

@auth_bp.route('/login' ,methods = ['GET', 'POST'])
def login():
    print('-'*10)
    categorias = cache.get("all_categorias")
    print(categorias)
    print('-'*10)
    if request.method == 'POST':
        usuario = request.form['nombre_usuario']
        contra = request.form['contraseña']

        print(usuario)
        usuario = Usuario(0,usuario,contra)
        usuario_logueado = ModeloUsuario.login(usuario)
        if usuario_logueado != None:
            print('usuario encontrado')
            if usuario_logueado.contrasena:
                login_user(usuario_logueado)
                return redirect(url_for('inicio'))

            else:
                flash('invalida contraseña')
                print('contraseña invalida')
            #return render_template('inicio.html' , usuario = usuario.usuario )
        else:
            print('usuario no encontrado')
            return render_template('login.html' )
    
    return render_template('login.html' , categorias= categorias )

 
@auth_bp.route('/cuenta')
@login_required
def cuenta():
    return render_template('cuenta.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('inicio'))