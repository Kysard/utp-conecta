from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('blog_P', __name__, url_prefix='/')

@bp.route('/blog')
def vista_blog():
    return render_template('blog.html')
