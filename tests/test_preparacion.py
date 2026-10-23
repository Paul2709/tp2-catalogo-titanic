
import unittest

from src.pipeline import preparar_pasajeros


class PruebasPreparacion(unittest.TestCase):

    def setUp(self):
        self.registro = {
            "PassengerId": "1",
            "Name": "Pasajero de prueba",
            "Ticket": "A/5 21171",
            "Pclass": "3",
            "Age": "22",
            "Survived": "0",
        }

    def test_registro_valido(self):
        pasajeros, rechazados = preparar_pasajeros(
            [self.registro]
        )

        self.assertEqual(len(pasajeros), 1)
        self.assertEqual(len(rechazados), 0)

    def test_registro_invalido(self):
        registro = self.registro.copy()
        registro["Pclass"] = "4"

        pasajeros, rechazados = preparar_pasajeros(
            [registro]
        )

        self.assertEqual(len(pasajeros), 0)
        self.assertEqual(len(rechazados), 1)
        self.assertIn("clase", rechazados[0]["motivo"])

    def test_registro_duplicado(self):
        copia = self.registro.copy()

        pasajeros, rechazados = preparar_pasajeros(
            [self.registro, copia]
        )

        self.assertEqual(len(pasajeros), 1)
        self.assertEqual(len(rechazados), 1)
        self.assertIn("duplicado", rechazados[0]["motivo"])

    def test_edad_desconocida(self):
        registro = self.registro.copy()
        registro["Age"] = None

        pasajeros, rechazados = preparar_pasajeros(
            [registro]
        )

        self.assertEqual(
            pasajeros[0].grupo_edad(),
            "Edad desconocida"
        )
        self.assertEqual(len(rechazados), 0)


if __name__ == "__main__":
    unittest.main()
