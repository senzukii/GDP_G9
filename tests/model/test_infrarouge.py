import unittest

from app.model.capteurs.capteur_infrarouge import CapteurInfrarouge


class TestCapteurInfrarouge(unittest.TestCase):
    def test_detecte_obstacle(self):
        capteur = CapteurInfrarouge()
        self.assertTrue(capteur.detecter(0.1))

    def test_ne_detecte_pas_obstacle(self):
        capteur = CapteurInfrarouge()
        self.assertFalse(capteur.detecter(0.9))


if __name__ == "__main__":
    unittest.main()
