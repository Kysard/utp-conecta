from flask import Blueprint, render_template, session, redirect, url_for, request  # Añadido request
from functools import wraps

bp = Blueprint('inicio_P', __name__, url_prefix='/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('autenticado'):
            return redirect(url_for('iniciarSesion_P.vista_iniciarSesion', next=request.url))  # Usa request aquí
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/inicio')
@login_required
def vista_inicio():
    try:
        # Verificar y obtener datos de la sesión
        usuario_data = {
            'username': session.get('usuario'),
            'dni': session.get('dni', ''),
            'tipo_usuario': session.get('tipo_usuario', 'estudiante')
        }
        
        if not usuario_data['username']:
            session.clear()
            return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))
        
        return render_template('inicio.html', 
                            usuario=usuario_data['username'],
                            datos_usuario=usuario_data)
    
    except Exception as e:
        print(f"Error en vista_inicio: {str(e)}")
        return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))