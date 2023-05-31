from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort, jsonify, send_from_directory, send_file
from flask_login import login_required, login_user, logout_user, current_user

from html import escape
from ..modelos.ModeloUsuario import ModeloUsuario
from ..modelos.ModeloCotizacion import ModeloCotizacion
from ..modelos.entidades.Usuario import Usuario

from ..forms import Registrar_Cuenta_Form, Login_Form, Correo_Form

from flask import current_app
from flask_mail import Message
from ..extensiones import mail, generar_pdf, verificar_pdf
from flask_dance.contrib.facebook import facebook

auth_bp = Blueprint('auth_bp', __name__,
                    static_folder='static', template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    formulario = Login_Form()
    if request.method == 'POST':
        correo = escape(request.form.get('correo'))
        contraseña = escape(request.form.get('contraseña'))
        # Se crea un objeto Usuario el cual tendra los datos enviados del usuario.
        usuario = Usuario(0, None, contraseña, None, None, correo)
        # Se obtiene el usuario de la base de datos si es que existe.
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
    return render_template('auth/login.html', form=formulario)


@auth_bp.route('/crear-cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    formulario = Registrar_Cuenta_Form()
    if request.method == 'POST':
        datos = {
            'nombre': escape(request.form.get('nombre')),
            'apellido': escape(request.form.get('apellido')),
            'rut': escape(request.form.get('rut')),
            'correo': escape(request.form.get('correo')),
            'contraseña': escape(request.form.get('contraseña'))
        }
        # Se valida el captcha
        if formulario.recaptcha.validate(formulario):
            respuesta = ModeloUsuario.registrar(datos)
            if respuesta['estado'] == False:
                flash(respuesta['mensaje'], 'error')
            else:
                flash(respuesta['mensaje'], 'success')
                return redirect(url_for('auth_bp.login'))
        else:
            flash('captcha invalido', 'success')
    return render_template('auth/crear-cuenta.html', form=formulario)


@auth_bp.route('/login-facebook')
def login_facebook():

    if not facebook.authorized:
        return redirect(url_for('facebook.login'))

    res = facebook.get('/me?fields=first_name,last_name,email')
    datos_api = res.json()
    data = {
        "nombre": datos_api['first_name'],
        "apellido": datos_api['last_name'],
        "correo": datos_api['email']
    }
    respuesta = ModeloUsuario.registrar_con_red_social(data)
    login_user(respuesta['usuario'])

    return redirect(url_for('main_bp.inicio'))


@auth_bp.route('/cuenta')
@login_required
def cuenta():
    return render_template('auth/cuenta.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.inicio'))


@auth_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contraseña():
    print('--------- RECUPERAR PASSWORD ----------')

    form = Correo_Form()

    if request.method == 'POST':
        correo = escape(request.form.get('correo'))

        # VALIDAMOS QUE EXISTA EL USUARIO CON EL CORREO.
        if form.recaptcha.validate(form):
            print('recapcha VERIFICADO')

            if (ModeloUsuario.buscar_correo(correo)):
                msg = Message("Recupera tu contraseña",
                              sender=current_app.config['MAIL_USERNAME'],
                              recipients=[correo])

                print('url: ', url_for('auth_bp.resetear_contraseña'))
                url = 'http://127.0.0.1:5001/resetear-contrasena'
                if current_app.config['FLASK_ENV'] == 'production':
                    url = 'https://madenco.site/resetear-contrasena'

                msg.body = f'''Para resetear tu contraseña, visita el siguiente enlace --> {url}
                Si no has solicitado un cambio de contraseña, simplemente ignore este correo.
                '''
                msg.html = f'''Para resetear tu contraseña, visita el siguiente enlace: <a href="{url}"> Enlace </a>
                Si no has solicitado un cambio de contraseña, simplemente ignore este correo.
                '''

                assert msg.sender == current_app.config['MAIL_USERNAME']
                mail.send(msg)
                flash(
                    f'[Madenco] Hemos enviado un link de recuperacion de contraseña al email: {correo}')
                # redirect(url_for('auth_bp.recuperar_contraseña'))
            else:
                print('Correo no detectado en la base de datos.')
                flash('El correo no tiene una cuenta registrada.')
        else:
            print('recapcha NO VERIFICADO')
            flash('Comprueba que eres humano')

    return render_template('auth/recuperar_contraseña.html', form=form)


@auth_bp.route('/resetear-contrasena', methods=['GET', 'POST'])
def resetear_contraseña():
    print('--------- RESETEAR PASSWORD ----------')

    form = Correo_Form()

    if request.method == 'POST':
        print('RESETEANDO CONTRASEÑA...')

    return render_template('auth/resetear_contraseña.html')


@auth_bp.route('/cuenta/mi-perfil', methods=['POST'])
@login_required
def mi_perfil():
    if request.method == 'POST':
        return render_template('auth/mi_perfil.html')


@auth_bp.route('/cuenta/mis-cotizaciones', methods=['POST'])
@login_required
def mis_cotizaciones():
    if request.method == 'POST':
        usuario_id = current_user.id
        print(f'Cotizaciones de {usuario_id}')
        cotizaciones = ModeloCotizacion.obtener_cotizacion_x_usuario(
            usuario_id)
        return render_template('auth/mis_cotizaciones.html', cotizaciones=cotizaciones)


@auth_bp.route('/cuenta/mis-cotizaciones/ver/<int:cotizacion_id>')
@login_required
def ver_cotizacion(cotizacion_id=None):

    detalle_cotizacion = ModeloCotizacion.obtener_cotizacion_x_id(
        cotizacion_id, current_user.id)
    print(detalle_cotizacion)
    if detalle_cotizacion['estado'] == False:
        print(detalle_cotizacion['mensaje'])
        abort(detalle_cotizacion['error'])

    # Verifica si existe el PDF en el servidor.
    pdf_url = verificar_pdf(cotizacion_id)
    if pdf_url == None:
        # Se genera el PDF.
        pdf_url = generar_pdf(detalle_cotizacion)

    # Se envia el PDF al cliente
    return send_from_directory(current_app.config['COTIZACION_FOLDER'], f'cotizacion_{cotizacion_id}.pdf')


@auth_bp.route('/cuenta/mis-cotizaciones/eliminar/<int:cotizacion_id>')
@login_required
def eliminar_cotizacion(cotizacion_id=None):
    x = 0
    print(
        f'--Eliminando cotizacion nro {cotizacion_id } de usuario id: { current_user.id } -------')


'''def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = fPara resetear tu contraseña, visita el siguiente enlace:
{url_for('reset_password', token=token, _external=True)}
Si no has solicitado un cambio de contraseña, simplemente ignore este correo.

    mail.send(msg)'''
