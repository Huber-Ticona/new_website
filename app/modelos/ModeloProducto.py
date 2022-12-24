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
                print('Tipo categoria_id: ', type(categoria_id))
                sql = """
                select producto_id, nombre , precio , url_imagen , imagen_extra , detalle from producto 
                where JSON_CONTAINS(detalle, '%s' ,'$.categorias') = 1"""
                cursor.execute( sql, categoria_id )
                consulta = cursor.fetchall()
                #consulta = list(cursor.fetchall())
                #consulta = [ list(item) for item in consulta ]
                print(consulta)
                

                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()
    @classmethod
    def obtener_todos_x_cat_superior(self,id_superior):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = """SELECT producto.nombre,producto.categoria,FORMAT(producto.precio, 'Currency'),producto.url_imagen,producto.producto_id,producto.imagen_extra
                        from (producto inner join categoria on producto.categoria = categoria.categoria_id ) 
                        WHERE JSON_EXTRACT(categoria.detalle, '$.id_superior') = %s """
                cursor.execute( sql ,id_superior)
                consulta = cursor.fetchall()
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def obtener_cat_inferior_superior(self,inferior_id):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                dicc = {}
                sql = "SELECT JSON_EXTRACT(detalle, '$.nombre_categoria'), JSON_EXTRACT(detalle, '$.id_superior') from categoria where categoria_id = %s"
                cursor.execute( sql ,inferior_id)
                respuesta = cursor.fetchone()
                respuesta = [item.replace('"','') for item in respuesta]
                dicc['inferior'] = respuesta[0]

                sql = "SELECT JSON_EXTRACT(detalle, '$.nombre_categoria'), JSON_EXTRACT(detalle, '$.id_superior') from categoria where categoria_id = %s"
                cursor.execute( sql ,respuesta[1])
                respuesta = cursor.fetchone()
                dicc['superior'] = respuesta[0].replace('"','')
                return dicc

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()
