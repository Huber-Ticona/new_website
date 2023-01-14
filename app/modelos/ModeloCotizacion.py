from ..extensiones import obtener_conexion
from datetime import datetime
class ModeloCotizacion():

    @classmethod
    def registrar(self, datos):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                x = 0
                fecha_creacion = datetime.now()

                sql = "INSERT INTO cotizacion (fecha_creacion, usuario_id) VALUES (%s, %s)"
                cursor.execute( sql , (fecha_creacion, datos['usuario_id']))
                cotizacion_id = cursor.lastrowid

                monto_total = 0
                # Agregar los productos y actualizar el monto total
                for producto in datos['productos']:
                    producto_id = producto['producto_id']
                    cantidad = producto['cantidad']
                    precio = producto['precio_unitario'].replace(',','')
                    monto_total += int(precio) * cantidad

                    sql2 = "INSERT INTO cotizacion_producto (cotizacion_id, producto_id, cantidad) VALUES (%s, %s, %s)"
                    cursor.execute( sql2, (cotizacion_id, producto_id, cantidad))

                # Actualizar el monto total en la tabla de cotizacion
                cursor.execute("UPDATE cotizacion SET monto_total=%s WHERE cotizacion_id=%s", (monto_total, cotizacion_id))
                miConexion.commit()

                return {
                    "estado" : True,
                    "mensaje" : 'Cotizacion Registrada'
                    }

        except Exception as ex:
            return {
                    "estado" : False,
                    "mensaje" : 'Error al registrar la Cotizacion (ex)'
                    }
        finally:
            miConexion.close()

    @classmethod
    def obtener_cotizacion_x_usuario(self, usuario_id):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                sql = "select cotizacion_id,monto_total,fecha_creacion from cotizacion where usuario_id = %s"
                cursor.execute(sql , usuario_id)
                resultado = cursor.fetchall()
                return resultado

        except Exception as ex:
            raise Exception(ex)
        finally:
            miConexion.close()