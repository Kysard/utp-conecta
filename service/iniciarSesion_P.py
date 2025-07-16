from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import logging

bp = Blueprint('iniciarSesion_P', __name__, url_prefix='/')

# Configuración de la API
API_URL = "http://localhost:8002/api/auth/login"
TIMEOUT = 5  # segundos

@bp.route('/', methods=['GET', 'POST'])
def vista_iniciarSesion():
    if request.method == 'POST':
        # Obtener datos del formulario
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contraseña')  
        
        # Validación simple
        if not usuario or not contrasena:
            flash('Por favor ingrese usuario y contraseña', 'error')
            return render_template('iniciarSesion.html')
        
        try:
            # Hacer petición a la API FastAPI
            response = requests.post(
                API_URL,
                json={
                    "usuario": usuario,
                    "contrasena": contrasena
                },
                timeout=TIMEOUT
            )
            
            # Procesar respuesta
            if response.status_code == 200:
                datos = response.json()
                
                # Verificar si la API devuelve los datos esperados
                if 'usuario_data' not in datos:
                    flash('Error en los datos recibidos del servidor', 'error')
                    return render_template('iniciarSesion.html')
                
                # Almacenar datos en la sesión
                session['user_data'] = datos['usuario_data']
                session['token'] = datos['token']
                session['autenticado'] = True
                
                # Mensaje de bienvenida personalizado
                nombres = datos['usuario_data']['Nombres']
                apellido_paterno = datos['usuario_data']['ApellidoPaterno']
                flash(f'Bienvenido {nombres} {apellido_paterno}!', 'success')
                return redirect(url_for('inicio_P.vista_inicio'))

            else:
                error_msg = response.json().get('detail', 'Credenciales incorrectas')
                flash(error_msg, 'error')
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error de conexión: {e}")
            flash('Error al conectar con el servidor. Intente nuevamente.', 'error')
    
    return render_template('iniciarSesion.html')

@bp.route('/logout')
def cerrar_sesion():
    # Verificar si hay una sesión activa
    if 'token' in session:
        try:
            # Llamar al endpoint de logout de la API
            response = requests.post(
                "http://localhost:8002/api/auth/logout",
                headers={"Authorization": f"Bearer {session['token']}"},
                timeout=TIMEOUT
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al cerrar sesión: {e}")
    
    # Limpiar la sesión de Flask
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))