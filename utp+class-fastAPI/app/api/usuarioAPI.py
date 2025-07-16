# app/api/usuarioAPI.py
import os
import uuid
from fastapi import APIRouter, File, Form, HTTPException, Depends, UploadFile
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from .conexion import get_db_connection  

router = APIRouter()

# Modelo Pydantic para validación de datos
class UsuarioRegistro(BaseModel):
    DNI: str
    Nombres: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Genero: str
    Usuario: str
    Contrasena: str


@router.post("/registrar")
async def registrar_usuario(usuario: UsuarioRegistro):
    """Endpoint para registrar un nuevo usuario"""
    try:
        # Validar género
        if usuario.Genero.upper() not in ['M', 'F', 'O']:
            raise HTTPException(
                status_code=400,
                detail="Género debe ser M (Masculino), F (Femenino) u O (Otro)"
            )

        # Validar DNI (8 dígitos)
        if not usuario.DNI.isdigit() or len(usuario.DNI) != 8:
            raise HTTPException(
                status_code=400,
                detail="DNI debe tener 8 dígitos numéricos"
            )

        # Obtener conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si DNI ya existe
        cursor.execute("SELECT DNI FROM Usuarios WHERE DNI = ?", usuario.DNI)
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="El DNI ya está registrado"
            )

        # Verificar si Usuario ya existe
        cursor.execute("SELECT Usuario FROM Usuarios WHERE Usuario = ?", usuario.Usuario)
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario ya está en uso"
            )

        # Insertar nuevo usuario (contraseña en texto plano)
        cursor.execute("""
            INSERT INTO Usuarios (
                DNI, Nombres, ApellidoPaterno, ApellidoMaterno, 
                Genero, Usuario, Contrasena
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario.DNI,
            usuario.Nombres,
            usuario.ApellidoPaterno,
            usuario.ApellidoMaterno,
            usuario.Genero.upper(),
            usuario.Usuario,
            usuario.Contrasena  # Se guarda directamente sin encriptar
        ))

        conn.commit()
        
        # Obtener el ID del nuevo usuario
        cursor.execute("SELECT SCOPE_IDENTITY()")
        id_usuario = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "message": "Usuario registrado exitosamente",
            "id_usuario": id_usuario
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar usuario: {str(e)}"
        )

@router.get("/consultar/{dni}")
async def consultar_usuario(dni: str):
    """Endpoint para consultar usuario por DNI"""
    try:
        # Validar DNI
        if not dni.isdigit() or len(dni) != 8:
            raise HTTPException(
                status_code=400,
                detail="DNI debe tener 8 dígitos numéricos"
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                DNI, Nombres, ApellidoPaterno, ApellidoMaterno,
                Genero, Usuario, FechaRegistro
            FROM Usuarios 
            WHERE DNI = ?
        """, dni)

        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "DNI": usuario.DNI,
            "Nombres": usuario.Nombres,
            "ApellidoPaterno": usuario.ApellidoPaterno,
            "ApellidoMaterno": usuario.ApellidoMaterno,
            "Genero": usuario.Genero,
            "Usuario": usuario.Usuario,
            "FechaRegistro": usuario.FechaRegistro.isoformat() if usuario.FechaRegistro else None
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar usuario: {str(e)}"
        )
    


class UsuarioActualizacion(BaseModel):
    Nombres: Optional[str] = None
    ApellidoPaterno: Optional[str] = None
    ApellidoMaterno: Optional[str] = None
    Genero: Optional[str] = None
    Telefono: Optional[str] = None
    Email: Optional[str] = None
    Direccion: Optional[str] = None
    FechaNacimiento: Optional[str] = None  # Mantenemos como string

@router.put("/actualizar/{dni}")
async def actualizar_usuario(dni: str, usuario_data: UsuarioActualizacion):
    """Endpoint para actualizar datos de un usuario existente"""
    try:
        # Validar DNI
        if not dni.isdigit() or len(dni) != 8:
            raise HTTPException(
                status_code=400,
                detail="DNI debe tener 8 dígitos numéricos"
            )
        
        # Validar género si se proporciona
        if usuario_data.Genero and usuario_data.Genero.upper() not in ['M', 'F', 'O']:
            raise HTTPException(
                status_code=400,
                detail="Género debe ser M (Masculino), F (Femenino) u O (Otro)"
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el usuario existe
        cursor.execute("SELECT IdUsuario FROM Usuarios WHERE DNI = ?", dni)
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Construir consulta SQL y parámetros
        update_fields = []
        params = []
        
        # Mapeo de campos a actualizar
        fields_mapping = {
            'Nombres': usuario_data.Nombres,
            'ApellidoPaterno': usuario_data.ApellidoPaterno,
            'ApellidoMaterno': usuario_data.ApellidoMaterno,
            'Genero': usuario_data.Genero.upper() if usuario_data.Genero else None,
            'Telefono': usuario_data.Telefono,
            'Email': usuario_data.Email,
            'Direccion': usuario_data.Direccion
        }

        # Procesar campos normales
        for field, value in fields_mapping.items():
            if value is not None:
                update_fields.append(f"{field} = ?")
                params.append(value)

        # Procesar FechaNacimiento por separado (manejo especial)
        if usuario_data.FechaNacimiento:
            try:
                # Convertir a formato datetime de SQL Server
                fecha_nac = datetime.strptime(usuario_data.FechaNacimiento, "%Y-%m-%d")
                update_fields.append("FechaNacimiento = ?")
                params.append(fecha_nac.strftime("%Y%m%d"))  # Formato compatible con SQL
            except ValueError:
                cursor.close()
                conn.close()
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha inválido. Use YYYY-MM-DD"
                )

        # Verificar email único si se está actualizando
        if usuario_data.Email:
            cursor.execute(
                "SELECT IdUsuario FROM Usuarios WHERE Email = ? AND DNI != ?",
                (usuario_data.Email, dni)
            )
            if cursor.fetchone():
                cursor.close()
                conn.close()
                raise HTTPException(
                    status_code=400,
                    detail="El correo electrónico ya está en uso por otro usuario"
                )

        if not update_fields:
            cursor.close()
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="No se proporcionaron datos para actualizar"
            )

        # Construir y ejecutar consulta final
        sql = f"UPDATE Usuarios SET {', '.join(update_fields)} WHERE DNI = ?"
        params.append(dni)

        try:
            cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error de base de datos al actualizar: {str(e)}"
            )
        finally:
            cursor.close()
            conn.close()

        return {
            "status": "success",
            "message": "Usuario actualizado exitosamente",
            "dni": dni
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al actualizar usuario: {str(e)}"
        )