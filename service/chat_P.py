from flask import render_template
from flask import Blueprint, render_template

bp = Blueprint('chat_P', __name__, url_prefix='/')

@bp.route('/chat')
def vista_chat():
    return render_template('chat.html')
