from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import logging

bp = Blueprint('iniciarSesion_P', __name__, url_prefix='/')

# Configuración de la API REST
API_BASE_URL = "http://localhost:8002"  # Ajusta esta URL según donde esté alojada tu API
LOGIN_ENDPOINT = "/api/login/login"
TIMEOUT = 10

@bp.route('/', methods=['GET', 'POST'])
def vista_iniciarSesion():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        contraseña = request.form.get('contraseña', '').strip()
        
        if not usuario or not contraseña:
            flash('Usuario y contraseña son requeridos', 'error')
            return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))
        
        try:
            # Preparar los datos para la API
            payload = {
                "usuario": usuario,
                "contrasena": contraseña
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Hacer la petición a la API
            response = requests.post(
                f"{API_BASE_URL}{LOGIN_ENDPOINT}",
                json=payload,
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                # Si la API devuelve un mensaje de éxito (ajusta según lo que devuelva tu API)
                session['autenticado'] = True
                session['usuario'] = usuario
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('inicio_P.vista_inicio'))
            elif response.status_code == 422:
                flash('Datos de inicio de sesión inválidos', 'error')
            else:
                flash('Credenciales incorrectas', 'error')
            
        except requests.exceptions.RequestException as e:
            flash('El servicio de autenticación no está disponible', 'error')
            logging.error(f"Error de conexión: {e}")
        except Exception as e:
            flash('Error inesperado al iniciar sesión', 'error')
            logging.error(f"Error inesperado: {e}")
    
    return render_template('iniciarSesion.html')

@bp.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))