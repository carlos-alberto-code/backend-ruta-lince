from src.models import Usuario
from src.database.repository import create
from src.services.login_service import hashear_contrasena


def crear_usuario(nombre: str, apellidos: str, email: str, password: str) -> Usuario:
    usuario = Usuario(
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        contrasena_hash=hashear_contrasena(password),
    )
    return create(usuario)


nombre = "Carlos Alberto"
apellidos = "Baltazar Hinojosa"
email = "A840159943@my.uvm.edu.mx"
password = "123"
try:
    crear_usuario(nombre, apellidos, email, password)
    print("Usuario creado exitosamente.")
except Exception as e:
    print(f"Error al crear el usuario: {e}")
