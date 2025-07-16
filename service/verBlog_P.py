from flask import render_template, session
from flask import Blueprint, render_template

bp = Blueprint('verBlog_P', __name__, url_prefix='/')

@bp.route('/verBlog')
def vista_verBlog():
    user_data = session.get('user_data')
    return render_template('verBlog.html', user_data=user_data)
