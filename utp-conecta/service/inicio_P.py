from flask import Blueprint, redirect, render_template, session, url_for, jsonify
import requests
import json
from datetime import datetime

bp = Blueprint('inicio_P', __name__, url_prefix='/')

# Configuración de la API
API_BASE_URL = 'http://127.0.0.1:8002/api/blog'

# Registra el filtro en el blueprint
@bp.app_template_filter('format_datetime')
def format_datetime(value, format='%d/%m/%Y %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
                # Intenta otro formato si el primero falla
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                return value  # Devuelve el valor original si no se puede parsear
    return value.strftime(format)

@bp.route('/inicio')
def vista_inicio():
    # Verificar si el usuario está autenticado
    if not session.get('autenticado'):
        return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))
    
    user_data = session.get('user_data')
    token = session.get('token')
    
    try:
        # Obtener blogs de todos los usuarios
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }
        
        # 1. Obtener blogs públicos
        response_blogs = requests.get(
            f'{API_BASE_URL}/blogs-publicos',
            headers=headers
        )
        
        if response_blogs.status_code != 200:
            blogs = []
        else:
            blogs = response_blogs.json()
            
            # Procesar multimedia para el template
            for blog in blogs:
                for img in blog.get('multimedia', []):
                    # Corregir ruta de imágenes
                    img['ruta'] = img['ruta'].replace('\\', '/')  # Convertir barras invertidas a normales
                    img['ruta'] = img['ruta'].replace('/static/uploads/blogs/', '/static/fastapi-blogs/')
        
        # 2. Obtener categorías para el sidebar
        response_categorias = requests.get(
            f'{API_BASE_URL}/categorias-subcategorias',
            headers=headers
        )
        
        categorias = []
        if response_categorias.status_code == 200:
            categorias_data = response_categorias.json().get('categorias', {})
            categorias = [
                {
                    'id': int(cat_id),
                    'nombre': cat['nombre'],
                    'icono': cat['icono']
                }
                for cat_id, cat in categorias_data.items()
            ]
        
        return render_template(
            'inicio.html',
            user_data=user_data,
            blogs=blogs,
            categorias=categorias
        )
            
    except requests.exceptions.RequestException as e:
        return render_template(
            'inicio.html',
            user_data=user_data,
            blogs=[],
            categorias=[],
            error=f"Error de conexión: {str(e)}"
        )
    except Exception as e:
        return render_template(
            'inicio.html',
            user_data=user_data,
            blogs=[],
            categorias=[],
            error=f"Error inesperado: {str(e)}"
        )