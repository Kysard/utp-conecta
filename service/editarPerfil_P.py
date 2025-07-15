from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('editarPerfil_P', __name__, url_prefix='/')

@bp.route('/editarPerfil')
def vista_editarPerfil():
    return render_template('editarPerfil.html')
