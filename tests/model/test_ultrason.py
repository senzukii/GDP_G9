import unittest

from app.model.capteurs.capteur_ultrason import CapteurUltrason


class TestCapteurUltrason(unittest.TestCase):
    def test_distance_valide(self):
        capteur = CapteurUltrason()
        self.assertEqual(capteur.lire_distance(42), 42)

    def test_distance_negative(self):
        capteur = CapteurUltrason()
        with self.assertRaises(ValueError):
            capteur.lire_distance(-1)


if __name__ == "__main__":
    unittest.main()
