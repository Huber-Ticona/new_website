import json
from ..extensiones import obtener_conexion

class ModeloProducto():

    @classmethod
    def obtener_producto_x_nombre(self,nombre_producto):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = "SELECT nombre,categoria,FORMAT(precio, 'Currency'),url_imagen,producto_id,imagen_extra FROM producto WHERE nombre = %s"
                cursor.execute( sql , nombre_producto )
                consulta = cursor.fetchone()
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def obtener_productos_x_categoria(self,categoria_id):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                #print('Tipo categoria_id: ', type(categoria_id))
                sql = """
                select producto_id, nombre , precio , url_imagen , imagen_extra , detalle from producto 
                where JSON_CONTAINS(detalle, '%s' ,'$.categorias') = 1 
                order by precio asc """
                cursor.execute( sql, categoria_id )
                consulta = cursor.fetchall()
                #consulta = list(cursor.fetchall())
                #consulta = [ list(item) for item in consulta ]
                #print(consulta)
                

                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()
    