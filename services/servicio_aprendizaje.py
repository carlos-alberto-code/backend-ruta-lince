from schemas.aprendizaje import DatosAprendizaje


class ServicioAprendizaje:

    @classmethod
    def obtener_datos(cls) -> DatosAprendizaje:
        ...
