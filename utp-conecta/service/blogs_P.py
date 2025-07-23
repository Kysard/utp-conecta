from flask import redirect, render_template, session, request, json
import requests
from flask import Blueprint, render_template

bp = Blueprint('blog_P', __name__, url_prefix='/')

@bp.route('blogs')
def vista_blog():
    user_data = session.get('user_data')
    token = session.get('token')
    
    if not user_data or not token:
        # Redirigir a login si no hay sesión
        return redirect('/login')
    
    # Obtener blogs del usuario actual
    id_usuario = user_data['IdUsuario']
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(
            f'http://127.0.0.1:8002/api/blog/blogs-usuario/{id_usuario}?estado=Activo',
            headers=headers
        )
        
        if response.status_code == 200:
            blogs = response.json()
        else:
            blogs = []
            print(f"Error al obtener blogs: {response.status_code}")
    except requests.exceptions.RequestException as e:
        blogs = []
        print(f"Error de conexión: {e}")
    
    return render_template('blogs.html', user_data=user_data, blogs=blogs)


