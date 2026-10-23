
import unittest

from src.modelos import Pasajero
from src.pipeline import filtrar_grupo, resumir_grupo


class PruebasResumen(unittest.TestCase):

    def setUp(self):
        datos = [
            (1, 1, 1),
            (2, 0, 1),
            (3, 1, 3),
            (4, 0, 3),
        ]

        self.pasajeros = []

        for identificador, sobrevivio, clase in datos:
            registro = {
                "PassengerId": str(identificador),
                "Name": f"Pasajero {identificador}",
                "Ticket": str(10000 + identificador),
                "Pclass": str(clase),
                "Age": "25",
                "Survived": str(sobrevivio),
            }

            self.pasajeros.append(Pasajero(registro))

    def test_cantidad_total(self):
        resultado = resumir_grupo(self.pasajeros)

        self.assertEqual(resultado["total"], 4)
        self.assertEqual(resultado["sobrevivientes"], 2)

    def test_proporcion_supervivencia(self):
        resultado = resumir_grupo(self.pasajeros)

        self.assertAlmostEqual(
            resultado["proporcion_supervivencia"],
            0.5,
        )

    def test_grupo_vacio(self):
        resultado = resumir_grupo([])

        self.assertEqual(resultado["total"], 0)
        self.assertIsNone(
            resultado["proporcion_supervivencia"]
        )

    def test_conservacion_de_cantidades(self):
        resultado = resumir_grupo(self.pasajeros)

        total_calculado = (
            resultado["sobrevivientes"]
            + resultado["no_sobrevivientes"]
        )

        self.assertEqual(total_calculado, resultado["total"])


if __name__ == "__main__":
    unittest.main()
