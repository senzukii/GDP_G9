import unittest
from unittest.mock import patch
from app.model.capteurs.capteur_RGB import CapteurRGB

class TestCapteurRGB(unittest.TestCase):
    
    def setUp(self):
        patch('app.model.capteurs.capteur_RGB.board').start()
        self.patcher = patch('app.model.capteurs.capteur_RGB.adafruit_tcs34725')
        self.mock_adafruit = self.patcher.start()
        self.addCleanup(patch.stopall)
        
        self.module_rgb = CapteurRGB(seuil=30)
        self.module_rgb.capteur = self.mock_adafruit.TCS34725.return_value

    def test_est_vert(self):
        """Teste la détection du vert."""
        self.module_rgb.capteur.color_rgb_bytes = (20, 200, 20) #type: ignore
        self.assertTrue(self.module_rgb.est_vert())
        self.assertFalse(self.module_rgb.est_rouge())

    def test_est_rouge(self):
        """Teste la détection du rouge."""
        self.module_rgb.capteur.color_rgb_bytes = (200, 20, 20) #type: ignore
        self.assertTrue(self.module_rgb.est_rouge())
        self.assertFalse(self.module_rgb.est_vert())

    def test_couleur_ambigue(self):
        """Teste qu'aucune couleur n'est détectée si similaires."""
        self.module_rgb.capteur.color_rgb_bytes = (100, 100, 100) #type: ignore
        self.assertFalse(self.module_rgb.est_vert())
        self.assertFalse(self.module_rgb.est_rouge())
    
    def test_lire_rgb_sans_capteur(self):
        """Teste que lire_rgb retourne (0,0,0) si pas de capteur."""
        capteur_vide = CapteurRGB()
        capteur_vide.capteur = None
        self.assertEqual(capteur_vide.lire_rgb(), (0, 0, 0))
    
    def test_seuil_personnalise(self):
        """Teste qu'on peut changer le seuil."""
        capteur = CapteurRGB(seuil=100)
        self.assertEqual(capteur.seuil, 100)

if __name__ == '__main__':
    unittest.main(verbosity=2)

#py -m unittest tests/model/test_rgb.py pour lancer le test depuis la racine du projet.