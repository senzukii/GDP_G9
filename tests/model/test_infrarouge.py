"""
Module : test_infrarouge.py
Description : Tests unitaires du capteur infrarouge LINE FOLLOWER.
              Utilise des mocks pour simuler le matériel sans Raspberry Pi.
"""

import unittest
from unittest.mock import Mock
from app.model.capteurs.capteur_infrarouge import CapteurInfrarouge

class TestCapteurInfrarouge(unittest.TestCase):

    # TEST 1 : le capteur détecte une ligne noire
    def test_ligne_detectee(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(return_value=0)

        self.assertTrue(capteur.ligne_detectee())

    # TEST 2 : le capteur ne détecte rien
    def test_pas_de_ligne(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(return_value=1)

        self.assertFalse(capteur.ligne_detectee())

    # TEST 3 : on vérifie que lire() est bien appelé
    def test_lire_est_appele(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(return_value=0)

        capteur.ligne_detectee()

        capteur.lire.assert_called_once()

    # TEST 4 : simuler une panne GPIO
    def test_panne_gpio(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(side_effect=RuntimeError("GPIO error"))

        with self.assertRaises(RuntimeError):
            capteur.ligne_detectee()

    # TEST 5 : séquence de valeurs
    def test_sequence_approche_ligne(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(side_effect=[1, 1, 0])

        self.assertFalse(capteur.ligne_detectee())
        self.assertFalse(capteur.ligne_detectee())
        self.assertTrue(capteur.ligne_detectee())

    # TEST 6 : valeur 2 → hors range → erreur
    def test_valeur_hors_range(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(return_value=2)

        with self.assertRaises(ValueError):
            capteur.ligne_detectee()

    # TEST 7 : valeur absurde → erreur
    def test_valeur_absurde(self):
        capteur = CapteurInfrarouge(pin=20)
        capteur.lire = Mock(return_value="abc")

        with self.assertRaises(ValueError):
            capteur.ligne_detectee()

if __name__ == '__main__':
    unittest.main()