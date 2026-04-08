import unittest
from unittest.mock import Mock

from app.model.capteurs.capteur_infrarouge import CapteurInfrarouge


class TestCapteurInfrarouge(unittest.TestCase):
    def test_valeur_basse(self):
        capteur = CapteurInfrarouge()
        self.assertTrue(capteur.detecter(0.1))

    def test_valeur_seuil(self):
        capteur = CapteurInfrarouge()
        self.assertFalse(capteur.detecter(0.5))

    def test_valeur_haute(self):
        capteur = CapteurInfrarouge()
        self.assertFalse(capteur.detecter(0.9))

    def test_valeur_invalide(self):
        capteur = CapteurInfrarouge()
        with self.assertRaises(TypeError):
            capteur.detecter(None)

    def test_detecter_avec_capteur_simule(self):
        capteur_gpio = Mock()
        capteur_gpio.value = 0.2

        capteur = CapteurInfrarouge(capteur=capteur_gpio)

        self.assertTrue(capteur.detecter())


if __name__ == "__main__":
    unittest.main()
