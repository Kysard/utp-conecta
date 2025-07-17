from fastapi import APIRouter, HTTPException, Response, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta
from .conexion import get_db_connection

router = APIRouter()
security = HTTPBasic()

# Almacenamiento de sesiones mejorado
sesiones_activas = {}

class UsuarioLogin(BaseModel):
    usuario: str
    contrasena: str

class SesionData(BaseModel):
    id_usuario: int
    usuario: str
    expiracion: datetime

def crear_token_sesion():
    return secrets.token_urlsafe(32)

def obtener_sesion_id(request: Request):
    # Primero intenta obtener de cookies (para navegador)
    sesion_id = request.cookies.get("session_id")
    # Si no está en cookies, intenta obtener del header (para Swagger/Postman)
    if not sesion_id:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            sesion_id = auth_header.split(" ")[1]
    return sesion_id

async def verificar_sesion(request: Request):
    sesion_id = obtener_sesion_id(request)
    
    if not sesion_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    sesion = sesiones_activas.get(sesion_id)
    if not sesion:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada"
        )
    
    if datetime.now() > sesion.expiracion:
        del sesiones_activas[sesion_id]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión expirada"
        )
    
    return sesion

@router.post("/login")
async def iniciar_sesion(
    credenciales: UsuarioLogin,
    response: Response
):
    """Endpoint para iniciar sesión"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT IdUsuario, DNI, Nombres, ApellidoPaterno, ApellidoMaterno, 
               Genero, TipoUsuario, Usuario, Telefono, Email, Direccion, 
               FechaNacimiento, FotoPerfil, FechaRegistro
        FROM Usuarios 
        WHERE Usuario = ? AND Contrasena = ? AND Activo = 1
    """, (credenciales.usuario, credenciales.contrasena))
    
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Crear sesión con tiempo de expiración (1 hora)
    sesion_id = crear_token_sesion()
    expiracion = datetime.now() + timedelta(hours=1)
    
    sesiones_activas[sesion_id] = SesionData(
        id_usuario=usuario.IdUsuario,
        usuario=usuario.Usuario,
        expiracion=expiracion
    )
    
    # Configurar cookie HTTP-only para seguridad
    response.set_cookie(
        key="session_id",
        value=sesion_id,
        httponly=True,
        max_age=3600,  # 1 hora en segundos
        secure=False,   # Cambiar a True en producción con HTTPS
        samesite="lax"
    )

    # Convertir fechas a string solo si existen y son objetos datetime
    fecha_nacimiento = usuario.FechaNacimiento
    if isinstance(fecha_nacimiento, datetime):
        fecha_nacimiento = fecha_nacimiento.isoformat()
    elif fecha_nacimiento is not None:
        # Si ya es un string, dejarlo como está
        pass
    
    fecha_registro = usuario.FechaRegistro
    if isinstance(fecha_registro, datetime):
        fecha_registro = fecha_registro.isoformat()
    elif fecha_registro is not None:
        # Si ya es un string, dejarlo como está
        pass

    return {
        "mensaje": "Sesión iniciada",
        "token": sesion_id,
        "usuario_data": {
            "IdUsuario": usuario.IdUsuario,
            "DNI": usuario.DNI,
            "Nombres": usuario.Nombres,
            "ApellidoPaterno": usuario.ApellidoPaterno,
            "ApellidoMaterno": usuario.ApellidoMaterno,
            "Genero": usuario.Genero,
            "TipoUsuario": usuario.TipoUsuario,
            "Usuario": usuario.Usuario,
            "Telefono": usuario.Telefono,
            "Email": usuario.Email,
            "Direccion": usuario.Direccion,
            "FechaNacimiento": fecha_nacimiento,
            "FotoPerfil": usuario.FotoPerfil,
            "FechaRegistro": fecha_registro
        }
    }

@router.post("/logout")
async def cerrar_sesion(
    request: Request,
    response: Response
):
    """Endpoint para cerrar sesión"""
    sesion_id = obtener_sesion_id(request)
    
    if not sesion_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay sesión activa"
        )
    
    if sesion_id in sesiones_activas:
        del sesiones_activas[sesion_id]
    
    # Eliminar la cookie
    response.delete_cookie("session_id")
    
    return {"mensaje": "Sesión cerrada"}

@router.get("/verificar-sesion")
async def verificar_sesion_activa(
    request: Request
):
    """Endpoint para verificar si la sesión es válida"""
    try:
        sesion = await verificar_sesion(request)
        return {
            "autenticado": True,
            "usuario": sesion.usuario
        }
    except HTTPException:
        return {
            "autenticado": False,
            "usuario": None
        }