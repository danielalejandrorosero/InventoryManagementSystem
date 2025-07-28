from app.models.productos import Producto
from app.decorators import requiere_nivel
from app.models.proveedores import Proveedor
from app.models.unidades_medida import UnidadMedida
from app.models.categorias import Categoria
from app.database import db
from flask_jwt_extended import jwt_required
from app.schemas.productos_schemas import ProductoSchema,ListarProductosSchema,BuscarProductosSchema
from flask import Blueprint, request, jsonify


productos_bp = Blueprint('productos', __name__, url_prefix='/productos')


@productos_bp.route('/crearProducto', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def crear_producto():
    try:
        data = ProductoSchema().load(request.json)
        if not data:
            return jsonify({'msg': 'No se recibieron datos válidos'})
        # El precio de compra y venta deben ser mayores a 0
        if data['precio_compra'] <= 0 or data['precio_venta'] <= 0:
            return jsonify({'msg': 'El precio de compra y venta deben ser mayores a 0'}), 400
        if not Categoria.query.filter_by(id_categoria=data['id_categoria']).first():
            return jsonify({'msg': 'La categoría no existe'}), 400
        # proveedorExiste
        if not Proveedor.query.filter_by(id_proveedor=data['id_proveedor']).first():
            return jsonify({'msg': 'El proveedor no existe'}), 400
        if not UnidadMedida.query.filter_by(id_unidad=data['id_unidad_medida']).first():
            return jsonify({'msg': 'La unidad de medida no existe'}), 400
        # codigo existe
        if Producto.query.filter_by(codigo=data['codigo']).first():
            return jsonify({'msg': 'El código del producto ya existe'}), 400
        if Producto.query.filter_by(sku=data['sku']).first():
            return jsonify({'msg': 'El SKU del producto ya existe'}), 400
        # Crear el nuevo producto
        crear_producto = Producto(
            nombre_producto=data['nombre_producto'],
            codigo=data['codigo'],
            sku=data['sku'],
            descripcion=data['descripcion'],
            precio_compra=data['precio_compra'],
            precio_venta=data['precio_venta'],
            id_unidad_medida=data['id_unidad_medida'],
            stock_minimo=data.get('stock_minimo', 0.0),
            stock_maximo=data.get('stock_maximo', 0.0),
            id_categoria=data['id_categoria'],
            id_proveedor=data['id_proveedor'],
        )
        db.session.add(crear_producto)
        db.session.commit()
        return jsonify({'msg': 'Producto creado correctamente'}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'Error interno del servidor: {str(e)}'}), 500



@productos_bp.route('/listarProductos', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_productos():
    try:
        productos = Producto.query.filter_by(estado='activo').all()
        if not productos:
            return jsonify({'msg': 'No se encontraron productos'}), 404
        productos_con_imagen = []
        for producto in productos:
            # Obtener la primera imagen asociada (si existe)
            imagen = None
            if hasattr(producto, 'imagenes') and producto.imagenes:
                img = producto.imagenes[0]
                imagen = {
                    'id_imagen': img.id_imagen,
                    'nombre_imagen': img.nombre_imagen,
                    'ruta_imagen': img.ruta_imagen
                }
            prod_dict = {
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'codigo': producto.codigo,
                'sku': producto.sku,
                'precio_compra': producto.precio_compra,
                'precio_venta': producto.precio_venta,
                'stock_minimo': producto.stock_minimo,
                'stock_maximo': producto.stock_maximo,
                'id_categoria': producto.id_categoria,
                'id_proveedor': producto.id_proveedor,
                'imagen': imagen
            }
            productos_con_imagen.append(prod_dict)
        data = ListarProductosSchema(many=True).dump(productos_con_imagen)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'msg': f'Error interno del servidor: {str(e)}'}), 500

@productos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def editar_producto(id):
    producto = Producto.query.get(id)
    if not producto or producto.estado != 'activo':
        return jsonify({'msg': 'Producto no encontrado'}), 404
    try:
        data = ProductoSchema().load(request.json)
        # Validaciones de integridad referencial y de datos
        if data['precio_compra'] <= 0 or data['precio_venta'] <= 0:
            return jsonify({'msg': 'El precio de compra y venta deben ser mayores a 0'}), 400
        if not Categoria.query.filter_by(id_categoria=data['id_categoria']).first():
            return jsonify({'msg': 'La categoría no existe'}), 400
        if not Proveedor.query.filter_by(id_proveedor=data['id_proveedor']).first():
            return jsonify({'msg': 'El proveedor no existe'}), 400
        if not UnidadMedida.query.filter_by(id_unidad=data['id_unidad_medida']).first():
            return jsonify({'msg': 'La unidad de medida no existe'}), 400
        # Validar código y SKU solo si cambian
        if data['codigo'] != producto.codigo and Producto.query.filter_by(codigo=data['codigo']).first():
            return jsonify({'msg': 'El código del producto ya existe'}), 400
        if data['sku'] != producto.sku and Producto.query.filter_by(sku=data['sku']).first():
            return jsonify({'msg': 'El SKU del producto ya existe'}), 400
    except Exception as err:
        return jsonify({'msg': 'Datos inválidos', 'errors': getattr(err, 'messages', str(err))}), 400
    # Actualizar los datos del producto
    producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
    producto.codigo = data.get('codigo', producto.codigo)
    producto.sku = data.get('sku', producto.sku)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio_compra = data.get('precio_compra', producto.precio_compra)
    producto.precio_venta = data.get('precio_venta', producto.precio_venta)
    producto.id_unidad_medida = data.get('id_unidad_medida', producto.id_unidad_medida)
    producto.stock_minimo = data.get('stock_minimo', producto.stock_minimo)
    producto.stock_maximo = data.get('stock_maximo', producto.stock_maximo)
    producto.id_categoria = data.get('id_categoria', producto.id_categoria)
    producto.id_proveedor = data.get('id_proveedor', producto.id_proveedor)
    try:
        db.session.commit()
        return jsonify({'msg': 'Producto actualizado correctamente'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({'msg': 'Error interno del servidor', 'errors': str(err)}), 500


@productos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requiere_nivel([1, 2])
def eliminar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'msg': 'Producto no encontrado'}), 404
    try:
        producto.estado = 'eliminado'
        db.session.commit()
        return jsonify({'msg': 'Producto eliminado correctamente (soft delete)'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({'msg': 'Error interno del servidor', 'errors': str(err)}), 500


# restaurar producto
@productos_bp.route('/restaurar/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])

def restaurar_producto(id):
    producto = Producto.query.get(id)

    if not producto:
        return jsonify({'msg': 'Producto no encontrado'}), 404

    if producto.estado != 'eliminado':
        return jsonify({'msg': 'El producto no está marcado como eliminado'}), 400

    try:
        producto.estado = 'activo'
        db.session.commit()
        return jsonify({'msg': 'Producto restaurado correctamente'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({
            'msg': 'Error interno del servidor',
            'error': str(err)
        }), 500

# listar productos eliminados
@productos_bp.route('/listar_eliminados', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_productos_eliminados():
    try:
        productos_eliminados = Producto.query.filter_by(estado='eliminado').all()
        if not productos_eliminados:
            return jsonify({'msg': 'No se encontraron productos eliminados'}), 404
        productos_con_imagen = []
        for producto in productos_eliminados:
            imagen = None
            if hasattr(producto, 'imagenes') and producto.imagenes:
                img = producto.imagenes[0]
                imagen = {
                    'id_imagen': img.id_imagen,
                    'nombre_imagen': img.nombre_imagen,
                    'ruta_imagen': img.ruta_imagen
                }
            prod_dict = {
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'codigo': producto.codigo,
                'sku': producto.sku,
                'precio_compra': producto.precio_compra,
                'precio_venta': producto.precio_venta,
                'stock_minimo': producto.stock_minimo,
                'stock_maximo': producto.stock_maximo,
                'id_categoria': producto.id_categoria,
                'id_proveedor': producto.id_proveedor,
                'imagen': imagen
            }
            productos_con_imagen.append(prod_dict)
        data = ListarProductosSchema(many=True).dump(productos_con_imagen)
        return jsonify(data), 200
    except Exception as err:
        return jsonify({'msg': 'Error interno del servidor', 'error': str(err)}), 500


# buscar productos por cualquier campo

@productos_bp.route('/buscarProductos', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def buscar_productos():
    try:
        data = request.get_json()
        busqueda = data.get('busqueda', '').strip() if data else ''
        if not busqueda:
            return jsonify({'msg': 'Debes enviar un valor en "busqueda"'}), 400

        like = f"%{busqueda}%"
        # Hacemos join con Categoria, Proveedor y UnidadMedida
        query = db.session.query(Producto).join(Producto.categoria).join(Producto.proveedor).join(Producto.unidad_medida)
        filtros = [Producto.estado == 'activo']
        filtros.append(
            db.or_(
                Producto.nombre_producto.ilike(like),
                Producto.codigo.ilike(like),
                Producto.sku.ilike(like),
                Producto.descripcion.ilike(like),
                Categoria.nombre_categoria.ilike(like),
                Proveedor.nombre_proveedor.ilike(like),
                UnidadMedida.nombre.ilike(like)
            )
        )
        productos = query.filter(*filtros).all()
        if not productos:
            return jsonify({'msg': 'No se encontraron productos'}), 404
        productos_con_imagen = []
        for producto in productos:
            imagen = None
            if hasattr(producto, 'imagenes') and producto.imagenes:
                img = producto.imagenes[0]
                imagen = {
                    'id_imagen': img.id_imagen,
                    'nombre_imagen': img.nombre_imagen,
                    'ruta_imagen': img.ruta_imagen
                }
            prod_dict = {
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'codigo': producto.codigo,
                'sku': producto.sku,
                'precio_compra': producto.precio_compra,
                'precio_venta': producto.precio_venta,
                'stock_minimo': producto.stock_minimo,
                'stock_maximo': producto.stock_maximo,
                'id_categoria': producto.id_categoria,
                'id_proveedor': producto.id_proveedor,
                'imagen': imagen
            }
            productos_con_imagen.append(prod_dict)
        data = ListarProductosSchema(many=True).dump(productos_con_imagen)
        return jsonify(data), 200
    except Exception as err:
        return jsonify({'msg': 'Error interno del servidor', 'error': str(err)}), 500
