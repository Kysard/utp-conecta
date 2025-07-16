from flask import render_template, session
from flask import Blueprint, render_template

bp = Blueprint('blog_P', __name__, url_prefix='/')

@bp.route('/blog')
def vista_blog():
    user_data = session.get('user_data')
    return render_template('blog.html', user_data=user_data)
