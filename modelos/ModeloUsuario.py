from database import obtener_conexion
from modelos.entidades.Usuario import Usuario

class ModeloUsuario():
    @classmethod
    def login(self , usuario ):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = "SELECT usuario_id,usuario,contrasena,nombre,apellido from usuario WHERE usuario = binary %s"
                cursor.execute( sql , usuario.usuario)
                consulta = cursor.fetchone()
                print(consulta)
                #devolver lista de categorias padres
                if consulta != None:
                    usuario = Usuario(consulta[0],consulta[1] , Usuario.comprobar_contrasena(usuario.contrasena , consulta[2] ) )
                    return usuario 
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
        
                sql = "SELECT usuario_id,usuario,contrasena,nombre,apellido from usuario WHERE usuario_id =  %s"
                cursor.execute( sql , id)
                consulta = cursor.fetchone()
                print('GET BY ID')
                print(consulta)
                #devolver lista de categorias padres
                if consulta != None:
                    usuario = Usuario(consulta[0], consulta[1], None  )
                    return usuario 
                else:
                    return None

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()