import unittest
from unittest.mock import Mock

from app.model.actionneurs.servomoteur import Servomoteur


class TestServomoteur(unittest.TestCase):
    def test_angle_basse(self):
        servo = Servomoteur()
        servo.tourner(0)
        self.assertEqual(servo.angle, 0)

    def test_angle_seuil(self):
        servo = Servomoteur()
        servo.tourner(90)
        self.assertEqual(servo.angle, 90)

    def test_angle_haute(self):
        servo = Servomoteur()
        servo.tourner(180)
        self.assertEqual(servo.angle, 180)

    def test_angle_invalide_basse(self):
        servo = Servomoteur()
        with self.assertRaises(ValueError):
            servo.tourner(-1)

    def test_angle_invalide_haute(self):
        servo = Servomoteur()
        with self.assertRaises(ValueError):
            servo.tourner(181)

    def test_tourner_avec_servo_simule(self):
        servo_pwm = Mock()

        servo = Servomoteur(servo=servo_pwm)
        servo.tourner(45)

        self.assertEqual(servo.angle, 45)
        self.assertEqual(servo_pwm.angle, 45)


if __name__ == "__main__":
    unittest.main()
