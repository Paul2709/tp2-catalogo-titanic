"""Pruebas complementarias de casos limite detectados en la auditoria."""

import csv
import tempfile
import unittest
from pathlib import Path

from src.fuentes import FuenteCSV
from src.modelos import Pasajero
from src.pipeline import inspeccionar_datos, preparar_pasajeros, resumir_grupo


class PruebasAuditoria(unittest.TestCase):
    def setUp(self):
        self.registro = {
            "PassengerId": "1",
            "Name": "Pasajero de prueba",
            "Ticket": "A/5 21171",
            "Pclass": "3",
            "Age": "22",
            "Survived": "0",
        }

    def test_csv_con_encabezados_duplicados_se_rechaza(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "duplicado.csv"
            ruta.write_text(
                "PassengerId,Name,Ticket,Pclass,Age,Survived,Survived\n"
                "1,Ejemplo,113803,1,30,1,0\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "encabezados duplicados"):
                FuenteCSV().cargar(ruta)

    def test_csv_encabezados_correctos_se_acepta(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "correcto.csv"
            with ruta.open("w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, self.registro.keys())
                escritor.writeheader()
                escritor.writerow(self.registro)
            registros = FuenteCSV().cargar(ruta)
            self.assertEqual(len(registros), 1)

    def test_ids_1_y_001_cuentan_como_duplicados(self):
        segundo = self.registro.copy()
        segundo["PassengerId"] = "001"
        registros = [self.registro, segundo]
        self.assertEqual(inspeccionar_datos(registros)["id_duplicados"], 1)
        pasajeros, rechazados = preparar_pasajeros(registros)
        self.assertEqual(len(pasajeros), 1)
        self.assertEqual(len(rechazados), 1)

    def test_limites_de_grupos_edad(self):
        casos = (("17.99", "Menor"), ("18", "Adulto"),
                 ("59.99", "Adulto"), ("60", "Adulto mayor"))
        for edad, esperado in casos:
            with self.subTest(edad=edad):
                registro = self.registro.copy()
                registro["Age"] = edad
                self.assertEqual(Pasajero(registro).grupo_edad(), esperado)

    def test_edades_no_finitas_se_rechazan(self):
        for edad in ("NaN", "Infinity", "-Infinity", "121"):
            with self.subTest(edad=edad):
                registro = self.registro.copy()
                registro["Age"] = edad
                with self.assertRaises(ValueError):
                    Pasajero(registro)

    def test_todos_rechazados_no_producen_porcentaje_invalido(self):
        registro = self.registro.copy()
        registro["Pclass"] = "4"
        pasajeros, rechazados = preparar_pasajeros([registro])
        self.assertEqual(len(pasajeros), 0)
        self.assertEqual(len(rechazados), 1)
        self.assertIsNone(resumir_grupo(pasajeros)["proporcion_supervivencia"])
