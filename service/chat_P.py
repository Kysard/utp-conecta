from flask import render_template, session
from flask import Blueprint, render_template

bp = Blueprint('chat_P', __name__, url_prefix='/')

@bp.route('/chat')
def vista_chat():
    user_data = session.get('user_data')
    return render_template('chat.html', user_data=user_data)
