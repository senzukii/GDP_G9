import unittest
from unittest.mock import Mock

from app.controller.controleur import Controleur


class TestControleur(unittest.TestCase):
    def setUp(self):
        self.moteur = Mock()
        self.moteur.vitesse = 50

        self.servo = Mock()
        self.capteur_ir = Mock()
        self.capteur_us_avant = Mock()
        self.capteur_rgb = Mock()

        self.vue = Mock()
        self.vue.afficher_etat.side_effect = (
            lambda vitesse, obstacle, distance:
            f"Vitesse: {vitesse} | Obstacle IR: {'oui' if obstacle else 'non'} | Distance: {distance} cm"
        )

        self.controleur = Controleur(
            moteur=self.moteur,
            servo=self.servo,
            capteur_ir=self.capteur_ir,
            capteur_us_avant=self.capteur_us_avant,
            capteur_rgb=self.capteur_rgb,
            vue=self.vue,
        )

    def test_stop_si_obstacle(self):
        self.capteur_ir.detecter.return_value = True

        message = self.controleur.mise_a_jour(valeur_ir=1, distance_avant=100)

        self.moteur.arreter.assert_called_once()
        self.moteur.avancer.assert_not_called()
        self.assertIn("Obstacle IR: oui", message)

    def test_avance_si_pas_obstacle(self):
        self.capteur_ir.detecter.return_value = False

        message = self.controleur.mise_a_jour(valeur_ir=0, distance_avant=100)

        self.moteur.avancer.assert_called_once()
        self.moteur.arreter.assert_not_called()
        self.assertIn("Obstacle IR: non", message)

    def test_stop_si_distance_trop_proche(self):
        self.capteur_ir.detecter.return_value = False

        message = self.controleur.mise_a_jour(valeur_ir=0, distance_avant=10)

        self.moteur.arreter.assert_called_once()
        self.moteur.avancer.assert_not_called()
        self.assertIn("Distance: 10 cm", message)

    def test_utilise_ultrason_si_distance_absente(self):
        self.capteur_ir.detecter.return_value = False
        self.capteur_us_avant.measure.return_value = 42

        message = self.controleur.mise_a_jour(valeur_ir=0, distance_avant=None)

        self.capteur_us_avant.measure.assert_called_once()
        self.moteur.avancer.assert_called_once()
        self.assertIn("Distance: 42 cm", message)

    def test_tourner(self):
        self.controleur.tourner(120)
        self.servo.tourner.assert_called_once_with(120)


if __name__ == "__main__":
    unittest.main()
