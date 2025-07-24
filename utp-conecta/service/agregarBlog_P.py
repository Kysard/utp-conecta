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