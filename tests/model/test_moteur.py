import unittest

from app.model.actionneurs.moteur import MoteurDC


class TestMoteurDC(unittest.TestCase):
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

    def test_vitesse_valide(self):
        moteur = MoteurDC()
        moteur.regler_vitesse(60)
        self.assertEqual(moteur.vitesse, 60)

    def test_vitesse_invalide(self):
        moteur = MoteurDC()
        with self.assertRaises(ValueError):
            moteur.regler_vitesse(120)


if __name__ == "__main__":
    unittest.main()
