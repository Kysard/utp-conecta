from flask import render_template, session
from flask import Blueprint, render_template

bp = Blueprint('agregarBlog_P', __name__, url_prefix='/')

@bp.route('/agregarBlog')
def vista_agregarBlog():
    user_data = session.get('user_data')
    return render_template('agregarBlog.html', user_data=user_data)
