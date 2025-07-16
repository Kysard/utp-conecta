from flask import Blueprint, render_template, request, jsonify
import requests

bp = Blueprint('registro_P', __name__, url_prefix='/')

# Configuración de la API
FASTAPI_URL = "http://localhost:8002/api/registro"  

# Ruta para mostrar el formulario y procesar el registro
@bp.route('/registro', methods=['GET', 'POST'])
def vista_registro():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario 
            data = {
                "DNI": request.form['dni'],
                "Nombres": request.form['nombres'],
                "ApellidoPaterno": request.form['apellido_paterno'],
                "ApellidoMaterno": request.form['apellido_materno'],
                "Genero": request.form['sexo'],
                "Usuario": request.form['usuario'],
                "Contrasena": request.form['contrasena']
            }

            # Consumir la API FastAPI
            response = requests.post(
                f"{FASTAPI_URL}/registrar",
                json=data
            )

            # Verificar si hubo error
            if response.status_code != 200:
                error_data = response.json()
                return render_template('registro.html', error=error_data.get("detail", "Error al registrar usuario"))

            # Si todo fue bien
            resultado = response.json()
            return render_template('iniciarSesion.html', mensaje=resultado["message"])

        except Exception as e:
            return render_template('registro.html', error=f"Error: {str(e)}")

    return render_template('registro.html')


# Ruta para consultar el DNI (combinando tu API y RENIEC)
@bp.route('/consultar_dni', methods=['POST'])
def consultar_dni():
    try:
        data = request.get_json()
        dni = data.get('dni', '').strip()

        if not dni or len(dni) != 8 or not dni.isdigit():
            return jsonify({'success': False, 'error': 'DNI inválido'}), 400

        # Primero verificar si el DNI ya está registrado en tu sistema
        try:
            response = requests.get(f"{FASTAPI_URL}/consultar/{dni}")
            if response.status_code == 200:
                return jsonify({
                    'success': False, 
                    'error': 'Este DNI ya está registrado en nuestro sistema'
                }), 400
        except:
            pass  # Si hay error al conectar con la API, continuamos con RENIEC

        # Llamada a API externa de DNI (RENIEC)
        TOKEN = "avaloshua_dhvvcg2502"
        url = f"http://go.net.pe:3000/api/v2/dni/{dni}"
        headers = {'Authorization': f'Bearer {TOKEN}'}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        api_data = response.json()

        if 'data' not in api_data or not api_data['data']:
            return jsonify({'success': False, 'error': 'DNI no encontrado'}), 404

        datos = api_data['data']
        sexo_raw = datos.get('sexo', '').upper()
        sexo_formateado = 'M' if sexo_raw == 'M' else 'F' if sexo_raw == 'F' else 'O'

        formatted_data = {
            'dni': dni,
            'nombres': datos.get('nombres', ''),
            'apellido_paterno': datos.get('apellido_paterno', ''),
            'apellido_materno': datos.get('apellido_materno', ''),
            'sexo': sexo_formateado  # Ahora en formato compatible con tu API (M/F/O)
        }

        return jsonify({'success': True, 'data': formatted_data})

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Error al conectar con RENIEC: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error del servidor: {str(e)}'}), 500