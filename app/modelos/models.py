from ..extensiones import db
from datetime import datetime
from sqlalchemy.orm import relationship


class Categoria(db.Model):
    __tablename__ = 'categoria'
    categoria_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    detalle = db.Column(db.JSON)
    padre_id = db.Column(db.Integer, db.ForeignKey('categoria.categoria_id'))


class Marca(db.Model):
    __tablename__ = 'marca'
    marca_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    detalle = db.Column(db.JSON)


class Producto(db.Model):
    __tablename__ = 'producto'
    producto_id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Integer, nullable=False)

    imagenes = db.Column(db.JSON)
    descuento = db.Column(db.Integer, nullable=True)
    ficha_tecnica = db.Column(db.JSON)
    detalle = db.Column(db.JSON)
    marca_id = db.Column(db.Integer, db.ForeignKey(
        "marca.marca_id", ondelete='CASCADE'))
    marca = relationship(Marca, cascade="all, delete", single_parent=True)


class Usuario(db.Model):
    __tablename__ = 'usuario'
    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    rut = db.Column(db.String(255))
    correo = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255))
    contrasena = db.Column(db.String(255), nullable=True)
    detalle = db.Column(db.JSON)


class Cotizacion(db.Model):
    __tablename__ = "cotizacion"
    cotizacion_id = db.Column(db.Integer, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    monto_total = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.usuario_id"))


class Cotizacion_Producto(db.Model):
    __tablename__ = "cotizacion_producto"
    cotizacion_id = db.Column(db.Integer, db.ForeignKey(
        "cotizacion.cotizacion_id"), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey(
        "producto.producto_id"), primary_key=True)
    cantidad = db.Column(db.Float)