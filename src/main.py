"""Punto de entrada: lee, inspecciona y opcionalmente exporta datos."""

import argparse

from src.fuentes import guardar_json, seleccionar_fuente
from src.pipeline import inspeccionar_datos


def construir_argumentos():
    """Definir opciones que puede ingresar el usuario en la terminal."""
    parser = argparse.ArgumentParser(
        description="Catalogo educativo de pasajeros del Titanic (avance inicial)."
    )
    parser.add_argument(
        "--entrada",
        default="data/titanic.csv",
        help="Archivo de entrada CSV o JSON.",
    )
    parser.add_argument(
        "--exportar-json",
        help="Ruta para guardar una copia equivalente en JSON.",
    )
    return parser


def main():
    """Coordinar la carga, la inspeccion y la exportacion opcional."""
    parser = construir_argumentos()
    opciones = parser.parse_args()

    try:
        fuente = seleccionar_fuente(opciones.entrada)
        registros = fuente.cargar(opciones.entrada)
        resumen = inspeccionar_datos(registros)
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
    if opciones.exportar_json:
        print(f"Archivo JSON creado: {opciones.exportar_json}")


if __name__ == "__main__":
    main()
