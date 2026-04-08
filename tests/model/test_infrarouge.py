import unittest
from unittest.mock import MagicMock, patch
from capteur_infrarouge import CapteurInfrarouge


class TestCapteurInfrarouge(unittest.TestCase):

    def setUp(self):
        """Capteur avec un InputDevice mocké."""
        self.capteur = CapteurInfrarouge(pin=20)
        self.capteur._capteur = MagicMock()

    # Détection de ligne 
    
    def test_ligne_noire_detectee(self):
        """Le capteur renvoie 0 → ligne noire détectée."""
        self.capteur._capteur.value = 0
        self.assertTrue(self.capteur.ligne_detectee())

    def test_aucune_ligne_detectee(self):
        """Le capteur renvoie 1 → aucune ligne détectée."""
        self.capteur._capteur.value = 1
        self.assertFalse(self.capteur.ligne_detectee())

    # Vérification appel de lire()

    def test_lire_est_appele(self):
        """Vérifie que lire() est bien appelé par ligne_detectee()."""
        with patch.object(self.capteur, "lire", return_value=0) as mock_lire:
            self.capteur.ligne_detectee()
            mock_lire.assert_called_once()

    #  Simulation de panne

    def test_panne_capteur(self):
        """Simule une panne matérielle lors de la lecture."""
        with patch.object(self.capteur, "lire", side_effect=Exception("Panne")):
            with self.assertRaises(Exception):
                self.capteur.lire()

    def test_capteur_non_initialise(self):
        """Lire sans appeler setup() lève une AttributeError."""
        c = CapteurInfrarouge(pin=20)  # _capteur vaut None
        with self.assertRaises(AttributeError):
            c.lire()

    #  Valeurs limites 

    def test_valeur_dans_range(self):
        """Valeurs valides (0 et 1) ne lèvent pas d'exception."""
        for valeur in [0, 1]:
            with self.subTest(valeur=valeur):
                self.capteur._capteur.value = valeur
                self.assertEqual(self.capteur.lire(), valeur)

    def test_valeur_hors_range(self):
        """Valeurs hors range [0, 1] lèvent une ValueError."""
        for valeur in [-1, 2, 255]:
            with self.subTest(valeur=valeur):
                self.capteur._capteur.value = valeur
                with self.assertRaisesRegex(ValueError, "Valeur invalide reçue"):
                    self.capteur.ligne_detectee()

    def test_valeur_absurde(self):
        """Valeurs absurdes (None, str, float…) lèvent une TypeError ou ValueError."""
        for valeur in [None, "abc", 3.14, [], {}]:
            with self.subTest(valeur=valeur):
                self.capteur._capteur.value = valeur
                with self.assertRaises((TypeError, ValueError)):
                    self.capteur.ligne_detectee()


if __name__ == "__main__":
    unittest.main()