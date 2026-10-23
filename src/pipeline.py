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

def indexar_pasajeros(pasajeros):
    """Organizar pasajeros por identificador."""
    indice = {}

    for pasajero in pasajeros:
        identificador = pasajero.identificador

        if identificador in indice:
            raise ValueError("El ID del pasajero esta duplicado.")

        indice[identificador] = pasajero

    return indice


def buscar_pasajero(indice, identificador):
    """Buscar un pasajero utilizando su ID."""
    return indice.get(identificador)


def filtrar_grupo(pasajeros, clase=None, grupo_edad=None):
    """Seleccionar pasajeros por clase y grupo de edad."""

    if clase is not None and clase not in (1, 2, 3):
        raise ValueError("La clase debe ser 1, 2 o 3.")

    grupos_validos = (
        "Menor",
        "Adulto",
        "Adulto mayor",
        "Edad desconocida",
    )

    if grupo_edad is not None and grupo_edad not in grupos_validos:
        raise ValueError("El grupo de edad no es valido.")

    seleccionados = []

    for pasajero in pasajeros:
        if clase is not None and pasajero.clase != clase:
            continue

        if (
            grupo_edad is not None
            and pasajero.grupo_edad() != grupo_edad
        ):
            continue

        seleccionados.append(pasajero)

    return seleccionados
