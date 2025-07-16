from flask import render_template, session, request, redirect, url_for, flash, jsonify
import requests
from flask import Blueprint
from datetime import datetime

bp = Blueprint('editarPerfil_P', __name__, url_prefix='/')

API_BASE_URL = "http://localhost:8002"

@bp.route('editarPerfil')
def vista_editarPerfil():
    user_data = session.get('user_data')
    if not user_data:
        flash("Por favor inicie sesión primero", "error")
        return redirect(url_for('login'))
    
    if 'FechaNacimiento' in user_data and user_data['FechaNacimiento']:
        try:
            # Convertir a datetime y luego formatear como YYYY-MM-DD
            fecha_dt = datetime.strptime(user_data['FechaNacimiento'], '%Y-%m-%d')
            user_data['FechaNacimiento_formatted'] = fecha_dt.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            user_data['FechaNacimiento_formatted'] = ''
    
    return render_template('editarPerfil.html', user_data=user_data)

@bp.route('actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    if 'user_data' not in session:
        return jsonify({"status": "error", "message": "No autenticado"}), 401
    
    dni = session['user_data'].get('DNI')
    if not dni:
        return jsonify({"status": "error", "message": "DNI no encontrado en sesión"}), 400
    
    try:
        # Mapear los nombres de los campos del formulario a los que espera la API
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
        
        # Filtrar campos vacíos o nulos
        datos_actualizacion = {k: v for k, v in datos_actualizacion.items() if v is not None and v != ''}
        
        if not datos_actualizacion:
            return jsonify({"status": "error", "message": "No se proporcionaron datos para actualizar"}), 400
        
        # Llamar a la API
        response = requests.put(
            f"{API_BASE_URL}/api/usuario/actualizar/{dni}",
            json=datos_actualizacion,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            # Actualizar los datos en la sesión
            user_data = session['user_data']
            for key, value in datos_actualizacion.items():
                user_data[key] = value
            
            session['user_data'] = user_data
            session.modified = True
            
            return jsonify({"status": "success", "message": "Perfil actualizado correctamente"})
        else:
            # Manejar errores de la API
            try:
                error_data = response.json()
                return jsonify({"status": "error", "message": error_data.get("detail", "Error al actualizar perfil")}), response.status_code
            except ValueError:
                return jsonify({"status": "error", "message": f"Error en la API: {response.text}"}), response.status_code
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500