import unittest

from app.controller.controleur import Controleur


class TestControleur(unittest.TestCase):
    def test_stop_si_obstacle(self):
        controleur = Controleur()
        controleur.moteur.regler_vitesse(50)

        message = controleur.mise_a_jour(0.1, 100)

        self.assertEqual(controleur.moteur.etat, "stop")
        self.assertIn("Obstacle IR: oui", message)

    def test_avance_si_pas_obstacle(self):
        controleur = Controleur()
        controleur.moteur.regler_vitesse(50)

        message = controleur.mise_a_jour(0.9, 100)

        self.assertEqual(controleur.moteur.etat, "avant")
        self.assertIn("Obstacle IR: non", message)

    def test_avance_au_seuil(self):
        controleur = Controleur()
        controleur.moteur.regler_vitesse(50)

        message = controleur.mise_a_jour(0.5, 20)

        self.assertEqual(controleur.moteur.etat, "avant")
        self.assertIn("Obstacle IR: non", message)
        self.assertIn("Distance: 20 cm", message)

    def test_tourner(self):
        controleur = Controleur()
        controleur.tourner(120)
        self.assertEqual(controleur.servo.angle, 120)


if __name__ == "__main__":
    unittest.main()
