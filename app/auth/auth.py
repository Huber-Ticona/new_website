from flask import Blueprint, render_template, session , request, redirect , url_for ,flash
from flask_login import login_required, login_user, logout_user
from html import escape
from ..modelos.ModeloUsuario import ModeloUsuario
from ..modelos.entidades.Usuario import Usuario
from ..forms import Registrar_Cuenta_Form,Login_Form,Correo_Form

from flask import current_app
from flask_mail import Message
from ..extensiones import mail
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
        # Se valida el captcha
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

@auth_bp.route('/recuperar-contrasena',methods=['GET','POST'])
def recuperar_contraseña():
    print('--------- RECUPERAR PASSWORD ----------')

    form = Correo_Form()

    if request.method == 'POST':
        correo = escape(request.form.get('correo'))

        # VALIDAMOS QUE EXISTA EL USUARIO CON EL CORREO.
        if form.recaptcha.validate(form):
            print('recapcha VERIFICADO')

            if(ModeloUsuario.buscar_correo(correo)):
                msg = Message("Recupera tu contraseña",
                    sender = current_app.config['MAIL_USERNAME'],
                    recipients = [correo])

                print('url: ',url_for('auth_bp.resetear_contraseña'))
                msg.body = f'''Para resetear tu contraseña, visita el siguiente enlace --> http://127.0.0.1:5001/resetear-contrasena
                Si no has solicitado un cambio de contraseña, simplemente ignore este correo.
                '''
                msg.html = f'''Para resetear tu contraseña, visita el siguiente enlace: <a href="http://127.0.0.1:5001/resetear-contrasena"> Enlace </a>
                Si no has solicitado un cambio de contraseña, simplemente ignore este correo.
                '''

                assert msg.sender == current_app.config['MAIL_USERNAME']
                mail.send(msg)     
                flash(f'Hemos enviado un link de recuperacion de contraseña al email: {correo}')
                #redirect(url_for('auth_bp.recuperar_contraseña'))
            else:
                print('Correo no detectado en la base de datos.')    
                flash('El correo no tiene una cuenta registrada.') 
        else:
            print('recapcha NO VERIFICADO')
            flash('Comprueba que eres humano')
        

    return render_template('auth/recuperar_contraseña.html' ,form = form)

@auth_bp.route('/resetear-contrasena',methods=['GET','POST'])
def resetear_contraseña():
    print('--------- RESETEAR PASSWORD ----------')

    form = Correo_Form()

    if request.method == 'POST':
        print('RESETEANDO CONTRASEÑA...')
    
    return render_template('auth/resetear_contraseña.html')


'''def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = fPara resetear tu contraseña, visita el siguiente enlace:
{url_for('reset_password', token=token, _external=True)}
Si no has solicitado un cambio de contraseña, simplemente ignore este correo.

    mail.send(msg)'''
