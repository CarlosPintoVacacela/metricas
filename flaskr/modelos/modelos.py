from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from marshmallow.fields import Nested
import enum
from sqlalchemy.schema import UniqueConstraint

db = SQLAlchemy()


clientes_productos = db.Table('cliente_producto',
    db.Column('cliente_id', db.Integer, db.ForeignKey('cliente.id'), primary_key = True),
    db.Column('item_compra_id', db.Integer, db.ForeignKey('item_compra.id'), primary_key = True))


class Usuario(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(13))
    nombre = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(500))
    fecha_creacion = db.Column(db.DateTime, nullable = False)
    fecha_actualizacion = db.Column(db.DateTime, nullable = False)
    compras = db.relationship('Compra', cascade='all, delete, delete-orphan')
    productos = db.relationship('ItemCompra', secondary = 'cliente_producto')


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_compra= db.Column(db.DateTime, nullable = False)
    fecha_creacion = db.Column(db.DateTime, nullable = False)
    fecha_actualizacion = db.Column(db.DateTime, nullable = False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    cliente = db.relationship("Cliente", back_populates="compras")
    items = db.relationship('ItemCompra', cascade='all, delete, delete-orphan')

class ItemCompra(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    unidades = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))
    producto = db.relationship("Producto")
    compra_id = db.Column(db.Integer, db.ForeignKey("compra.id"))
    compra = db.relationship("Compra", back_populates="items")

class Tipoproducto(enum.Enum):
    CAMISETA = 1
    CHOMPA = 2
    BUSO = 3

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificador = db.Column(db.String(13))
    nombre = db.Column(db.String(120)) 
    tipoproducto = db.Column(db.Enum(Tipoproducto)) 
    precio = db.Column(db.Float()) 
    fecha_creacion = db.Column(db.DateTime, nullable = False)
    fecha_actualizacion = db.Column(db.DateTime, nullable = False)

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unidades = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))
    producto = db.relationship("Producto")
    fecha_actualizacion = db.Column(db.DateTime, nullable = False)
    
    

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Cliente
         include_relationships = True
         load_instance = True

class ProductoSchema(SQLAlchemyAutoSchema):
    tipoproducto = EnumADiccionario(attribute=("tipoproducto"))
    class Meta:
         model = Producto
         include_relationships = True
         load_instance = True

class ItemSchema(SQLAlchemyAutoSchema):
    producto = Nested(ProductoSchema)
    class Meta:
         model = ItemCompra
         include_relationships = True
         load_instance = True

class InventarioSchema(SQLAlchemyAutoSchema):
    producto = Nested(ProductoSchema)
    class Meta:
         model = Inventario
         include_relationships = True
         load_instance = True

class CompraDetalleSchema(SQLAlchemyAutoSchema):
    cliente = Nested(ClienteSchema)
    items = fields.List(fields.Nested(lambda: ItemSchema()))
    class Meta:
         model = Compra
         include_relationships = True
         load_instance = True

class CompraSchema(SQLAlchemyAutoSchema):
    cliente = Nested(ClienteSchema)
    items = fields.List(fields.Nested(lambda: ItemSchema()))
    class Meta:
         model = Compra
         include_relationships = True
         load_instance = True

class CompraSimpleSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Compra
         include_relationships = True
         load_instance = True


class ClienteDetalleSchema(SQLAlchemyAutoSchema):
    productos =  fields.List(fields.Nested(lambda: ItemSchema()))
    class Meta:
         model = Cliente
         include_relationships = True
         load_instance = True

class ProductoDetalleSchema(SQLAlchemyAutoSchema):
    tipoproducto = EnumADiccionario(attribute=("tipoproducto"))
    class Meta:
         model = Producto
         include_relationships = True
         load_instance = True








class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True