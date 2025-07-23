from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
import requests
import json

bp = Blueprint('editarBlog_P', __name__, url_prefix='/')

# Configuración de la API
API_BASE_URL = 'http://127.0.0.1:8002/api/blog'

@bp.route('/editarBlog')
def vista_editarBlog():
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for('login'))
    
    id_post = request.args.get('id')
    if not id_post:
        return "ID de blog no proporcionado", 400
    
    try:
        # Obtener token de sesión
        token = session.get('token')
        if not token:
            return redirect(url_for('login'))
        
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }
        
        # 1. Obtener datos del blog desde la API
        response_blog = requests.get(
            f'{API_BASE_URL}/blog/{id_post}',
            headers=headers
        )
        
        if response_blog.status_code != 200:
            return f"Blog no encontrado (Error {response_blog.status_code})", 404
            
        blog_data = response_blog.json()
        
        # Verificar que el blog pertenece al usuario
        if blog_data['id_usuario'] != user_data['IdUsuario']:
            return "No tienes permiso para editar este blog", 403
            
        # 2. Obtener categorías y subcategorías
        response_categorias = requests.get(
            f'{API_BASE_URL}/categorias-subcategorias',
            headers=headers
        )
        
        if response_categorias.status_code != 200:
            return "Error al obtener categorías", 500
            
        categorias_data = response_categorias.json().get('categorias', {})
        
        # Preparar datos para el template
        blog = {
            'id_post': blog_data['id_post'],
            'titulo': blog_data['titulo'],
            'contenido': blog_data['contenido'],
            'estado': blog_data['estado'],
            'categoria_actual': blog_data['categorias'][0]['id_categoria'] if blog_data['categorias'] else None,
            'subcategoria_actual': blog_data['categorias'][0]['id_subcategoria'] if blog_data['categorias'] else None,
            'multimedia': blog_data['multimedia']
        }
        
        # Procesar multimedia para el template
        for img in blog['multimedia']:
            # Corregir ruta de imágenes
            img['ruta'] = img['ruta'].replace('\\', '/')  # Convertir barras invertidas a normales
            img['ruta'] = img['ruta'].replace('/static/uploads/blogs/', '/static/fastapi-blogs/')
            img['nombre_archivo'] = img['ruta'].split('/')[-1]
        
        # Preparar estructura de categorías más plana para el template
        categorias_lista = []
        subcategorias_lista = []
        
        for cat_id, cat in categorias_data.items():
            categorias_lista.append({
                'id': int(cat_id),
                'nombre': cat['nombre'],
                'icono': cat['icono']
            })
            
            for sub in cat['subcategorias']:
                subcategorias_lista.append({
                    'id': sub['id'],
                    'nombre': sub['nombre'],
                    'id_categoria': int(cat_id)
                })
        
        return render_template(
            'editarBlog.html',
            user_data=user_data,
            blog=blog,
            categorias=categorias_lista,
            subcategorias=subcategorias_lista,
            subcategoria_actual=blog['subcategoria_actual'])
            
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con la API: {str(e)}", 500
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

@bp.route('/obtener-subcategorias/<int:id_categoria>')
def obtener_subcategorias(id_categoria):
    try:
        token = session.get('token')
        if not token:
            return jsonify({'error': 'No autenticado'}), 401
            
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }
        
        response = requests.get(
            f'{API_BASE_URL}/categorias-subcategorias',
            headers=headers
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Error al obtener categorías'}), 500
            
        categorias = response.json().get('categorias', {})
        
        if str(id_categoria) not in categorias:
            return jsonify({'subcategorias': []})
            
        return jsonify({
            'subcategorias': categorias[str(id_categoria)]['subcategorias']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500