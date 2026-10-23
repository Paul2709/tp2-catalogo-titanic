"""Inspeccion y validacion preliminar del conjunto de datos."""

from src.modelos import Pasajero

COLUMNAS_OBLIGATORIAS = {
    "PassengerId",
    "Name",
    "Ticket",
    "Pclass",
    "Age",
    "Survived",
}


def validar_esquema(registros):
    """Revisar que cada registro incluya los campos necesarios."""
    if not registros:
        raise ValueError("El archivo no contiene observaciones.")

    for numero, registro in enumerate(registros, start=1):
        faltantes = COLUMNAS_OBLIGATORIAS - registro.keys()
        if faltantes:
            columnas = ", ".join(sorted(faltantes))
            raise ValueError(
                f"El registro {numero} no contiene las columnas: {columnas}."
            )


def inspeccionar_datos(registros):
    """Contar observaciones, edades vacias y los ID duplicados."""
    validar_esquema(registros)

    identificadores = [registro["PassengerId"] for registro in registros]
    edades_faltantes = sum(registro["Age"] is None for registro in registros)
    identificadores_duplicados = len(identificadores) - len(set(identificadores))
    sobrevivientes = sum(registro["Survived"] == "1" for registro in registros)

    return {
        "observaciones": len(registros),
        "edades_faltantes": edades_faltantes,
        "id_duplicados": identificadores_duplicados,
        "sobrevivientes_registrados": sobrevivientes,
    }

def preparar_pasajeros(registros):
    """Separar pasajeros validos y registros rechazados."""
    validar_esquema(registros)

    pasajeros = []
    rechazados = []
    identificadores = set()

    for numero, registro in enumerate(registros, start=1):
        try:
            pasajero = Pasajero(registro)

            if pasajero.identificador in identificadores:
                raise ValueError("El ID del pasajero esta duplicado.")

        except ValueError as error:
            rechazados.append({
                "registro": numero,
                "identificador": registro.get("PassengerId"),
                "motivo": str(error),
            })
            continue

        identificadores.add(pasajero.identificador)
        pasajeros.append(pasajero)

    return pasajeros, rechazados
