import unittest
from unittest.mock import Mock

from app.model.actionneurs.moteur import MoteurDC


class TestMoteurDC(unittest.TestCase):
    def setUp(self):
        self.driver = Mock()
        self.moteur = MoteurDC()
        self.moteur_mock = MoteurDC(moteur=self.driver)

    def test_vitesse_basse(self):
        self.moteur.regler_vitesse(0)
        self.assertEqual(self.moteur.lire_vitesse(), 0)

    def test_vitesse_seuil(self):
        self.moteur.regler_vitesse(50)
        self.assertEqual(self.moteur.lire_vitesse(), 50)

    def test_vitesse_haute(self):
        self.moteur.regler_vitesse(100)
        self.assertEqual(self.moteur.lire_vitesse(), 100)

    def test_avancer(self):
        self.moteur.avancer()
        self.assertEqual(self.moteur.lire_etat(), "avant")

    def test_reculer(self):
        self.moteur.reculer()
        self.assertEqual(self.moteur.lire_etat(), "arriere")

    def test_arreter(self):
        self.moteur.arreter()
        self.assertEqual(self.moteur.lire_etat(), "stop")

    def test_vitesse_invalide_basse(self):
        with self.assertRaises(ValueError):
            self.moteur.regler_vitesse(-1)

    def test_vitesse_invalide_haute(self):
        with self.assertRaises(ValueError):
            self.moteur.regler_vitesse(101)

    def test_set_etat_invalide(self):
        with self.assertRaises(ValueError):
            self.moteur.set_etat("tourne")

    def test_moteur_avec_driver_simule(self):
        self.moteur_mock.regler_vitesse(60)
        self.moteur_mock.avancer()
        self.moteur_mock.reculer()
        self.moteur_mock.arreter()

        self.assertEqual(self.moteur_mock.vitesse, 60)
        self.assertEqual(self.moteur_mock.etat, "stop")
        self.assertGreaterEqual(self.driver.set_speed.call_count, 1)
        self.assertEqual(self.driver.set_speed.call_args_list[0].args, (60,))
        self.driver.forward.assert_called_once()
        self.driver.backward.assert_called_once()
        self.driver.stop.assert_called_once()

    def test_rampe_depart_avec_driver_simule(self):
        self.moteur_mock.regler_vitesse(25)
        self.driver.reset_mock()

        self.moteur_mock.avancer()

        self.assertGreaterEqual(self.driver.set_speed.call_count, 3)
        self.assertEqual(self.driver.set_speed.call_args_list[0].args, (15,))
        self.assertEqual(self.driver.set_speed.call_args_list[-1].args, (25,))
        self.driver.forward.assert_called_once()

    def test_moteur_avec_pwm(self):
        pwm = Mock()
        moteur_pwm = MoteurDC(pwm=pwm, canal=3)

        moteur_pwm.regler_vitesse(25)

        pwm.set_pwm.assert_called_once_with(3, 0, 1023)

    def test_rampe_depart_avec_pwm(self):
        pwm = Mock()
        moteur_pwm = MoteurDC(pwm=pwm, canal=3)

        moteur_pwm.regler_vitesse(25)
        pwm.reset_mock()

        moteur_pwm.avancer()

        self.assertGreaterEqual(pwm.set_pwm.call_count, 3)
        self.assertEqual(pwm.set_pwm.call_args_list[0].args, (3, 0, 614))
        self.assertEqual(pwm.set_pwm.call_args_list[-1].args, (3, 0, 1023))


if __name__ == "__main__":
    unittest.main()
