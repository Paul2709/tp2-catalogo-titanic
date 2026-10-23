"""Pruebas de los archivos de salida."""

import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.exportacion import (
    exportar_fichas,
    exportar_rechazos,
    exportar_resumen,
)
from src.modelos import Pasajero


class PruebasExportacion(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        self.addCleanup(self.directorio.cleanup)
        self.ruta = Path(self.directorio.name)
        self.pasajero = Pasajero({
            "PassengerId": "1",
            "Name": "Pasajero Uno",
            "Ticket": "A/5 21171",
            "Pclass": "3",
            "Age": None,
            "Survived": "0",
        })

    def test_exportar_fichas(self):
        destino = self.ruta / "pasajeros.csv"
        exportar_fichas([self.pasajero], destino)

        with destino.open(encoding="utf-8-sig", newline="") as archivo:
            filas = list(csv.DictReader(archivo))

        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["PassengerId"], "1")
        self.assertEqual(filas[0]["GrupoEdad"], "Edad desconocida")
        self.assertEqual(filas[0]["Age"], "")

    def test_exportar_fichas_vacias(self):
        destino = self.ruta / "pasajeros.csv"
        exportar_fichas([], destino)

        with destino.open(encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            self.assertIn("PassengerId", lector.fieldnames)
            self.assertEqual(list(lector), [])

    def test_exportar_resumen(self):
        destino = self.ruta / "resumen.json"
        resumen = {
            "total": 4,
            "sobrevivientes": 2,
            "no_sobrevivientes": 2,
            "proporcion_supervivencia": 0.5,
        }
        exportar_resumen(resumen, destino)

        with destino.open(encoding="utf-8") as archivo:
            resultado = json.load(archivo)

        self.assertEqual(resultado, resumen)

    def test_exportar_rechazos(self):
        destino = self.ruta / "rechazados.csv"
        rechazos = [{
            "registro": 4,
            "identificador": "9",
            "motivo": "La clase debe ser 1, 2 o 3.",
        }]
        exportar_rechazos(rechazos, destino)

        with destino.open(encoding="utf-8-sig", newline="") as archivo:
            filas = list(csv.DictReader(archivo))

        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["registro"], "4")
        self.assertIn("clase", filas[0]["motivo"])

    def test_exportar_rechazos_vacios(self):
        destino = self.ruta / "rechazados.csv"
        exportar_rechazos([], destino)

        with destino.open(encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            self.assertEqual(len(list(lector)), 0)
            self.assertEqual(lector.fieldnames, [
                "registro", "identificador", "motivo"
            ])
