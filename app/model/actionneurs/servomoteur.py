try:
    import Adafruit_PCA9685 #type: ignore
except ImportError:
    Adafruit_PCA9685 = None

class Servomoteur:
    """
    Classe de contrôle pour un servomoteur branché sur une carte I2C PCA9685.
    
    Fonctionnalités principales :
    - Pilote le moteur en convertissant un angle (0° à 180°) en signal électrique PWM.
    - SÉCURITÉ : Limite les angles physiques pour éviter de casser la direction.
    - Raccourcis de mouvements (gauche, droite, milieu, min, max).
    """
    
    # Valeurs calibrées basées sur le duty cycle : 4%, 6%, 8%
    PULSE_GAUCHE = 190   # 4% duty cycle - LIMITE PHYSIQUE GAUCHE
    PULSE_CENTRE = 285   # 6% duty cycle  
    PULSE_DROITE = 380   # 8% duty cycle - LIMITE PHYSIQUE DROITE
    
    # Angles logiques correspondants (remappés pour sécurité)
    ANGLE_MIN_SAFE = 45    # "Gauche max" devient 45° dans le code
    ANGLE_CENTRE = 90      # Centre reste 90°
    ANGLE_MAX_SAFE = 135   # "Droite max" devient 135° dans le code
    
    def __init__(self, servo=None, canal=0, adresse_i2c=0x40):
        """
        Initialise le servomoteur et configure la communication matérielle.
        
        Args:
            canal (int, optionnel): Le port (0 à 15) de la carte PCA9685. Défaut à 0.
            adresse_i2c (hex, optionnel): L'adresse I2C de la carte PCA9685. Défaut à 0x40.
            
        Comportement:
            - Active le signal PWM à 50 Hz.
            - Force le moteur à se positionner à 90° (centre) dès l'instanciation.
            - BLOQUE les angles dangereux (< 45° ou > 135°)
        """
        self._canal = canal
        self._angle = 90
        self._servo = servo
        self._pwm = None
        
        if self._servo is None and Adafruit_PCA9685:
            self._pwm = Adafruit_PCA9685.PCA9685(address=adresse_i2c, busnum=1)
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
        
        # ⚠️ SÉCURITÉ : Bloquer les angles dangereux
        if valeur < self.ANGLE_MIN_SAFE or valeur > self.ANGLE_MAX_SAFE:
            raise ValueError(
                f"DANGER ! Angle {valeur}° hors limites safe. "
                f"Utilisez entre {self.ANGLE_MIN_SAFE}° et {self.ANGLE_MAX_SAFE}° "
                f"pour ne pas casser la direction !"
            )
        
        self._angle = valeur
        
        if self._servo is not None:
            if hasattr(self._servo, "angle"):
                self._servo.angle = valeur
            elif hasattr(self._servo, "set_angle"):
                self._servo.set_angle(valeur)
            return
        
        # Conversion avec les valeurs calibrées (duty cycle)
        if self._pwm:
            # Mapping: 45° → PULSE_GAUCHE, 90° → PULSE_CENTRE, 135° → PULSE_DROITE
            if valeur <= 90:
                # Interpolation entre gauche safe (45°) et centre (90°)
                ratio = (valeur - self.ANGLE_MIN_SAFE) / (self.ANGLE_CENTRE - self.ANGLE_MIN_SAFE)
                pulse = int(self.PULSE_GAUCHE + (self.PULSE_CENTRE - self.PULSE_GAUCHE) * ratio)
            else:
                # Interpolation entre centre (90°) et droite safe (135°)
                ratio = (valeur - self.ANGLE_CENTRE) / (self.ANGLE_MAX_SAFE - self.ANGLE_CENTRE)
                pulse = int(self.PULSE_CENTRE + (self.PULSE_DROITE - self.PULSE_CENTRE) * ratio)
            
            self._pwm.set_pwm(self._canal, 0, pulse)
    
    def tourner(self, angle):
        self.set_angle(angle)
    
    def aller_a(self, angle):
        self.angle = angle
    
    def lire_angle(self):
        return self.angle
    
    def gauche(self):
        """Tourne à gauche (position safe max)"""
        self.aller_a(self.ANGLE_MIN_SAFE)  # 45° = gauche max safe
    
    def droite(self):
        """Tourne à droite (position safe max)"""
        self.aller_a(self.ANGLE_MAX_SAFE)  # 135° = droite max safe
    
    def milieu(self):
        """Position centrale (tout droit)"""
        self.aller_a(self.ANGLE_CENTRE)  # 90°
    
    def min(self):
        """Position minimale SAFE (gauche max)"""
        self.aller_a(self.ANGLE_MIN_SAFE)  # 45° au lieu de 0°
    
    def max(self):
        """Position maximale SAFE (droite max)"""
        self.aller_a(self.ANGLE_MAX_SAFE)  # 135° au lieu de 180°
