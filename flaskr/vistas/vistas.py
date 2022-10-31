from flask import request

from flaskr.modelos.modelos import ProductoDetalleSchema
from ..modelos import db, Cliente,Compra, ItemCompra,  Producto, ClienteSchema, ProductoSchema, Usuario, UsuarioSchema, ClienteDetalleSchema, CompraSchema, CompraDetalleSchema, ProductoDetalleSchema, ItemSchema, Inventario, InventarioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime


cliente_schema = ClienteSchema()
cliente_detalle_schema = ClienteDetalleSchema()

compra_schema = CompraSchema()
compra_detalle_schema = CompraDetalleSchema()

item_compra_schema = ItemSchema

producto_schema = ProductoSchema()
producto_detalle_schema = ProductoDetalleSchema()

usuario_schema = UsuarioSchema()

inventario_schema = InventarioSchema()


class VistaClientes(Resource):
    @jwt_required()
    def get(self):
        return[cliente_schema.dump(client) for client in Cliente.query.all()]

    @jwt_required()
    def post(self):
        cliente = Cliente.query.filter(Cliente.identificacion == request.json["identificacion"]).first()
        
        if cliente is None:
            nuevo_cliente = Cliente(
                identificacion=request.json["identificacion"], 
                nombre=request.json["nombre"], 
                telefono=request.json["telefono"], 
                email=request.json["email"],
                direccion=request.json["direccion"],
                fecha_creacion = datetime.now(),
                fecha_actualizacion = datetime.now()
                )
            db.session.add(nuevo_cliente)
            db.session.commit()
            return {"mensaje":"Cliente creado exitosamente", "cliente":cliente_schema.dump(nuevo_cliente)}, 200
        else:
            return {"mensaje":"Cliente ya existente", "cliente":cliente_schema.dump(cliente)}, 404

    
class VistaCliente(Resource):
    @jwt_required()
    def get(self, id_cliente):
        return cliente_detalle_schema.dump(Cliente.query.get_or_404(id_cliente))

    @jwt_required()
    def put(self, id_cliente):
        cliente = Cliente.query.get_or_404(id_cliente)
        cliente.identificacion=request.json["identificacion"]
        cliente.nombre=request.json["nombre"]
        cliente.telefono=request.json["telefono"]
        cliente.email=request.json["email"]
        cliente.direccion=request.json["direccion"]
        cliente.fecha_actualizacion = datetime.now()
        db.session.commit()
        return {"mensaje":"Cliente actualizado exitosamente", "cliente":cliente_detalle_schema.dump(cliente)}, 200

    @jwt_required()
    def delete(self, id_cliente):
        cliente = Cliente.query.get_or_404(id_cliente)
        db.session.delete(cliente)
        db.session.commit()
        return {"mensaje":"Cliente eliminado exitosamente"}, 200

class VistaProductos(Resource):
    @jwt_required()
    def get(self):
        return[producto_schema.dump(product) for product in Producto.query.all()]

    @jwt_required()
    def post(self):
        producto = Producto.query.filter(Producto.identificador == request.json["identificador"]).first()
        if producto is None:
            nuevo_producto = Producto(
                identificador=request.json["identificador"], 
                nombre=request.json["nombre"], 
                tipoproducto=request.json["tipoproducto"], 
                precio=request.json["precio"],
                fecha_creacion = datetime.now(),
                fecha_actualizacion = datetime.now()
                )
            db.session.add(nuevo_producto)
            db.session.commit()
            return {"mensaje":"Producto creado exitosamente", "producto":producto_schema.dump(nuevo_producto)}, 200
        else:
            return {"mensaje":"Ya existe un producto con ese identificador", "producto":producto_schema.dump(producto)}, 404

class VistaProducto(Resource):
    @jwt_required()
    def get(self, id_producto):
        print("entra")
        return producto_detalle_schema.dump(Producto.query.get_or_404(id_producto))

    @jwt_required()
    def put(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        producto.identificador=request.json["identificador"]
        producto.nombre=request.json["nombre"]
        producto.tipoproducto=request.json["tipoproducto"]
        producto.precio=request.json["precio"]
        producto.fecha_actualizacion = datetime.now()
        db.session.commit()
        return {"mensaje":"Cliente actualizado exitosamente", "cliente":producto_schema.dump(producto)}, 200

    @jwt_required()
    def delete(self, id_producto):
        prodcuto = Producto.query.get_or_404(id_producto)
        db.session.delete(prodcuto)
        db.session.commit()
        return {"mensaje":"Usuario eliminado exitosamente"}, 200


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return {"mensaje":"Las credenciales no son correctas"}, 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token":token_de_acceso}


class VistaUsuarios(Resource):

    @jwt_required()
    def get(self):
        return[cliente_schema.dump(client) for client in Cliente.query.all()]

    @jwt_required()
    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"]).first()
        if usuario is not None:
             return {"mensaje":'El usuario ya existe!'}, 409
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje":"Usuario creado exitosamente", "usuario":usuario_schema.dump(nuevo_usuario)}, 200

    

class VistaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))

    @jwt_required()
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return {"mensaje":"Usuario actualizado exitosamente", "usuario":usuario_schema.dump(usuario)}, 200

    @jwt_required()
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return {"mensaje":"Usuario eliminado exitosamente"}, 200


class VistaCompras(Resource):

    @jwt_required()
    def get(self):
        return[compra_schema.dump(compra) for compra in Compra.query.all()]

    @jwt_required()
    def post(self):
        cliente = Cliente.query.get(request.json['id_cliente'])
        array = []
        for item in request.json['items']:
            array.append(item["producto"]["id"])
        inventario = Inventario.query.filter(Inventario.producto_id.in_(array) ).all()
        if len(inventario) != len(request.json['items']):
            return {"mensaje":"Algunos productos no han sido agregados al inventario"}, 400

        for item in request.json['items']:
            for invent in inventario:
                if invent.id == item["producto"]["id"]:
                    res = invent
            if res is not None:
                if item["unidades"]>res.unidades:
                    return {"mensaje":"No se disponen de las unidades"}, 400
            else:
                return {"mensaje":"No se encuentra el producto"}, 400

        if cliente is not None:
            format = '%d/%m/%Y'
            nueva_compra = Compra( 
                fecha_compra=datetime.strptime(request.json['fecha_compra'], format), 
                fecha_creacion=datetime.now(), 
                fecha_actualizacion=datetime.now()
                )
            cliente.compras.append(nueva_compra)
            db.session.add(nueva_compra)
            for item in request.json['items']:
                nuevo_item = ItemCompra(
                    unidades = item["unidades"],
                    producto_id=item["producto"]["id"]
                )
                for invent in inventario:
                    if invent.id == item["producto"]["id"]:
                        invent.unidades = invent.unidades-item["unidades"]
                nueva_compra.items.append(nuevo_item)
                cliente.productos.append(nuevo_item)
            db.session.commit()
        return {"mensaje":"Compra creada exitosamente", "compra":compra_schema.dump(nueva_compra)}, 200

class VistaCompra(Resource):
    @jwt_required()
    def get(self, id_compra):
        return compra_detalle_schema.dump(Compra.query.get_or_404(id_compra))

    @jwt_required()
    def put(self, id_compra):
        usuario = Compra.query.get_or_404(id_compra)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return {"mensaje":"Usuario actualizado exitosamente", "usuario":usuario_schema.dump(usuario)}, 200

    @jwt_required()
    def delete(self, id_compra):
        compra = Compra.query.get_or_404(id_compra)
        db.session.delete(compra)
        db.session.commit()
        return {"mensaje":"Compra eliminada exitosamente"}, 200
    


class VistaInventario(Resource):

    @jwt_required()
    def get(self):
        return[inventario_schema.dump(inventario) for inventario in Inventario.query.all()]

    @jwt_required()
    def post(self):
        id_producto = request.json['producto']['id']
        inventario = Inventario.query.filter(Inventario.producto_id == id_producto).first()
        if inventario is None:
            inventario = Inventario(
                unidades = request.json['unidades'],
                fecha_actualizacion=datetime.now(),
                producto_id = id_producto
            )
            db.session.add(inventario)
        else:
            inventario.unidades = request.json['unidades']
            inventario.fecha_actualizacion =datetime.now()
        db.session.commit()
        return {"mensaje":"Iventario actualizado", "inventario":compra_schema.dump(inventario)}, 200

class VistaInventarioProducto(Resource):
    def get(self):
        inventario = Inventario.query.all()
        array = []
        for item in inventario:
            array.append(item.producto_id)
        productos = Producto.query.filter(Producto.id.not_in(array) ).all()
        
        return[producto_schema.dump(invent) for invent in productos]


class VistaTest(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"]).first()
        if usuario is not None:
             return {"mensaje":'El usuario ya existe!'}, 409
        nuevo_usuario = Usuario(nombre="admin", contrasena="12345")
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje":"Usuario creado exitosamente", "usuario":usuario_schema.dump(nuevo_usuario)}, 200