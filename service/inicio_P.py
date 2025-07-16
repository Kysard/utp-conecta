from flask import Blueprint, redirect, render_template, session, url_for

bp = Blueprint('inicio_P', __name__, url_prefix='/')

@bp.route('inicio')
def vista_inicio():
    # Verificar si el usuario está autenticado
    if not session.get('autenticado'):
        return redirect(url_for('iniciarSesion_P.vista_iniciarSesion'))
    user_data = session.get('user_data')
    return render_template('inicio.html', user_data=user_data)