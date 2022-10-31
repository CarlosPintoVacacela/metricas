from flaskr import create_app
from flaskr.vistas.vistas import VistaProducto
from .modelos import db, Usuario
from flask_restful import Api
from .vistas import VistaClientes,VistaProductos, VistaLogIn, VistaUsuarios, VistaCliente, VistaUsuario, VistaProducto, VistaCompras, VistaCompra, VistaInventario, VistaInventarioProducto, VistaTest
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

CORS(app)

api = Api(app)

api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaClientes, '/clientes')
api.add_resource(VistaCliente, '/cliente/<int:id_cliente>')
api.add_resource(VistaProductos, '/productos')
api.add_resource(VistaProducto, '/producto/<int:id_producto>')
api.add_resource(VistaCompras, '/compras')
api.add_resource(VistaCompra, '/compra/<int:id_compra>')
api.add_resource(VistaInventario, '/inventario')
api.add_resource(VistaInventarioProducto, '/inventarioprod')
api.add_resource(VistaTest, '/test')

jwt = JWTManager(app)
