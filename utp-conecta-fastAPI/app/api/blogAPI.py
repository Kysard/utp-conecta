from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Optional
from .conexion import get_db_connection
import pyodbc
import os
from datetime import datetime
import uuid
from fastapi.responses import JSONResponse

router = APIRouter()

# Configuración para archivos
UPLOAD_DIR = "static/uploads/blogs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_IMAGES = 10
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

@router.post("/crear-blog", status_code=status.HTTP_201_CREATED)
async def crear_blog_completo(
    titulo: str = Form(..., min_length=5, max_length=255),
    contenido: str = Form(..., min_length=10),
    id_usuario: int = Form(...),
    id_categoria: int = Form(...),
    id_subcategoria: int = Form(...),
    estado: str = Form("Activo"),
    imagenes: List[UploadFile] = File(default=[]),
    conn = Depends(get_db_connection)
):
    # Validación básica de imágenes
    if len(imagenes) > MAX_IMAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No puedes subir más de {MAX_IMAGES} imágenes"
        )

    cursor = conn.cursor()
    try:
        # 1. Crear el post del blog
        cursor.execute(
            """INSERT INTO BlogPosts 
            (IdUsuario, Titulo, Contenido, Estado, FechaPublicacion) 
            OUTPUT INSERTED.IdPost 
            VALUES (?, ?, ?, ?, GETDATE())""",
            (id_usuario, titulo, contenido, estado)
        )
        id_post = cursor.fetchone()[0]

        # 2. Asociar categorías
        cursor.execute(
            "INSERT INTO PostCategorias (IdPost, IdSubcategoria) VALUES (?, ?)",
            (id_post, id_subcategoria)
        )

        # 3. Procesar imágenes
        uploaded_images = []
        for img in imagenes:
            # Validar tipo de imagen
            if img.content_type not in ALLOWED_IMAGE_TYPES:
                continue

            # Validar tamaño
            img_data = await img.read()
            if len(img_data) > MAX_FILE_SIZE:
                continue

            # Generar nombre único
            file_ext = img.filename.split('.')[-1]
            unique_name = f"{uuid.uuid4()}.{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_name)

            # Guardar archivo
            with open(file_path, "wb") as buffer:
                buffer.write(img_data)

            # Registrar en base de datos
            cursor.execute(
                """INSERT INTO Multimedia 
                (IdPost, Tipo, RutaArchivo, NombreOriginal, Tamano) 
                VALUES (?, 'Imagen', ?, ?, ?)""",
                (id_post, f"/{file_path}", img.filename, len(img_data))
            )
            uploaded_images.append({
                "nombre": img.filename,
                "ruta": f"/{file_path}",
                "tamaño": len(img_data)
            })

        conn.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Blog creado exitosamente",
                "post_id": id_post,
                "imagenes_subidas": uploaded_images,
                "total_imagenes": len(uploaded_images)
            }
        )

    except pyodbc.Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()

@router.get("/categorias-subcategorias")
async def obtener_categorias_completas(conn = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        # Obtener todas las categorías con sus subcategorías
        cursor.execute("""
            SELECT c.IdCategoria, c.Nombre as Categoria, c.Icono,
                   s.IdSubcategoria, s.Nombre as Subcategoria
            FROM Categorias c
            LEFT JOIN Subcategorias s ON c.IdCategoria = s.IdCategoria
            ORDER BY c.IdCategoria, s.IdSubcategoria
        """)
        
        categorias = {}
        for row in cursor.fetchall():
            if row.IdCategoria not in categorias:
                categorias[row.IdCategoria] = {
                    "nombre": row.Categoria,
                    "icono": row.Icono,
                    "subcategorias": []
                }
            if row.IdSubcategoria:
                categorias[row.IdCategoria]["subcategorias"].append({
                    "id": row.IdSubcategoria,
                    "nombre": row.Subcategoria
                })
        
        return {"categorias": categorias}
    
    except pyodbc.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()

@router.get("/blogs-usuario/{id_usuario}", response_model=List[dict])
async def obtener_blogs_usuario(
    id_usuario: int,
    estado: Optional[str] = None,
    conn = Depends(get_db_connection)
):
    cursor = conn.cursor()
    try:
        # Consulta base para obtener los posts del usuario
        query = """
            SELECT 
                bp.IdPost, bp.Titulo, bp.Contenido, 
                bp.FechaPublicacion, bp.FechaActualizacion,
                bp.Estado, bp.Visitas,
                u.IdUsuario, u.Nombres, u.ApellidoPaterno, u.ApellidoMaterno,
                u.FotoPerfil, u.TipoUsuario
            FROM BlogPosts bp
            JOIN Usuarios u ON bp.IdUsuario = u.IdUsuario
            WHERE bp.IdUsuario = ?
        """
        
        params = [id_usuario]
        
        # Filtrar por estado si se proporciona
        if estado:
            query += " AND bp.Estado = ?"
            params.append(estado)
        
        query += " ORDER BY bp.FechaPublicacion DESC"
        
        cursor.execute(query, params)
        posts = cursor.fetchall()
        
        if not posts:
            return []
        
        # Estructura para almacenar los resultados
        resultados = []
        
        for post in posts:
            # Obtener categorías y subcategorías para cada post
            cursor.execute("""
                SELECT 
                    c.IdCategoria, c.Nombre AS Categoria, c.Icono,
                    sc.IdSubcategoria, sc.Nombre AS Subcategoria
                FROM PostCategorias pc
                JOIN Subcategorias sc ON pc.IdSubcategoria = sc.IdSubcategoria
                JOIN Categorias c ON sc.IdCategoria = c.IdCategoria
                WHERE pc.IdPost = ?
            """, (post.IdPost,))
            
            categorias = []
            for cat in cursor.fetchall():
                categorias.append({
                    "id_categoria": cat.IdCategoria,
                    "categoria": cat.Categoria,
                    "icono": cat.Icono,
                    "id_subcategoria": cat.IdSubcategoria,
                    "subcategoria": cat.Subcategoria
                })
            
            # Obtener multimedia para cada post
            cursor.execute("""
                SELECT 
                    IdMultimedia, Tipo, RutaArchivo, 
                    NombreOriginal, Tamano, FechaSubida, Orden
                FROM Multimedia
                WHERE IdPost = ?
                ORDER BY Orden
            """, (post.IdPost,))
            
            multimedia = []
            for media in cursor.fetchall():
                multimedia.append({
                    "id": media.IdMultimedia,
                    "tipo": media.Tipo,
                    "ruta": media.RutaArchivo,
                    "nombre_original": media.NombreOriginal,
                    "tamano": media.Tamano,
                    "fecha_subida": media.FechaSubida,
                    "orden": media.Orden
                })
            
            # Construir el objeto del post
            post_data = {
                "id_post": post.IdPost,
                "titulo": post.Titulo,
                "contenido": post.Contenido,
                "fecha_publicacion": post.FechaPublicacion,
                "fecha_actualizacion": post.FechaActualizacion,
                "estado": post.Estado,
                "visitas": post.Visitas,
                "usuario": {
                    "id": post.IdUsuario,
                    "nombres": post.Nombres,
                    "apellido_paterno": post.ApellidoPaterno,
                    "apellido_materno": post.ApellidoMaterno,
                    "foto_perfil": post.FotoPerfil,
                    "tipo_usuario": post.TipoUsuario
                },
                "categorias": categorias,
                "multimedia": multimedia
            }
            
            resultados.append(post_data)
        
        return resultados
    
    except pyodbc.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()