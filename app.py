from flask import Flask

from service import agregarBlog_P, blog_P, chat_P, editarBlog_P, editarPerfil_P, iniciarSesion_P, inicio_P, registro_P, perfil_P, verBlog_P

app = Flask(__name__)
app.secret_key = 'clave-secreta-utp-conecta-2023' 

# Registrar blueprints
app.register_blueprint(iniciarSesion_P.bp)
app.register_blueprint(registro_P.bp)
app.register_blueprint(inicio_P.bp)
app.register_blueprint(perfil_P.bp)
app.register_blueprint(editarPerfil_P.bp)
app.register_blueprint(blog_P.bp)
app.register_blueprint(verBlog_P.bp)
app.register_blueprint(agregarBlog_P.bp)
app.register_blueprint(editarBlog_P.bp)
app.register_blueprint(chat_P.bp)


if __name__ == '__main__':
    app.run(debug=True)