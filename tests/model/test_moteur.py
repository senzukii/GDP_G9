import unittest
from unittest.mock import Mock

from app.model.actionneurs.moteur import MoteurDC


class TestMoteurDC(unittest.TestCase):
    def test_vitesse_basse(self):
        moteur = MoteurDC()
        moteur.regler_vitesse(0)
        self.assertEqual(moteur.vitesse, 0)

    def test_vitesse_seuil(self):
        moteur = MoteurDC()
        moteur.regler_vitesse(50)
        self.assertEqual(moteur.vitesse, 50)

    def test_vitesse_haute(self):
        moteur = MoteurDC()
        moteur.regler_vitesse(100)
        self.assertEqual(moteur.vitesse, 100)

    def test_avancer(self):
        moteur = MoteurDC()
        moteur.avancer()
        self.assertEqual(moteur.etat, "avant")

    def test_reculer(self):
        moteur = MoteurDC()
        moteur.reculer()
        self.assertEqual(moteur.etat, "arriere")

    def test_arreter(self):
        moteur = MoteurDC()
        moteur.arreter()
        self.assertEqual(moteur.etat, "stop")

    def test_vitesse_invalide_basse(self):
        moteur = MoteurDC()
        with self.assertRaises(ValueError):
            moteur.regler_vitesse(-1)

    def test_vitesse_invalide_haute(self):
        moteur = MoteurDC()
        with self.assertRaises(ValueError):
            moteur.regler_vitesse(101)

    def test_moteur_avec_driver_simule(self):
        driver = Mock()

        moteur = MoteurDC(moteur=driver)
        moteur.regler_vitesse(60)
        moteur.avancer()
        moteur.reculer()
        moteur.arreter()

        self.assertEqual(moteur.vitesse, 60)
        self.assertEqual(moteur.etat, "stop")
        driver.set_speed.assert_called_once_with(60)
        driver.forward.assert_called_once()
        driver.backward.assert_called_once()
        driver.stop.assert_called_once()


if __name__ == "__main__":
    unittest.main()
