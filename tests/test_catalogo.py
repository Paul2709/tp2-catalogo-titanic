
import unittest

from src.modelos import Pasajero
from src.pipeline import (
    buscar_pasajero,
    filtrar_grupo,
    indexar_pasajeros,
)


class PruebasCatalogo(unittest.TestCase):

    def setUp(self):
        registros = [
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
            {
                "PassengerId": "3",
                "Name": "Pasajero Tres",
                "Ticket": "34567",
                "Pclass": "1",
                "Age": "12",
                "Survived": "1",
            },
        ]

        self.pasajeros = [Pasajero(r) for r in registros]
        self.indice = indexar_pasajeros(self.pasajeros)

    def test_buscar_pasajero_existente(self):
        pasajero = buscar_pasajero(self.indice, 1)
        self.assertEqual(pasajero.nombre, "Pasajero Uno")

    def test_buscar_pasajero_inexistente(self):
        pasajero = buscar_pasajero(self.indice, 999)
        self.assertIsNone(pasajero)

    def test_filtrar_por_clase(self):
        resultado = filtrar_grupo(self.pasajeros, clase=1)
        self.assertEqual(len(resultado), 2)

    def test_filtrar_edad_desconocida(self):
        resultado = filtrar_grupo(
            self.pasajeros,
            grupo_edad="Edad desconocida",
        )
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].identificador, 2)

    def test_combinar_filtros(self):
        resultado = filtrar_grupo(
            self.pasajeros,
            clase=1,
            grupo_edad="Menor",
        )
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].identificador, 3)

    def test_clase_invalida(self):
        with self.assertRaises(ValueError):
            filtrar_grupo(self.pasajeros, clase=4)


if __name__ == "__main__":
    unittest.main()
