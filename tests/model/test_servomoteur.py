import unittest
from unittest.mock import patch
from app.model.actionneurs.servomoteur import Servomoteur


class TestServomoteur(unittest.TestCase):
    """
    Tests unitaires du servomoteur via la carte PCA9685.
    Le @patch remplace Adafruit_PCA9685 par un faux objet pour pouvoir
    exécuter ces tests sur un PC classique, sans que le robot ne soit branché.
    
    Le PWM est la technique qui consiste à envoyer 
    une série d'impulsions à une fréquence fixe (ici 50 Hz). 

    La puce PCA9685 découpe son signal électrique sur une échelle allant de 0 à 4095.
    La formule mathématique de notre code convertit les degrés en un "Pulse" sur cette échelle :
        - Pulse de 150 (signal court)  -> Le moteur se place à 0°.
        - Pulse de 375 (signal moyen)  -> Le moteur se place à 90°.
        - Pulse de 600 (signal long)   -> Le moteur se place à 180°.
        
    """
    
    def setUp(self):
        self.patcher_adafruit = patch('app.model.actionneurs.servomoteur.Adafruit_PCA9685')
        self.mock_adafruit = self.patcher_adafruit.start()
        self.faux_pwm = self.mock_adafruit.PCA9685.return_value

    def tearDown(self):
        self.patcher_adafruit.stop()

    def test_initialisation(self):
        # On récupère l'instance de la classe PCA9685 créée par le constructeur du servomoteur
        # On crée une instance du servomoteur, qui doit initialiser le PWM et se positionner à 90°
        servo = Servomoteur() 
        self.assertEqual(servo.canal, 0)
        self.assertEqual(servo.lire_angle(), 90)
        self.faux_pwm.set_pwm_freq.assert_called_with(50)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 375) # 0 = canal, 0 = on, 375 = pulse pour 90°
    
    def test_aller_a_0(self):
        servo = Servomoteur()
        
        servo.aller_a(0)
        
        self.assertEqual(servo.lire_angle(), 0)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 150) #0 = canal, 0 = on, 150 = pulse pour 0°
    
    def test_aller_a_90(self):
        servo = Servomoteur()
        
        servo.aller_a(90)
        
        self.assertEqual(servo.lire_angle(), 90)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 375) # 0 = canal, 0 = on, 375 = pulse pour 90°
    
    def test_aller_a_180(self):
        servo = Servomoteur()
        servo.aller_a(180)
        
        self.assertEqual(servo.lire_angle(), 180)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 600) # 0 = canal, 0 = on, 600 = pulse pour 180°
    
    def test_angle_negatif(self):
        servo = Servomoteur()
        
        with self.assertRaises(ValueError):
            servo.aller_a(-10)
    
    def test_angle_trop_grand(self):
        servo = Servomoteur()
        
        with self.assertRaises(ValueError):
            servo.aller_a(200)
    
    def test_type_invalide(self):
        servo = Servomoteur()
        with self.assertRaises(TypeError):
            servo.aller_a("90")
    
    def test_gauche(self):
        servo = Servomoteur()
        servo.gauche()
        self.assertEqual(servo.lire_angle(), 45)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 262)
    
    def test_droite(self):
        servo = Servomoteur()
        
        servo.droite()
        
        self.assertEqual(servo.lire_angle(), 135)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 487)
    
    def test_milieu(self):
        servo = Servomoteur()
        
        servo.gauche()
        servo.milieu()
        
        self.assertEqual(servo.lire_angle(), 90)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 375)
    
    def test_min(self):
        servo = Servomoteur()
        
        servo.min()
        
        self.assertEqual(servo.lire_angle(), 0)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 150)
    
    def test_max(self):
        servo = Servomoteur()
        
        servo.max()
        
        self.assertEqual(servo.lire_angle(), 180)
        self.faux_pwm.set_pwm.assert_called_with(0, 0, 600)
    
    def test_sequence(self):
        servo = Servomoteur()
        servo.gauche()
        self.assertEqual(servo.lire_angle(), 45)
        servo.droite()
        self.assertEqual(servo.lire_angle(), 135)
        servo.milieu()
        self.assertEqual(servo.lire_angle(), 90)

if __name__ == '__main__':
    unittest.main(verbosity=2)