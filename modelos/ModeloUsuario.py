from database import obtener_conexion

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
                

        finally:
            miConexion.close()