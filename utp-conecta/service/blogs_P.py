# # blogs_P.py
# from flask import render_template, session
# from flask import Blueprint, render_template

# bp = Blueprint('blog_P', __name__, url_prefix='/')

# @bp.route('blogs')
# def vista_blog():
#     user_data = session.get('user_data')
#     return render_template('blogs.html', user_data=user_data)



# <!-- blogs.html -->
# <!DOCTYPE html>
# <html lang="en">

# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Blog | UTP Conecta +</title>
#     {% include 'head.html' %}

# </head>

# <body>



#     <div class="main-wrapper">

#         {% include 'encabezado.html' %}
#         {% include 'barraLateral.html' %}

#         <div class="page-wrapper">
#             <div class="content container-fluid">
#                 <div class="page-header">
#                     <div class="row">
#                         <div class="col-lg-6 col-md-6 col-sm-6 col-12">
#                             <h5 class="text-uppercase mb-0 mt-0 page-title">Blog</h5>
#                         </div>
#                         <div class="col-lg-6 col-md-6 col-sm-6 col-12">
#                             <ul class="breadcrumb float-right p-0 mb-0">
#                                 <li class="breadcrumb-item"><a href="#"><i class="fas fa-home"></i> Home</a>
#                                 </li>
#                                 <li class="breadcrumb-item"><a href="#">Blog</a></li>
#                                 <li class="breadcrumb-item"><span> Blog</span></li>
#                             </ul>
#                         </div>
#                     </div>
#                 </div>
#                 <div class="row">
#                     <div class="col-lg-12 col-sm-12 col-12 text-right add-btn-col">
#                         <a class="btn btn-primary btn-rounded float-right" href="#"><i
#                                 class="fas fa-plus"></i> Add Blog</a>
#                     </div>
#                 </div>
#                 <div class="row">
#                     <div class="col-sm-6 col-md-6 col-lg-4">
#                         <div class="blog grid-blog">
#                             <div class="blog-image">
#                                 <a href="./templates/verBlog.html"><img class="img-fluid" src="assets/img/blog/blog-01.jpg"
#                                         alt=""></a>
#                             </div>
#                             <div class="blog-content">
#                                 <h3 class="blog-title"><a href="./templates/verBlog.html">Do You Know the ABCs School?</a></h3>
#                                 <p>Lorem ipsum dolor sit amet, consectetur em adipiscing elit, sed do eiusmod tempor
#                                     incididunt ut labore etmis dolore magna aliqua. Ut enim ad minim veniam, quis
#                                     noftrud exercitation ullamco sit laboris.</p>
#                                 <a href="./templates/verBlog.html" class="read-more"><i class="fas fa-long-arrow-alt-right"
#                                         aria-hidden="true"></i> Read More</a>
#                                 <div class="blog-info clearfix">
#                                     <div class="post-left">
#                                         <ul>
#                                             <li><a href="#"><i class="far fa-calendar-alt" aria-hidden="true"></i>
#                                                     <span>December 6, 2018</span></a></li>
#                                         </ul>
#                                     </div>
#                                     <div class="post-right"><a href="#"><i class="far fa-heart"
#                                                 aria-hidden="true"></i>21</a> <a href="#"><i class="fas fa-eye"
#                                                 aria-hidden="true"></i>8</a> <a href="#"><i class="fas fa-comment-o"
#                                                 aria-hidden="true"></i>17</a>
#                                     </div>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#             <div class="notification-box">
#                 <div class="msg-sidebar notifications msg-noti">
#                     <div class="topnav-dropdown-header">
#                         <span>Messages</span>
#                     </div>
#                     <div class="drop-scroll msg-list-scroll">
#                         <ul class="list-box">
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">R</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Richard Miles </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item new-message">
#                                         <div class="list-left">
#                                             <span class="avatar">J</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Ruth C. Gault</span>
#                                             <span class="message-time">1 Aug</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">T</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author"> Tarah Shropshire </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">M</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Mike Litorus</span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">C</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author"> Catherine Manseau </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">D</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author"> Domenic Houston </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">B</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author"> Buster Wigton </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">R</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author"> Rolland Webber </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">C</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author"> Claire Mapes </span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">M</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Melita Faucher</span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">J</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Jeffery Lalor</span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">L</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Loren Gatlin</span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                             <li>
#                                 <a href="chat.html">
#                                     <div class="list-item">
#                                         <div class="list-left">
#                                             <span class="avatar">T</span>
#                                         </div>
#                                         <div class="list-body">
#                                             <span class="message-author">Tarah Shropshire</span>
#                                             <span class="message-time">12:28 AM</span>
#                                             <div class="clearfix"></div>
#                                             <span class="message-content">Lorem ipsum dolor sit amet, consectetur
#                                                 adipiscing</span>
#                                         </div>
#                                     </div>
#                                 </a>
#                             </li>
#                         </ul>
#                     </div>
#                     <div class="topnav-dropdown-footer">
#                         <a href="chat.html">See all messages</a>
#                     </div>
#                 </div>
#             </div>
#         </div>

#     </div>



#     <script src="../static/js/jquery-3.6.0.min.js"></script>

#     <script src="../static/js/bootstrap.bundle.min.js"></script>

#     <script src="../static/js/jquery.slimscroll.js"></script>

#     <script src="../static/js/app.js"></script>

# </body>

# </html>


from flask import redirect, render_template, session, request, json
import requests
from flask import Blueprint, render_template

bp = Blueprint('blog_P', __name__, url_prefix='/')

@bp.route('blogs')
def vista_blog():
    user_data = session.get('user_data')
    token = session.get('token')
    
    if not user_data or not token:
        # Redirigir a login si no hay sesión
        return redirect('/login')
    
    # Obtener blogs del usuario actual
    id_usuario = user_data['IdUsuario']
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(
            f'http://127.0.0.1:8002/api/blog/blogs-usuario/{id_usuario}?estado=Activo',
            headers=headers
        )
        
        if response.status_code == 200:
            blogs = response.json()
        else:
            blogs = []
            print(f"Error al obtener blogs: {response.status_code}")
    except requests.exceptions.RequestException as e:
        blogs = []
        print(f"Error de conexión: {e}")
    
    return render_template('blogs.html', user_data=user_data, blogs=blogs)


