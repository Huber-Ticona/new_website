from ..extensiones import obtener_conexion

class ModeloCategoria():


    @classmethod # OBSOLETA
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
    
    @classmethod  # USADA EN LA NUEVA VERSION DE TIENDA
    def obtener_categoria_x_nombre_y_padre(self,nombre,padre_id):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = """
                SELECT categoria_id, nombre, nivel ,padre_id from categoria 
                WHERE nombre = %s and padre_id = %s """

                cursor.execute( sql , ( nombre, padre_id ) )
                consulta = cursor.fetchone()
                
                #print('Categoria: ', consulta)
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod  # USADA EN LA NUEVA VERSION DE TIENDA
    def obtener_categorias_hijas_x_padre(self,padre_id):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
        
                sql = """
                SELECT categoria_id, nombre, nivel ,padre_id from categoria 
                WHERE padre_id = %s  """

                cursor.execute( sql , ( padre_id ) )
                consulta = cursor.fetchall()
                
                print('Subcategorias: ', consulta)
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()
    @classmethod # USADA EN LA NUEVA VERSION DE TIENDA
    def rollup_categoria(self):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                print('- OBTENIENDO ROLLUP CATEGORIAS -')
                sql = '''
                with vista as(
                select  c.categoria_id as id ,replace(c.nombre,' ','-') as nombre , b.nombre as padre,b.categoria_id as padre_id , c.nivel
                from categoria c inner join categoria b ON b.categoria_id = c.padre_id

                )

                select distinct(padre),padre_id , nivel ,group_concat(concat(id,';',nombre))
                from vista 
                group by padre
                order by nivel
                '''
                cursor.execute( sql )
                consulta = list(cursor.fetchall())
                #print(consulta)
                #print(type(consulta))
                id = [ item[1] for item in consulta ]
                categoria_padre = [ item[0] for item in consulta ]
                sub_categoria = [ item[3] for item in consulta ]
                nivel = [ item[2] for item in consulta ]

                consulta = [ id, categoria_padre, sub_categoria , nivel ]
                print(consulta)
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()

    @classmethod 
    def obt_rutas(self):
        miConexion = obtener_conexion()
        try:
            with miConexion.cursor() as cursor:
                print('- OBTENIENDO LAS RUTAS DE LAS CATEGORIAS -')
                sql = '''
                WITH RECURSIVE rutas (categoria_id, nombre, nivel, ruta) AS (
                SELECT c.categoria_id, c.nombre, c.nivel, c.nombre
                FROM categoria c
                WHERE c.padre_id IS NULL
                UNION ALL
                SELECT c.categoria_id, c.nombre, c.nivel, CONCAT(r.ruta, '/', c.nombre)
                FROM categoria c
                INNER JOIN rutas r ON c.padre_id = r.categoria_id
                )
                SELECT r.categoria_id, replace(r.ruta,' ','-') as ruta, r.nombre, r.nivel
                FROM rutas r;
                '''

                cursor.execute( sql )
                consulta = list(cursor.fetchall())
                
                id = [ item[0] for item in consulta ]
                ruta = [ item[1] for item in consulta ]
                consulta = [ id, ruta ]
                print(consulta)
                return consulta

        except Exception as ex:
            raise Exception(ex)

        finally:
            miConexion.close()