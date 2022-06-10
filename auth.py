from flask import Blueprint, render_template, session , request, redirect , url_for

from modelos.ModeloUsuario import ModeloUsuario
from modelos.entidades.Usuario import Usuario


auth_bp = Blueprint('auth_bp', __name__ ,static_folder='static', template_folder='templates')

@auth_bp.route('/login' ,methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = request.form['nombre_usuario']
        contra = request.form['contraseña']

        print(usuario)
        usuario = Usuario(usuario,contra)
        usuario_logueado = ModeloUsuario.login(usuario)
        if usuario_logueado != None:
            print('usuario encontrado')
        else:
            print('usuario no encontrado')

        #return redirect(url_for('auth_bp.usuario'))

        #VALIDAR CUENTA EN DB 
        '''miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = "select * from producto"
                cursor.execute( sql )
                consulta = cursor.fetchall()

                print(consulta)
                return render_template('contacto.html')

        finally:
            miConexion.close()'''

    
    return render_template('login.html' )
        
@auth_bp.route('/usuario')
def usuario():
    if 'usuario' in session:
        user = session['usuario']
    return f"<p>{user}<p>"

@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return "<p>Sesión cerrada con exito<p>"