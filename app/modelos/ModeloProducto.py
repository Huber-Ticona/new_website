import json
from ..extensiones import obtener_conexion, db
from sqlalchemy import func, text
from ..modelos.models import Producto, Categoria, Marca


class ModeloProducto():

    @classmethod
    def obtener_producto_x_nombre(self, nombre_producto):
        '''miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:

                sql = "SELECT nombre,categoria,FORMAT(precio, 'Currency'),url_imagen,producto_id,imagen_extra FROM producto WHERE nombre = %s"
                cursor.execute(sql, nombre_producto)
                consulta = cursor.fetchone()

                print('Producto: ', consulta)
                lista_imagenes = json.loads(consulta[5])
                print(lista_imagenes)
                consulta = [consulta[i] if i !=
                            5 else lista_imagenes for i in range(len(consulta))]
                print('Producto new: ', consulta)
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()'''
        producto = Producto.query.filter_by(nombre=nombre_producto).first()
        print('producto -> ', producto)
        return producto

    @classmethod
    def obtener_productos_x_categoria(self, categoria_id, orden, marcas, precio_min, precio_max):

        print('Buscando productos | Categoria_id: ', categoria_id)
        query = Producto.query.filter(func.json_contains(
            Producto.detalle, str(categoria_id), "$.categorias") == 1)
        if marcas:
            query = query.filter(Producto.marca_id.in_(marcas))

        if precio_min is not None:
            query = query.filter(Producto.precio >= int(precio_min))

        if precio_max is not None:
            query = query.filter(Producto.precio <= int(precio_max))

        if orden == 'precio_asc':
            print('asc')
            query = query.order_by(Producto.precio.asc())
        if orden == 'precio_desc':
            print('desc')
            query = query.order_by(Producto.precio.desc())

        result = query.all()
        print('PRODUCTOS ', result)
        return result

    @classmethod
    def obtener_distintas_marcas_x_categoria(self, categoria_id):
        print(
            f'--- Obteniendo lista de marcas para categoria: {categoria_id} ------- ')
        marcas = db.session.query(Marca).join(
            Producto, Producto.marca_id == Marca.marca_id
        ).filter(
            text("json_contains(Producto.detalle, :categoria, '$.categorias') = 1")
        ).params(categoria=str(categoria_id)).distinct().all()
        print(marcas)
        return marcas
        print(f'--- Obteniendo lista de marcas END ------- ')

    @classmethod
    def todos_los_productos(self):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                print('Buscando todos los productos')
                productos = Producto.query.all()
                return productos

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def buscador_de_productos(self, nombre_producto):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                print('Buscando productos similares a: ', nombre_producto)
                sql = """
                    select producto_id, nombre, precio, url_imagen, imagen_extra, detalle 
                    from producto 
                    where nombre like '%%{}%%' 
                    order by precio asc
                """.format(nombre_producto)
                cursor.execute(sql)
                consulta = cursor.fetchall()
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()
