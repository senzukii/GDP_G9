try:
    import Adafruit_PCA9685
except ImportError:
    Adafruit_PCA9685 = None


class Servomoteur:
    """
    Classe de contrôle pour un servomoteur branché sur une carte I2C PCA9685.
    
    Fonctionnalités principales :
    - Pilote le moteur en convertissant un angle (0° à 180°) en signal électrique PWM.
    - Sécurité matérielle : bloque automatiquement les angles invalides pour ne pas forcer le moteur.
    - Raccourcis de mouvements (gauche, droite, milieu, min, max).
    """

    def __init__(self, servo=None, canal=0, adresse_i2c=0x40):
        """
        Initialise le servomoteur et configure la communication matérielle.
        
        Args:
            canal (int, optionnel): Le port (0 à 15) de la carte PCA9685. Défaut à 0.
            adresse_i2c (hex, optionnel): L'adresse I2C de la carte PCA9685. Défaut à 0x40.
            
        Comportement:
            - Active le signal PWM à 50 Hz.
            - Permet l'exécution du code sur un PC sans matériel.
            - Force le moteur à se positionner à 90° (centre) dès l'instanciation.
        """
        self._canal = canal
        self._angle = 90
        self._servo = servo
        self._pwm = None
        
        if self._servo is None and Adafruit_PCA9685:
            self._pwm = Adafruit_PCA9685.PCA9685(address=adresse_i2c) # Initialisation de la carte PCA9685
            self._pwm.set_pwm_freq(50)
        
        self.angle = 90 


    @property
    def canal(self):
        return self._canal

    @canal.setter
    def canal(self, valeur):
        if not isinstance(valeur, int) or not (0 <= valeur <= 15):
            raise ValueError("Le canal doit être un entier compris entre 0 et 15.")
        self._canal = valeur

    @property
    def pwm(self):
        return self._pwm

    @property
    def angle(self):
        return self.get_angle()

    @angle.setter
    def angle(self, valeur):
        self.set_angle(valeur)

    def get_angle(self):
        return self._angle

    def set_angle(self, valeur):
        if not isinstance(valeur, (int, float)):
            raise TypeError("L'angle doit être un nombre")
        
        if valeur < 0 or valeur > 180:
            raise ValueError("L'angle doit être entre 0 et 180")
        
        self._angle = valeur
        
        if self._servo is not None:
            if hasattr(self._servo, "angle"):
                self._servo.angle = valeur
            elif hasattr(self._servo, "set_angle"):
                self._servo.set_angle(valeur)
            return

        
        # Conversion de l'angle, valeur/180, puis mult par l'amplitude du signal (600-150) et ajout à la valeur minimale (150)
        if self._pwm:
            pulse = int(150 + (valeur / 180.0) * (600 - 150)) 
            self._pwm.set_pwm(self._canal, 0, pulse) # Canal, on, pulse (durée de l'impulsion)

    def tourner(self, angle):
        self.set_angle(angle)


    def aller_a(self, angle):
        self.angle = angle
    
    def lire_angle(self):
        return self.angle
    
    def gauche(self):
        self.aller_a(45)
    
    def droite(self):
        self.aller_a(135)
    
    def milieu(self):
        self.aller_a(90)
    
    def min(self):
        self.aller_a(0)
    
    def max(self):
        self.aller_a(180)