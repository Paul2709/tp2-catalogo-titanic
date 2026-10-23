"""Pruebas de lectura CSV y JSON."""

import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.fuentes import FuenteCSV, FuenteJSON, guardar_json


class PruebasFuentes(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.carpeta = Path(self.temporal.name)
        self.ruta_csv = self.carpeta / "ejemplo.csv"
        filas = [
            {
                "PassengerId": "1",
                "Name": "Pasajero Uno",
                "Ticket": "A/5 21171",
                "Pclass": "3",
                "Age": "22",
                "Survived": "0",
            },
            {
                "PassengerId": "2",
                "Name": "Pasajero Dos",
                "Ticket": "PC 17599",
                "Pclass": "1",
                "Age": "",
                "Survived": "1",
            },
        ]
        with self.ruta_csv.open("w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=filas[0].keys())
            escritor.writeheader()
            escritor.writerows(filas)

    def test_csv_leido_correctamente(self):
        registros = FuenteCSV().cargar(self.ruta_csv)
        self.assertEqual(len(registros), 2)
        self.assertIsNone(registros[1]["Age"])

    def test_csv_y_json_producen_mismos_datos(self):
        datos_csv = FuenteCSV().cargar(self.ruta_csv)
        ruta_json = self.carpeta / "ejemplo.json"
        guardar_json(datos_csv, ruta_json)
        datos_json = FuenteJSON().cargar(ruta_json)
        self.assertEqual(datos_csv, datos_json)

    def test_json_no_admite_un_objeto_suelto(self):
        ruta_json = self.carpeta / "incorrecto.json"
        ruta_json.write_text(json.dumps({"PassengerId": 1}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "lista de objetos"):
            FuenteJSON().cargar(ruta_json)


if __name__ == "__main__":
    unittest.main()
