import unittest
from unittest.mock import Mock

from app.model.capteurs.capteur_ultrason import CapteurUltrason


class TestCapteurUltrason(unittest.TestCase):
    def test_valeur_basse(self):
        capteur = CapteurUltrason()
        self.assertEqual(capteur.lire_distance(0), 0)

    def test_valeur_seuil(self):
        capteur = CapteurUltrason()
        self.assertEqual(capteur.lire_distance(20), 20)

    def test_valeur_haute(self):
        capteur = CapteurUltrason()
        self.assertEqual(capteur.lire_distance(100), 100)

    def test_valeur_invalide(self):
        capteur = CapteurUltrason()
        with self.assertRaises(ValueError):
            capteur.lire_distance(-1)

    def test_lire_distance_avec_capteur_simule(self):
        capteur_gpio = Mock()
        capteur_gpio.distance = 0.2

        capteur = CapteurUltrason(sensor=capteur_gpio, max_distance_cm=100)

        self.assertEqual(capteur.lire_distance(), 20)


if __name__ == "__main__":
    unittest.main()
