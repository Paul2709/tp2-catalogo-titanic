
"""Punto de entrada de la aplicacion del Titanic."""

import argparse

from src.fuentes import guardar_json, seleccionar_fuente
from src.pipeline import (
    buscar_pasajero,
    filtrar_grupo,
    indexar_pasajeros,
    inspeccionar_datos,
    preparar_pasajeros,
)


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

    parser.add_argument(
        "--buscar-id",
        type=int,
        help="Identificador del pasajero que desea buscar.",
    )

    parser.add_argument(
        "--clase",
        type=int,
        choices=[1, 2, 3],
        help="Filtrar pasajeros por clase.",
    )

    parser.add_argument(
        "--grupo-edad",
        choices=[
            "Menor",
            "Adulto",
            "Adulto mayor",
            "Edad desconocida",
        ],
        help="Filtrar pasajeros por grupo de edad.",
    )

    return parser


def main():
    """Cargar datos y ejecutar las consultas solicitadas."""
    parser = construir_argumentos()
    opciones = parser.parse_args()

    if opciones.buscar_id is not None:
        if opciones.clase is not None or opciones.grupo_edad is not None:
            parser.error(
                "No combine --buscar-id con los filtros de grupo."
            )

    try:
        fuente = seleccionar_fuente(opciones.entrada)
        registros = fuente.cargar(opciones.entrada)

        resumen = inspeccionar_datos(registros)
        pasajeros, rechazados = preparar_pasajeros(registros)
        indice = indexar_pasajeros(pasajeros)

        if opciones.exportar_json:
            guardar_json(registros, opciones.exportar_json)

    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("CATALOGO DE PASAJEROS DEL TITANIC")
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

    if opciones.buscar_id is not None:
        pasajero = buscar_pasajero(indice, opciones.buscar_id)

        print("\nRESULTADO DE LA BUSQUEDA")

        if pasajero is None:
            print("No se encontro el pasajero solicitado.")
        else:
            for campo, valor in pasajero.ficha().items():
                print(f"{campo}: {valor}")

    elif opciones.clase is not None or opciones.grupo_edad is not None:
        seleccionados = filtrar_grupo(
            pasajeros,
            clase=opciones.clase,
            grupo_edad=opciones.grupo_edad,
        )

        print("\nRESULTADO DEL FILTRO")
        print(f"Pasajeros encontrados: {len(seleccionados)}")

        if not seleccionados:
            print("No se encontraron pasajeros para estos filtros.")

        for pasajero in seleccionados[:10]:
            print(
                f"ID: {pasajero.identificador} | "
                f"Nombre: {pasajero.nombre} | "
                f"Clase: {pasajero.clase} | "
                f"Grupo: {pasajero.grupo_edad()}"
            )

        if len(seleccionados) > 10:
            print("Se muestran solamente los primeros 10 pasajeros.")


if __name__ == "__main__":
    main()
