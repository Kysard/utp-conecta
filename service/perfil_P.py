from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('perfil_P', __name__, url_prefix='/')

@bp.route('/perfil')
def vista_perfil():
    return render_template('perfil.html')
