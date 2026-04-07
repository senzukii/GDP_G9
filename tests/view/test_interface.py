import unittest

from app.view.interface import Interface


class TestInterface(unittest.TestCase):
    def test_affichage(self):
        vue = Interface()
        message = vue.afficher_etat(40, True, 18)
        self.assertIn("Vitesse: 40", message)
        self.assertIn("Obstacle IR: oui", message)
        self.assertIn("Distance: 18 cm", message)


if __name__ == "__main__":
    unittest.main()
