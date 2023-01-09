from flask import Blueprint, render_template, session , request, redirect , url_for ,flash
from flask_login import login_required, login_user, logout_user
from html import escape
from ..modelos.ModeloUsuario import ModeloUsuario
from ..modelos.entidades.Usuario import Usuario
from ..forms import Registrar_Cuenta_Form,Login_Form
from flask_wtf.recaptcha import  Recaptcha

from flask_dance.contrib.facebook import facebook

auth_bp = Blueprint('auth_bp', __name__ ,static_folder='static', template_folder='templates')

@auth_bp.route('/login' ,methods = ['GET', 'POST'])
def login():
    print('-'*10)
    formulario = Login_Form()

    if request.method == 'POST':
        rut = escape(request.form.get('rut'))
        contraseña = escape(request.form.get('contraseña'))
        print(f'----- POST | rut: {rut} | contraseña: {contraseña} --------')
        #Se crea un objeto Usuario el cual tendra los datos enviados del usuario.
        usuario = Usuario(0,rut,contraseña,None,None,None)
        #Se obtiene el usuario de la base de datos si es que existe.
        usuario_logueado = ModeloUsuario.login(usuario)

        if usuario_logueado != None:
            print('usuario encontrado')
            if usuario_logueado.contrasena:
                login_user(usuario_logueado)
                return redirect(url_for('main_bp.inicio'))

            else:
                print('CONTRASEÑA INCORRECTA')
        else:
            print('USUARIO NO ENCONTRADO')

        flash('USUARIO O CONTRASEÑA INCORRECTAS')
    
    return render_template('auth/login.html', form = formulario)

@auth_bp.route('/crear-cuenta' ,methods = ['GET', 'POST'])
def crear_cuenta():
    formulario = Registrar_Cuenta_Form()
    if request.method == 'POST':
        datos = {
        'nombre' : escape(request.form.get('nombre')),
        'apellido' : escape(request.form.get('apellido')),
        'rut' : escape(request.form.get('rut')),
        'correo' : escape(request.form.get('correo')),
        'contraseña' : escape(request.form.get('contraseña'))
        }
        if formulario.recaptcha.validate(formulario):
            print('captcha valido')
            #respuesta = { "estado":True , "mensaje":"testeando captacha"}
            respuesta = ModeloUsuario.registrar(datos)
            if respuesta['estado'] == False:
                flash(respuesta['mensaje'] , 'error')
                print(respuesta['mensaje'] )
            else:
                flash(respuesta['mensaje'] , 'success')
                print(respuesta['mensaje'])
                return redirect(url_for('auth_bp.login'))
        else:
            print('captcha invalido')
            flash('captcha invalido', 'success')
        #
        
        #else:
         #   print('captcha no valido')
    return render_template('auth/crear-cuenta.html' , form = formulario)


@auth_bp.route('/login-facebook')
def login_facebook():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    res = facebook.get('/me?fields=name,email')
    print(res.json())

    return "login con facebook"

@auth_bp.route('/cuenta')
@login_required
def cuenta():
    return render_template('auth/cuenta.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.inicio'))