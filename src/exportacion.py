"""Exportacion de fichas, resumenes y registros rechazados."""

import csv
import json
from pathlib import Path


COLUMNAS_FICHAS = [
    "PassengerId",
    "Name",
    "Ticket",
    "Pclass",
    "Age",
    "Survived",
    "GrupoEdad",
]

COLUMNAS_RECHAZOS = ["registro", "identificador", "motivo"]


def guardar_csv(filas, columnas, ruta):
    """Guardar una lista de diccionarios en un archivo CSV."""
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with destino.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


def exportar_fichas(pasajeros, ruta):
    """Guardar las fichas de los pasajeros seleccionados."""
    fichas = [pasajero.ficha() for pasajero in pasajeros]
    guardar_csv(fichas, COLUMNAS_FICHAS, ruta)


def exportar_resumen(resumen, ruta):
    """Guardar un resumen estadistico en formato JSON."""
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with destino.open("w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, indent=2, ensure_ascii=False)


def exportar_rechazos(rechazados, ruta):
    """Guardar los registros rechazados y sus motivos."""
    guardar_csv(rechazados, COLUMNAS_RECHAZOS, ruta)
