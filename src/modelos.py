
import math
import re


class Pasajero:
    """Representa un pasajero del Titanic."""

    PATRON_BILLETE = r"[A-Za-z0-9][A-Za-z0-9 ./-]*"

    def __init__(self, registro):
        try:
            self.identificador = int(registro["PassengerId"])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("El ID debe ser un numero entero.") from error

        if self.identificador <= 0:
            raise ValueError("El ID debe ser positivo.")

        self.nombre = str(registro.get("Name") or "").strip()
        self.billete = str(registro.get("Ticket") or "").strip()

        if not self.nombre:
            raise ValueError("El nombre no puede estar vacio.")

        if not re.fullmatch(self.PATRON_BILLETE, self.billete):
            raise ValueError("El formato del billete es invalido.")

        clase = str(registro.get("Pclass", "")).strip()

        if clase not in ("1", "2", "3"):
            raise ValueError("La clase debe ser 1, 2 o 3.")

        self.clase = int(clase)

        supervivencia = str(registro.get("Survived", "")).strip()

        if supervivencia not in ("0", "1"):
            raise ValueError("La supervivencia debe ser 0 o 1.")

        self.sobrevivio = int(supervivencia)

        edad = registro.get("Age")

        if edad is None or str(edad).strip() == "":
            self.edad = None
        else:
            try:
                self.edad = float(edad)
            except (TypeError, ValueError) as error:
                raise ValueError("La edad debe ser numerica.") from error

            if not math.isfinite(self.edad) or not 0 <= self.edad <= 120:
                raise ValueError("La edad esta fuera del rango permitido.")

    def grupo_edad(self):
        """Determina el grupo de edad del pasajero."""
        if self.edad is None:
            return "Edad desconocida"

        if self.edad < 18:
            return "Menor"

        if self.edad < 60:
            return "Adulto"

        return "Adulto mayor"

    def ficha(self):
        """Devuelve la informacion del pasajero."""
        return {
            "PassengerId": self.identificador,
            "Name": self.nombre,
            "Ticket": self.billete,
            "Pclass": self.clase,
            "Age": self.edad,
            "Survived": self.sobrevivio,
            "GrupoEdad": self.grupo_edad(),
        }
