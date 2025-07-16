# from flask import render_template, session
# from flask import Blueprint, render_template

# bp = Blueprint('editarPerfil_P', __name__, url_prefix='/')

# @bp.route('editarPerfil')
# def vista_editarPerfil():
#     user_data = session.get('user_data')
#     return render_template('editarPerfil.html', user_data=user_data)



from flask import render_template, session, request, redirect, url_for, flash, jsonify
import requests
from flask import Blueprint
from datetime import datetime  # Añade esta importación

bp = Blueprint('editarPerfil_P', __name__, url_prefix='/')

API_BASE_URL = "http://localhost:8002"

@bp.route('editarPerfil')
def vista_editarPerfil():
    user_data = session.get('user_data')
    if not user_data:
        flash("Por favor inicie sesión primero", "error")
        return redirect(url_for('login'))  # Ajusta según tu ruta de login
    
    # Convertir FechaNacimiento de string a datetime si existe
    if 'FechaNacimiento' in user_data and user_data['FechaNacimiento']:
        try:
            # Asume que la fecha viene en formato 'YYYY-MM-DD' desde la API
            user_data['FechaNacimiento_dt'] = datetime.strptime(user_data['FechaNacimiento'], '%Y-%m-%d')
        except (ValueError, TypeError):
            user_data['FechaNacimiento_dt'] = None
    
    return render_template('editarPerfil.html', user_data=user_data)

@bp.route('actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    if 'user_data' not in session:
        return jsonify({"status": "error", "message": "No autenticado"}), 401
    
    dni = session['user_data'].get('DNI')
    if not dni:
        return jsonify({"status": "error", "message": "DNI no encontrado en sesión"}), 400
    
    try:
        # Preparar los datos para la API
        datos_actualizacion = {
            "Nombres": request.form.get('nombres'),
            "ApellidoPaterno": request.form.get('apellido_paterno'),
            "ApellidoMaterno": request.form.get('apellido_materno'),
            "Genero": request.form.get('genero'),
            "Telefono": request.form.get('telefono'),
            "Email": request.form.get('email'),
            "Direccion": request.form.get('direccion'),
            "FechaNacimiento": request.form.get('fecha_nacimiento')
        }
        
        # Filtrar campos vacíos
        datos_actualizacion = {k: v for k, v in datos_actualizacion.items() if v is not None and v != ''}
        
        # Llamar a la API
        response = requests.put(
            f"{API_BASE_URL}/api/actualizar/{dni}",
            json=datos_actualizacion
        )
        
        if response.status_code == 200:
            # Actualizar los datos en la sesión
            user_data = session['user_data']
            for key, value in datos_actualizacion.items():
                if key != "FechaNacimiento":  # Manejo especial para fechas
                    user_data[key] = value
                else:
                    # Guardar la fecha como string
                    user_data[key] = value
            
            session['user_data'] = user_data
            session.modified = True
            
            return jsonify({"status": "success", "message": "Perfil actualizado correctamente"})
        else:
            error_data = response.json()
            return jsonify({"status": "error", "message": error_data.get("detail", "Error al actualizar perfil")}), response.status_code
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    










# <!DOCTYPE html>
# <html lang="en">

# <head>
# 	<meta charset="UTF-8">
# 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
# 	<title>Editar Perfil | UTP Conecta +</title>
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
# 							<h5 class="text-uppercase mb-0 mt-0 page-title">Editar Perfil</h5>
# 						</div>
# 						<div class="col-lg-6 col-md-6 col-sm-6 col-12">
# 							<ul class="breadcrumb float-right p-0 mb-0">
# 								<li class="breadcrumb-item"><a href="#"><i class="fas fa-home"></i> Inicio</a>
# 								</li>
# 								<li class="breadcrumb-item"><a href="#">Pagina</a></li>
# 								<li class="breadcrumb-item"><span>Editar Perfil</span></li>
# 							</ul>
# 						</div>
# 					</div>
# 				</div>
# 				<div class="page-content">
# 					<div class="row">
# 						<div class="col-lg-12 col-md-12 col-sm-12 col-12">
# 							<div class="card">
# 								<div class="card-header">
# 									<div class="card-title">Informacion</div>
# 								</div>
# 								<div class="card-body">
# 									<div class="row">
# 										<div class="col-lg-6 col-md-6 col-sm-6 col-12">
# 											<form>
# 												<div class="form-group">
# 													<label>Nombre</label>
# 													<input type="text" class="form-control" value="{{ user_data.Nombres }}">
# 												</div>
# 												<div class="form-group">
# 													<label>Apellido Paterno</label>
# 													<input type="text" class="form-control" value="{{ user_data.ApellidoPaterno }}">
# 												</div>
# 												<div class="form-group">
# 													<label>Apellido Materno</label>
# 													<input type="text" class="form-control" value="{{ user_data.ApellidoMaterno }}">
# 												</div>

# 												<div class="form-group">
# 													<label>Genero</label>
# 													<select class="form-control select">
# 														<option>Masculino</option>
# 														<option>Femenino</option>
# 													</select>
# 												</div>
												
# 											</form>
# 										</div>
# 										<div class="col-lg-6 col-md-6 col-sm-6 col-12">
# 											<form>
# 												<div class="form-group">
# 													<label>Telefono</label>
# 													<input type="number" class="form-control" value="{{ user_data.Telefono }}">
# 												</div>
# 												<div class="form-group">
# 													<label>Email</label>
# 													<input type="text" class="form-control"
# 														value="{{ user_data.Email }}">
# 												</div>
# 												<div class="form-group">
# 													<label>Fecha de Nacimiento</label>
# 													<input class="form-control datetimepicker-input datetimepicker"
# 														type="text" data-toggle="datetimepicker">
# 												</div>

# 											</form>
# 										</div>
# 										<div class="col-lg-12 col-md-12 col-sm-12 col-12">
# 											<form>
# 												<div class="form-group">
# 													<label>Direccion</label>
# 													<textarea class="form-control"
# 														placeholder="Present Address">{{ user_data.Direccion }}</textarea>
# 												</div>
# 											</form>
# 										</div>
# 										<div class="col-lg-12 col-md-12 col-sm-12 col-12">
# 											<form>
# 												<div class="form-group">
# 													<label>Cargar Imagen</label>
# 													<input type="file" name="pic" accept="image/*" class="form-control">
# 												</div>
# 											</form>
# 										</div>
# 										<div class="col-lg-12 col-md-12 col-sm-12 col-12">
# 											<form>
# 												<div class="form-group text-center custom-mt-form-group">
# 													<button class="btn btn-primary mr-2" type="submit">Guardar</button>
# 													<button class="btn btn-secondary" type="reset">Cancelar</button>
# 												</div>
# 											</form>
# 										</div>
# 									</div>
# 								</div>
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

# 	<script src="../static/plugins/datetimepicker/js/tempusdominus-bootstrap-4.min.js"></script>

# 	<script src="../static/js/app.js"></script>

# </body>

# </html>