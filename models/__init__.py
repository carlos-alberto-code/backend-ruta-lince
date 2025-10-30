"""
Módulo de modelos de base de datos.

Este módulo exporta todos los modelos SQLModel para facilitar los imports
en otros módulos de la aplicación.

Uso:
    from models import User, UserCreate, UserPublic
"""

from models.user import User, UserCreate, UserPublic, UserUpdate, UserWithPassword

# Exportar todos los modelos
__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UserWithPassword",
]

# Nota: Cuando agregues más modelos (ej. Token, Product, etc.),
# impórtalos aquí y agrégalos a __all__
