from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from controller.producto_controller import *
from controller.proveedor_controller import *
from controller.categoria_controller import *
from controller.inventario_controller import *
from controller.login_controller import *

app = Flask(__name__)
app.secret_key = "GP2TkNjHVx"

######################################################################################
################################ INC RUTAS PRODUCTOS #################################
######################################################################################
@app.route('/productos', methods=["GET"])
def productos():
    productos = get_productos()
    categorias = get_categorias()
    proveedores = get_proveedores()
    respuesta = []

    print(productos)
    for i in productos:
        nombre_categoria = ""
        nombre_proveedor = ""
        for c in categorias:
            print(c)
            if i["id_categoria"] == c["id"]:
                nombre_categoria = c["nombre"]
        
        for p in proveedores:
            print(p)
            if i["id_proveedor"] == p["id"]:
                nombre_proveedor = p["nombre"]

        data = {
            "id" :  i["id"],
            "nombre" : i["nombre"],
            "precio" : i["precio"],
            "nombre_categoria" : nombre_categoria,
            "nombre_proveedor" : nombre_proveedor,
            "fecha_creacion" : i["fecha_creacion"] 
        }
        respuesta.append(data)
    print(respuesta)
    return render_template("/producto/tables.html",respuesta=respuesta)
    # return jsonify(productos)

@app.route('/producto/<int:id>', methods=["GET"])
def producto(id):
    producto = get_producto(id)
    if producto:
        return jsonify(producto)
    else:
        return "Producto no encontrado", 404

@app.route('/crear-producto', methods=["POST"])
def crear_producto():
    data = request.get_json()
    nombre = data["nombre"]
    precio = data["precio"]
    id_categoria = data["id_categoria"]
    id_proveedor = data["id_proveedor"]
    fecha_creacion = data["fecha_creacion"]
    result = insert_producto(nombre, precio, id_categoria, id_proveedor, fecha_creacion)
    return jsonify(result), 201

@app.route('/editar-producto/<int:id>', methods=["PUT"])
def editar_producto(id):
    data = request.get_json()
    nombre = data["nombre"]
    precio = data["precio"]
    id_categoria = data["id_categoria"]
    id_proveedor = data["id_proveedor"]
    fecha_creacion = data["fecha_creacion"]
    result = edit_producto(id, nombre, precio, id_categoria, id_proveedor, fecha_creacion)
    return result

@app.route('/eliminar-producto/<int:id>', methods=["DELETE"])
def eliminar_producto(id):
    result = delete_producto(id)
    return result
######################################################################################
################################ FIN RUTAS PRODUCTOS #################################
######################################################################################

######################################################################################
############################### INC RUTAS PROVEEDORES ################################
######################################################################################
@app.route('/proveedores', methods=["GET"])
def proveedores():
    proveedores = get_proveedores()
    return render_template("/proveedor/tables.html",proveedores=proveedores)
    #return jsonify(categorias)

@app.route('/proveedor/<int:id>', methods=["GET"])
def proveedor(id):
    proveedor = get_proveedor(id)
    if proveedor:
        return jsonify(proveedor)
    else:
        return "Proveedor no encontrado", 404

@app.route('/crear-proveedor', methods=["POST"])
def crear_proveedor():
    data = request.get_json()
    nombre = data["nombre"]
    result = insert_proveedor(nombre)
    return jsonify(result), 201

@app.route('/editar-proveedor/<int:id>', methods=["PUT"])
def editar_proveedor(id):
    data = request.get_json()
    nombre = data["nombre"]
    result = edit_proveedor(id, nombre)
    return result

@app.route('/eliminar-proveedor/<int:id>', methods=["DELETE"])
def eliminar_proveedor(id):
    result = delete_proveedor(id)
    return result
######################################################################################
############################### FIN RUTAS PROVEEDORES ################################
######################################################################################

######################################################################################
################################ INC RUTAS CATEGORIAS ################################
######################################################################################
@app.route('/categorias', methods=["GET"])
def categorias():
    if "user" in session:
        categorias = get_categorias()
        return render_template("/categoria/tables.html",categorias=categorias)
    else:
        return render_template("/base_vistas/Error.html")

@app.route('/categoria/<int:id>', methods=["GET"])
def categoria(id):
    categoria = get_categoria(id)
    if categoria:
        return jsonify(categoria)
    else:
        return "Categoria no encontrado", 404

@app.route('/crear-categoria', methods=["POST","GET"])
def crear_categoria():
    if "user" in session:
        if request.method == "GET":
            return render_template("/categoria/register.html")
        else:
            nombre = request.form.get('nombre')
            result = insert_categoria(nombre)
            print(result)
            return redirect(url_for("categorias"))
    else:
        return render_template("/base_vistas/Error.html")    

@app.route('/modificar-categoria/<int:id>', methods=['GET', 'POST'])
def modificar_categoria(id):
    if request.method == "GET":
        if "user" in session:
            # Recuperar la categoría correspondiente a través del ID
            categoria = get_categoria(id)
            return render_template('categoria/form-modificar.html', categoria=categoria)
        else:
            return render_template("/base_vistas/Error.html")
    else:
        # Procesar el formulario de modificación aquí
        nuevo_nombre = request.form.get('nombre')
        id = id
        print(f"nuevo_nombre: {nuevo_nombre} id: {id}")
        # Actualizar la categoría en la base de datos o donde sea necesario
        result = edit_categoria(id, nuevo_nombre)
        print(f"result: {result}")
        # Redirigir a la página principal o a donde desees después de la modificación
        return redirect(url_for("categorias"))

@app.route('/eliminar-categoria/<int:id>', methods=['GET'])
def eliminar_categoria(id):
    if "user" in session:
        result = delete_categoria(id)
        print(result)
        return redirect(url_for("categorias"))
    else:
        return render_template("/base_vistas/Error.html")

######################################################################################
################################ FIN RUTAS CATEGORIAS ################################
######################################################################################

######################################################################################
############################### INC RUTAS INVENTARIOS ################################
######################################################################################

'''RUTAS INVENTARIOS'''
@app.route('/inventarios', methods=["GET"])
def inventarios():
    inventarios = get_inventarios()
    return render_template("/inventario/tables.html",inventarios=inventarios)
    #return jsonify(inventarios)

@app.route('/inventario/<int:id>', methods=["GET"])
def inventario(id):
    inventario = get_inventario(id)
    if inventario:
        return jsonify(inventario)
    else:
        return "Inventario no encontrado", 404

@app.route('/crear-inventario', methods=["POST"])
def crear_inventario():
    data = request.get_json()
    nombre = data["nombre"]
    result = insert_inventario(nombre)
    return jsonify(result), 201

@app.route('/editar-inventario/<int:id>', methods=["PUT"])
def editar_inventario(id):
    data = request.get_json()
    nombre = data["nombre"]
    result = edit_inventario(id, nombre)
    return result
'''FIN RUTAS INVENTARIOS'''


@app.route("/crear-inventario")
def vista_crear_inventario():
    return render_template("/inventario/crear_inventario.html")

@app.route("/crear-producto")
def vista_crear_producto():
    return render_template("/producto/register.html")

# @app.route("/crear-categoria")
# def vista_crear_categoria():
#     return render_template("/categoria/register.html")

@app.route("/crear-proveedor")
def vista_crear_proveedor():
    return render_template("/proveedor/register.html")

@app.route("/editar-inventario")
def vista_editar_inventario():
    return render_template("/inventario/editar.html")

@app.route("/editar-producto")
def vista_editar_producto():
    return render_template("/producto/editar.html")

@app.route("/editar-categoria")
def vista_editar_categoria():
    return render_template("/categoria/editar.html")

@app.route("/editar-proveedor")
def vista_editar_proveedor():
    return render_template("/proveedor/editar.html")

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/index", methods = ["GET","POST"])
def principal():
        if request.method == "GET":
            if "user" in session:
                return render_template("/index/index.html")
            else:
                return render_template("/base_vistas/Error.html")
        else:
            return render_template("/index/index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    print("dentro del login")
    if request.method == "GET":
        return render_template("/login/login.html")
    else:
        # Obtenemos los datos del formulario
        email = request.form.get("email")
        password = request.form.get("password")
        user = get_usuario(email,password)

        # Validamos los datos
        if user:
            print(f"user: {user}")
            print(f"email: {email}")
            session["user"] = email
            print(session["user"])
            return redirect(url_for("principal"))
        else:
            return render_template("/login/404.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



    
if __name__ == '__main__':
    app.run(debug=True)