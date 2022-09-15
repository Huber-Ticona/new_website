from database import obtener_conexion

class ModeloCategoria():

    @classmethod
    def obtener_superior_id(self,superior):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                print('... buscando categoria superior: ',superior)
                sql = "SELECT * from categoria WHERE JSON_EXTRACT(detalle, '$.tipo_categoria') = 'superior' and JSON_EXTRACT(detalle, '$.nombre_categoria') = %s "
                cursor.execute( sql , superior )
                consulta = cursor.fetchone()
                #print(f'Categoria:  ')
                print('Categoria_ID: ', consulta)
                if consulta != None:
                    return consulta[0] # solo categoria_id
                else:
                    return consulta  #retorna None

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def obtener_inferiores(self,superior_id ):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = """SELECT JSON_EXTRACT(categoria.detalle, '$.nombre_categoria'), count(producto.categoria)
                        from (producto inner join categoria on producto.categoria = categoria.categoria_id ) 
                        WHERE JSON_EXTRACT(categoria.detalle, '$.id_superior') = %s
                        group by producto.categoria """

                cursor.execute( sql , superior_id )

                consulta = cursor.fetchall()
                if consulta != None:
                    consulta = [[(consulta[i][0]).replace('"',''),consulta[i][1]] for i in range(len(consulta))]
                
                print('Categoria_ID: ', consulta)
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod
    def obtener_categoria_id(self,nombre_categoria):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = "SELECT * from categoria WHERE JSON_EXTRACT(detalle, '$.nombre_categoria') = %s"
                cursor.execute( sql , nombre_categoria )
                consulta = cursor.fetchone()
                print(f'Categoria: {nombre_categoria} ')
                print('Categoria_ID: ', consulta)
                if consulta != None:
                    return consulta[0] # solo categoria_id
                else:
                    return consulta  #retorna None

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()