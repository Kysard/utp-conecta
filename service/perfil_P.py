from flask import render_template, session
from flask import Blueprint, render_template

bp = Blueprint('perfil_P', __name__, url_prefix='/')

@bp.route('/perfil')
def vista_perfil():
    user_data = session.get('user_data')
    return render_template('perfil.html', user_data=user_data)
