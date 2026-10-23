"""Fuentes de datos con una interfaz comun para CSV y JSON."""

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path


def normalizar_fila(fila):
    """Representar todas las celdas como texto o None para ambos formatos."""
    resultado = {}
    for clave, valor in fila.items():
        if not isinstance(clave, str):
            raise ValueError("Los nombres de las columnas deben ser texto.")
        if isinstance(valor, (dict, list)):
            raise ValueError(f"El campo {clave} debe tener un valor simple.")
        if valor is None or str(valor).strip() == "":
            resultado[clave] = None
        else:
            resultado[clave] = str(valor).strip()
    return resultado


class FuenteDatos(ABC):
    """Interfaz comun que exige implementar el metodo cargar."""

    @abstractmethod
    def cargar(self, ruta):
        """Devolver una lista de diccionarios con los datos cargados."""


class FuenteCSV(FuenteDatos):
    """Lee un CSV con encabezados."""

    def cargar(self, ruta):
        with Path(ruta).open("r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if not lector.fieldnames:
                raise ValueError("El CSV no tiene encabezados.")
            if len(lector.fieldnames) != len(set(lector.fieldnames)):
                raise ValueError("El CSV tiene encabezados duplicados.")
            registros = []
            for numero, fila in enumerate(lector, start=2):
                if None in fila:
                    raise ValueError(
                        f"La fila {numero} del CSV tiene columnas adicionales."
                    )
                registros.append(normalizar_fila(fila))
        return registros


class FuenteJSON(FuenteDatos):
    """Lee un JSON que contiene una lista de objetos."""

    def cargar(self, ruta):
        with Path(ruta).open("r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        if not isinstance(contenido, list):
            raise ValueError("El JSON debe contener una lista de objetos.")
        registros = []
        for posicion, fila in enumerate(contenido, start=1):
            if not isinstance(fila, dict):
                raise ValueError(
                    f"El elemento {posicion} del JSON no es un objeto."
                )
            registros.append(normalizar_fila(fila))
        return registros


def seleccionar_fuente(ruta):
    """Devolver la fuente apropiada segun la extension del archivo."""
    extension = Path(ruta).suffix.lower()
    if extension == ".csv":
        return FuenteCSV()
    if extension == ".json":
        return FuenteJSON()
    raise ValueError("Formato no admitido: use un archivo .csv o .json.")


def guardar_json(registros, ruta):
    """Crear un archivo JSON equivalente a los registros cargados."""
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, indent=2, ensure_ascii=False)
