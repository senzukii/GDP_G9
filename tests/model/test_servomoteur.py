import unittest

from app.model.actionneurs.servomoteur import Servomoteur


class TestServomoteur(unittest.TestCase):
    def test_angle_valide(self):
        servo = Servomoteur()
        servo.tourner(120)
        self.assertEqual(servo.angle, 120)

    def test_angle_invalide(self):
        servo = Servomoteur()
        with self.assertRaises(ValueError):
            servo.tourner(200)


if __name__ == "__main__":
    unittest.main()
