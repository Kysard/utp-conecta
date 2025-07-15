from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('agregarBlog_P', __name__, url_prefix='/')

@bp.route('/agregarBlog')
def vista_agregarBlog():
    return render_template('agregarBlog.html')
