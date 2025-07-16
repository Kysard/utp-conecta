# from flask import render_template, session
# from flask import Blueprint, render_template

# bp = Blueprint('agregarBlog_P', __name__, url_prefix='/')

# @bp.route('/agregarBlog')
# def vista_agregarBlog():
#     user_data = session.get('user_data')
#     return render_template('agregarBlog.html', user_data=user_data)



# <!DOCTYPE html>
# <html lang="es">

# <head>
# 	<meta charset="UTF-8">
# 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
# 	<title>Agregar Blog | UTP Conecta +</title>
# 	{% include 'head.html' %}
# </head>

# <body>


# 	<div class="main-wrapper">

# 		{% include 'encabezado.html' %}
# 		{% include 'barraLateral.html' %}

# 		<div class="page-wrapper">
# 			<div class="content container-fluid">
# 				<div class="page-header">
# 					<div class="row">
# 						<div class="col-lg-6 col-md-6 col-sm-6 col-12">
# 							<h5 class="text-uppercase mb-0 mt-0 page-title">Agregar blog</h5>
# 						</div>
# 						<div class="col-lg-6 col-md-6 col-sm-6 col-12">
# 							<ul class="breadcrumb float-right p-0 mb-0">
# 								<li class="breadcrumb-item"><a href="#">Inicio</a></li>
# 								<li class="breadcrumb-item"><a href="#">Blog</a></li>
# 								<li class="breadcrumb-item"><span> Agregar blog</span></li>
# 							</ul>
# 						</div>
# 					</div>
# 				</div>
# 				<div class="card">
# 					<div class="card-body">
# 						<div class="row">
# 							<div class="col-md-12">
# 								<form>
# 									<div class="form-group">
# 										<label>Nombre del blog</label>
# 										<input type="text" class="form-control">
# 									</div>
# 									<div class="form-group">
# 										<label>Imágenes del blog</label>
# 										<input type="file" name="pic" accept="image/*" class="form-control">
# 										<small class="form-text text-muted">Tamaño máximo de archivo: 50 MB. Imágenes
# 											permitidas: jpg, gif, png. Máximo 10 imágenes solamente.</small>
# 									</div>
# 									<div class="form-group">
# 										<div class="row">
# 											<div class="col-md-3 col-sm-3 col-4 col-lg-3 col-xl-2">
# 												<div class="product-thumbnail">
# 													<img src="../static/img/blog/blog-thumb-01.jpg"
# 														class="img-thumbnail img-fluid" alt="">
# 													<span class="product-remove" title="eliminar"><i
# 															class="fas fa-times"></i></span>
# 												</div>
# 											</div>
# 											<div class="col-md-3 col-sm-3 col-4 col-lg-3 col-xl-2">
# 												<div class="product-thumbnail">
# 													<img src="../static/img/placeholder-thumb.jpg"
# 														class="img-thumbnail img-fluid" alt="">
# 													<span class="product-remove" title="eliminar"><i
# 															class="fas fa-times"></i></span>
# 												</div>
# 											</div>
# 											<div class="col-md-3 col-sm-3 col-4 col-lg-3 col-xl-2">
# 												<div class="product-thumbnail">
# 													<img src="../static/img/placeholder-thumb.jpg"
# 														class="img-thumbnail img-fluid" alt="">
# 													<span class="product-remove" title="eliminar"><i
# 															class="fas fa-times"></i></span>
# 												</div>
# 											</div>
# 											<div class="col-md-3 col-sm-3 col-4 col-lg-3 col-xl-2">
# 												<div class="product-thumbnail">
# 													<img src="../static/img/placeholder-thumb.jpg"
# 														class="img-thumbnail img-fluid" alt="">
# 													<span class="product-remove" title="eliminar"><i
# 															class="fas fa-times"></i></span>
# 												</div>
# 											</div>
# 										</div>
# 									</div>

# 									<div class="row">
# 										<div class="col-md-6">
# 											<div class="form-group">
# 												<label>Categoría del blog</label>
# 												<select class="form-control select">
# 													<option>Biblioteca</option>
# 													<option>Deporte</option>
# 													<option>Gestión</option>
# 												</select>
# 											</div>
# 										</div>
# 										<div class="col-lg-6 col-md-6">
# 											<div class="form-group">
# 												<label>Subcategoría del blog</label>
# 												<select class="form-control select">
# 													<option>Ingeniería de Sistemas</option>
# 													<option>Administración</option>
# 													<option>Marketing</option>
# 													<option>Contabilidad</option>
# 													<option>Psicología</option>
# 													<option>Ingeniería Industrial</option>
# 													<option>Comunicación</option>
# 													<option>Medicina</option>
# 												</select>
# 											</div>
# 										</div>
# 									</div>
# 									<div class="form-group">
# 										<label>Descripción del blog</label>
# 										<input type="text" class="form-control">
# 									</div>
# 									<div class="m-t-20 text-center">
# 										<button class="btn btn-primary btn-lg">Publicar blog</button>
# 									</div>
# 								</form>
# 							</div>
# 						</div>
# 					</div>
# 				</div>
# 			</div>
# 		</div>
# 	</div>

# 	<script src="../static/js/jquery-3.6.0.min.js"></script>

# 	<script src="../static/js/bootstrap.bundle.min.js"></script>

# 	<script src="../static/js/jquery.slimscroll.js"></script>

# 	<script src="../static/js/select2.min.js"></script>
# 	<script src="../static/js/moment.min.js"></script>

# 	<script src="../static/js/app.js"></script>

# </body>

# </html>



from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
import requests
import os

bp = Blueprint('agregarBlog_P', __name__, url_prefix='/')

# Configuración de la API
API_BASE_URL = "http://127.0.0.1:8002/api/blog"  # Ajusta según tu configuración

@bp.route('/agregarBlog')
def vista_agregarBlog():
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for('login'))  # Redirigir si no hay sesión
    
    # Obtener categorías y subcategorías de la API
    try:
        response = requests.get(f"{API_BASE_URL}/categorias-subcategorias")
        if response.status_code == 200:
            categorias = response.json().get('categorias', {})
        else:
            categorias = {}
    except requests.exceptions.RequestException:
        categorias = {}
    
    return render_template('agregarBlog.html', 
                         user_data=user_data,
                         categorias=categorias)

@bp.route('/agregarBlog', methods=['POST'])
def crear_blog():
    user_data = session.get('user_data')
    if not user_data:
        return jsonify({"error": "No autorizado"}), 401
    
    try:
        # Preparar datos del formulario
        form_data = {
            'titulo': request.form.get('titulo'),
            'contenido': request.form.get('contenido'),
            'id_usuario': user_data.get('IdUsuario'),  # Obtener del usuario logueado
            'id_categoria': request.form.get('categoria'),
            'id_subcategoria': request.form.get('subcategoria'),
            'estado': 'Activo'
        }
        
        # Preparar archivos
        files = []
        if 'imagenes' in request.files:
            for file in request.files.getlist('imagenes'):
                if file.filename != '':
                    files.append(('imagenes', (file.filename, file.stream, file.mimetype)))
        
        # Enviar a la API
        response = requests.post(
            f"{API_BASE_URL}/crear-blog",
            data=form_data,
            files=files
        )
        
        if response.status_code == 201:
            return jsonify(response.json()), 201
        else:
            return jsonify({"error": "Error al crear el blog"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500