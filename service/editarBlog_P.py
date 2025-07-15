from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('editarBlog_P', __name__, url_prefix='/')

@bp.route('/editarBlog')
def vista_editarBlog():
    return render_template('editarBlog.html')
