from flask import Blueprint, render_template, request, jsonify
from zeep import Client
import requests

bp = Blueprint('registro_P', __name__, url_prefix='/')

# Ruta para mostrar el formulario y procesar el registro
@bp.route('/registro', methods=['GET', 'POST'])
def vista_registro():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario 
            dni = request.form['dni']
            nombres = request.form['nombres']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            sexo = request.form['sexo']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']

            # Consumir el servicio SOAP 
            wsdl = 'http://localhost:8000/?wsdl'
            client = Client(wsdl=wsdl)
            resultado = client.service.registrar_usuario(
                dni, nombres, apellido_paterno,
                apellido_materno, sexo, usuario, contrasena
            )

            return render_template('iniciarSesion.html', mensaje=resultado)

        except Exception as e:
            return render_template('registro.html', error=f"Error: {str(e)}")

    return render_template('registro.html')


# Ruta para consultar el DNI
@bp.route('/consultar_dni', methods=['POST'])
def consultar_dni():
    try:
        data = request.get_json()
        dni = data.get('dni', '').strip()

        if not dni or len(dni) != 8 or not dni.isdigit():
            return jsonify({'success': False, 'error': 'DNI inválido'}), 400

        # Llamada a API externa de DNI
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
        sexo_formateado = 'Masculino' if sexo_raw == 'M' else 'Femenino' if sexo_raw == 'F' else ''

        formatted_data = {
            'dni': dni,
            'nombres': datos.get('nombres', ''),
            'apellido_paterno': datos.get('apellido_paterno', ''),
            'apellido_materno': datos.get('apellido_materno', ''),
            'sexo': sexo_formateado
        }

        return jsonify({'success': True, 'data': formatted_data})

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Error al conectar con RENIEC: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error del servidor: {str(e)}'}), 500

