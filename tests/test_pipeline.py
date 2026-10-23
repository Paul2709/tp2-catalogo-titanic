"""Pruebas de inspeccion preliminar del dataset."""

import unittest

from src.pipeline import inspeccionar_datos, validar_esquema


class PruebasPipeline(unittest.TestCase):
    def setUp(self):
        self.registros = [
            {
                "PassengerId": "1",
                "Name": "Pasajero Uno",
                "Ticket": "12345",
                "Pclass": "3",
                "Age": "22",
                "Survived": "0",
            },
            {
                "PassengerId": "2",
                "Name": "Pasajero Dos",
                "Ticket": "23456",
                "Pclass": "1",
                "Age": None,
                "Survived": "1",
            },
        ]

    def test_caso_normal(self):
        resumen = inspeccionar_datos(self.registros)
        self.assertEqual(resumen["observaciones"], 2)
        self.assertEqual(resumen["edades_faltantes"], 1)
        self.assertEqual(resumen["sobrevivientes_registrados"], 1)

    def test_entrada_invalida_sin_columna(self):
        registros = [{"PassengerId": "1"}]
        with self.assertRaisesRegex(ValueError, "columnas"):
            validar_esquema(registros)

    def test_detectar_ids_duplicados(self):
        duplicado = self.registros[0].copy()
        registros = self.registros + [duplicado]
        resumen = inspeccionar_datos(registros)
        self.assertEqual(resumen["id_duplicados"], 1)


if __name__ == "__main__":
    unittest.main()
