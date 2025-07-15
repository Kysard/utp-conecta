from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('verBlog_P', __name__, url_prefix='/')

@bp.route('/verBlog')
def vista_verBlog():
    return render_template('verBlog.html')
