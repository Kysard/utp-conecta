from flask import render_template, session
from flask import Blueprint, render_template

bp = Blueprint('editarBlog_P', __name__, url_prefix='/')

@bp.route('/editarBlog')
def vista_editarBlog():
    user_data = session.get('user_data')
    return render_template('editarBlog.html', user_data=user_data)
