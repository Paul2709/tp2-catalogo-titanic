
"""Punto de entrada de la aplicacion del Titanic."""

import argparse

from src.fuentes import guardar_json, seleccionar_fuente
from src.pipeline import inspeccionar_datos, preparar_pasajeros


def construir_argumentos():
    """Definir las opciones de la terminal."""
    parser = argparse.ArgumentParser(
        description="Catalogo educativo de pasajeros del Titanic."
    )

    parser.add_argument(
        "--entrada",
        default="data/titanic.csv",
        help="Archivo de entrada CSV o JSON.",
    )

    parser.add_argument(
        "--exportar-json",
        help="Ruta para guardar una copia en JSON.",
    )

    return parser


def main():
    """Cargar, inspeccionar y validar los datos."""

    parser = construir_argumentos()
    opciones = parser.parse_args()

    try:
        fuente = seleccionar_fuente(opciones.entrada)

        registros = fuente.cargar(opciones.entrada)

        resumen = inspeccionar_datos(registros)

        pasajeros, rechazados = preparar_pasajeros(registros)

        if opciones.exportar_json:
            guardar_json(registros, opciones.exportar_json)

    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("CATALOGO DEL TITANIC - INSPECCION INICIAL")
    print(f"Archivo: {opciones.entrada}")

    print(f"Observaciones: {resumen['observaciones']}")
    print(f"Edades faltantes: {resumen['edades_faltantes']}")
    print(f"ID duplicados: {resumen['id_duplicados']}")
    print(f"Sobrevivientes registrados: {resumen['sobrevivientes_registrados']}")

    print(f"Pasajeros validos: {len(pasajeros)}")
    print(f"Registros rechazados: {len(rechazados)}")

    for rechazo in rechazados[:5]:
        print(
            f"Registro {rechazo['registro']}: "
            f"{rechazo['motivo']}"
        )

    if opciones.exportar_json:
        print(f"Archivo JSON creado: {opciones.exportar_json}")


if __name__ == "__main__":
    main()
