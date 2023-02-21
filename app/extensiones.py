from flask_caching import Cache
import pymysql
from flask_login import LoginManager
from flask import current_app
from flask_mail import Mail
from datetime import datetime
#reportlab
from reportlab.lib.pagesizes import letter,A4,mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

login_manager = LoginManager()

cache = Cache()

mail = Mail()

def obtener_conexion():
    return pymysql.connect(
        host=current_app.config['HOST'],
        user=current_app.config['USER'],
        password=current_app.config['PASSWORD'], 
        db=current_app.config['DB'])

def verificar_pdf(cotizacion_id):
    x=0
    ruta = current_app.config['COTIZACION_FOLDER'] + "\cotizacion_"+ str(cotizacion_id) +".pdf"
    #ruta = current_app.config['COTIZACION_FOLDER'] + "\logo.png"
    print('Verificando PDF: ' , ruta)

    if os.path.isfile(ruta):
        print('existe pdf')
        return ruta
    else:
        print('no existe pdf')
        return None

def generar_pdf(datos):

    print('----- GENERANDO PDF ------')
    print('RUTA: ' + current_app.config['COTIZACION_FOLDER'])

    # A4 (210 * 297 mm)
    url = current_app.config['COTIZACION_FOLDER'] + "\cotizacion_"+ str(datos['cotizacion_id']) +".pdf"
    c = canvas.Canvas( url , pagesize=A4)

    c.line(0, 296*mm , 200*mm , 296*mm )
    #logo

    imagen = ImageReader(current_app.config['DOCS_FOLDER'] + '\logo2.png' )

    # Dibujar la imagen en la posición (x, y) con un ancho y alto específico
    c.drawImage(imagen, 10*mm , 270*mm,35*mm, 20 *mm)

    c.setFont("Helvetica", 9)

    #fecha
    fecha = datos['fecha_creacion']
    c.drawString(180*mm, 285*mm, str(fecha))

    c.setFont("Helvetica", 6)
    c.drawString(46*mm, 285*mm, "MADERAS ENCO")
    c.drawString(46*mm, 282*mm , "GIRO: BARRACA DE MADERAS")
    c.drawString(46*mm, 279*mm , "RUT: 92.648.000-6")
    c.drawString(46*mm, 276*mm , "Av. Santa María 2483")
    c.drawString(46*mm, 273*mm , "Arica")
    c.drawString(46*mm, 270*mm , "Email: ventas.enco@chilemat.cl")

    #encabezado
    c.setFont("Helvetica", 14)
    c.drawString(80*mm, 750, "Cotización N° ")
    c.drawString(120*mm, 750, str(datos['cotizacion_id']))

    #Datos cotizacion
    c.setFont("Helvetica", 10)
    c.drawString(50, 700, "Cliente:")
    c.drawString(150, 700, datos['cliente'])
    c.drawString(50, 680, "Email:")
    c.drawString(150, 680, datos['correo'])
    c.drawString(50, 660, "Comuna:")
    c.drawString(150, 660, "Arica")
    c.drawString(50, 640, "Ciudad:")
    c.drawString(150, 640, "Arica")

    # Crear una tabla de productos
    tabla_productos = [ ["Codigo", "Descripcion", "U/M", "Cantidad", "Precio", "Total"] ]

    monto_total = 0
    for item in datos['lista_productos']:
        tabla_productos.append( ['xxxx' , item[3] , 'Plancha', item[2] , item[4] , (item[2] * item[4]) ] )
        monto_total = item[5] 

    # Dibujar la tabla en la posición (100, 600)
    x = 50
    y = 600
    # Dibujar línea encabezado de tabla
    c.line(x, y-3, 550, y-3 )
    c.setFont("Helvetica", 9)
    anchos_columnas = [20*mm, 70*mm, 20*mm, 20*mm, 20*mm, 20*mm]
    for fila in tabla_productos:
        for i, celda in enumerate(fila):
            c.drawString(x, y, str(celda))
            x += anchos_columnas[i]
        y -= 20
        x = 50

    

    #FOOTER
    c.setFont("Helvetica", 10)
    x = 50
    y -= 30
    c.drawString(x, y, "Total Neto:")
    c.drawString(x + 100, y, str(monto_total))
    c.drawString(x, y - 20, "IVA:")
    c.drawString(x + 100, y-20, f'{(monto_total*0.19):.2f}' )
    c.drawString(x, y-40, "Total:")
    c.drawString(x + 100, y-40, f'{(monto_total*1.19):.2f}' )

    c.save()
    return url

