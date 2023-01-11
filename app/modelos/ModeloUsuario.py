from ..extensiones import obtener_conexion
from .entidades.Usuario import Usuario
from flask import jsonify

class ModeloUsuario():
    @classmethod
    def registrar(self , datos ):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                correo = datos['correo'] 
                rut = datos['rut']

                if (datos['nombre'] is None) or (datos['apellido'] is None) or (datos['rut'] is None) or (datos['correo'] is None) or (datos['contraseña'] is None):
                    return {'estado':False , 'mensaje': 'Todos los campos son obligatorios'}
                # comprobar si ya existe un usuario con el mismo correo o rut
                sql = """
                SELECT usuario_id, nombre ,apellido  ,
                    (CASE WHEN correo = %s and rut = %s THEN 'correo y rut'
                    WHEN correo = %s THEN 'correo' 
                    WHEN rut = %s THEN 'rut'
                    END) as en_uso
                FROM usuario
                WHERE correo = %s or rut = %s
                """
                cursor.execute( sql , (correo,rut,correo,rut,correo,rut))
                usuario = cursor.fetchone()

                if usuario is not None:
                    # si ya existe un usuario con el mismo correo o rut, no insertar los datos del formulario
                    return dict(
                        estado = False,
                        mensaje = f'Ya existe un usuario con el mismo {usuario[3]}.'
                    )

                # si no existe, insertar los datos del formulario en la base de datos
                sql = "INSERT INTO usuario(nombre,apellido,rut,correo,contrasena) VALUES (%s,%s,%s,%s,%s) "
                cursor.execute( sql , (datos['nombre'] ,datos['apellido'] ,datos['rut'] , datos['correo'] , datos['contraseña'] ) )
                miConexion.commit()

                return dict(
                    estado = True,
                    mensaje = f'Usuario registrado {datos["nombre"]}'
                )
                

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def login(self , usuario ):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = "SELECT usuario_id , rut , contrasena , nombre , apellido , correo from usuario WHERE rut = %s "
                cursor.execute( sql , usuario.rut)
                consulta = cursor.fetchone()
                print(consulta)

                if consulta != None:
                    return Usuario(consulta[0],consulta[1] , Usuario.comprobar_contrasena(usuario.contrasena ,consulta[2]), consulta[3],consulta[4],consulta[5] )
                else:
                    return None

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def get_by_id(self , id ):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                print(f'-------- GET BY ID {id}-------')
                sql = "SELECT usuario_id , rut , contrasena , nombre , apellido , correo from usuario WHERE usuario_id = %s"
                cursor.execute( sql , id)
                consulta = cursor.fetchone()
                
                print(consulta)
                print('-------- GET BY END -------')

                if consulta != None:
                    return  Usuario(consulta[0],consulta[1] , None , consulta[3],consulta[4],consulta[5] )
                else:
                    return None

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()
    @classmethod
    def buscar_correo(self, correo):
        miconexion = obtener_conexion()
        try:
            with miconexion.cursor() as cursor:
                print(f'-------- OBTENER CORREO: {correo} -------')
                sql = "SELECT usuario_id , rut , contrasena , nombre , apellido , correo from usuario WHERE correo = %s"
                cursor.execute( sql , correo )
                consulta = cursor.fetchone()
                
                print('usuario: ',consulta)
                print('-------- END -------')
                return consulta

        except Exception as ex:
            raise Exception(ex)
        finally:
            miconexion.close()