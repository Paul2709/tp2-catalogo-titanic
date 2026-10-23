
import unittest

from src.modelos import Pasajero


class PruebasPasajero(unittest.TestCase):

    def setUp(self):
        self.registro = {
            "PassengerId": "1",
            "Name": "Braund, Mr. Owen Harris",
            "Ticket": "A/5 21171",
            "Pclass": "3",
            "Age": "22",
            "Survived": "0",
        }

    def test_pasajero_valido(self):
        pasajero = Pasajero(self.registro)
        self.assertEqual(pasajero.identificador, 1)
        self.assertEqual(pasajero.grupo_edad(), "Adulto")

    def test_edad_desconocida(self):
        self.registro["Age"] = None
        pasajero = Pasajero(self.registro)
        self.assertEqual(pasajero.grupo_edad(), "Edad desconocida")

    def test_menor(self):
        self.registro["Age"] = "12"
        pasajero = Pasajero(self.registro)
        self.assertEqual(pasajero.grupo_edad(), "Menor")

    def test_adulto_mayor(self):
        self.registro["Age"] = "65"
        pasajero = Pasajero(self.registro)
        self.assertEqual(pasajero.grupo_edad(), "Adulto mayor")

    def test_clase_invalida(self):
        self.registro["Pclass"] = "4"
        with self.assertRaises(ValueError):
            Pasajero(self.registro)

    def test_billete_invalido(self):
        self.registro["Ticket"] = "@@@"
        with self.assertRaises(ValueError):
            Pasajero(self.registro)

    def test_edad_negativa(self):
        self.registro["Age"] = "-5"
        with self.assertRaises(ValueError):
            Pasajero(self.registro)

    def test_supervivencia_invalida(self):
        self.registro["Survived"] = "3"
        with self.assertRaises(ValueError):
            Pasajero(self.registro)


if __name__ == "__main__":
    unittest.main()
