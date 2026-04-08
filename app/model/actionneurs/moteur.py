try:
    import Adafruit_PCA9685 #type: ignore
except ImportError:
    Adafruit_PCA9685 = None

try:
    from gpiozero import OutputDevice #type: ignore
except ImportError:
    OutputDevice = None


class MoteurDC:
    """
    Classe de controle d'un moteur DC (ou d'un double pont H type L298N).

    API uniforme avec Servomoteur:
    - proprietes + getter/setter explicites
    - methodes metier simples (avancer, reculer, arreter)
    - compatibilite avec un driver simule pour les tests
    """

    def __init__(self, moteur=None, canal=None, adresse_i2c=0x40, pwm=None, pins_direction=None):
        self._vitesse = 0
        self._etat = "stop"
        self._moteur = moteur
        
        # Gestion de un ou plusieurs canaux (ex: 5 pour ENA, 4 pour ENB)
        if canal is None:
            self._canal = [5, 4] 
        elif isinstance(canal, int):
            self._canal = [canal]
        else:
            self._canal = canal
            
        self._pwm = pwm
        self._rampe_depart_min = 15
        self._rampe_pas = 5
        self._rampe_palier = 5

        #Configuration matérielle des broches IN1, IN2, IN3, IN4 ---
        self._pins_direction = []
        if pins_direction and OutputDevice is not None:
            for pin in pins_direction:
                self._pins_direction.append(OutputDevice(pin))

        # Initialisation du PCA9685
        if self._moteur is None and self._pwm is None and Adafruit_PCA9685:
            self._pwm = Adafruit_PCA9685.PCA9685(address=adresse_i2c)
            self._pwm.set_pwm_freq(50)

    @property
    def vitesse(self):
        return self.get_vitesse()

    @vitesse.setter
    def vitesse(self, valeur):
        self.set_vitesse(valeur)

    @property
    def etat(self):
        return self.get_etat()

    @etat.setter
    def etat(self, valeur):
        self.set_etat(valeur)

    @property
    def moteur(self):
        return self.get_moteur()

    @moteur.setter
    def moteur(self, valeur):
        self.set_moteur(valeur)

    def get_vitesse(self):
        return self._vitesse

    def set_vitesse(self, vitesse):
        if not isinstance(vitesse, (int, float)):
            raise TypeError("vitesse invalide")

        if vitesse < 0 or vitesse > 100:
            raise ValueError("vitesse invalide")

        self._vitesse = vitesse
        self._appliquer_vitesse_driver(vitesse)

    def get_etat(self):
        return self._etat

    def set_etat(self, etat):
        if etat not in ("stop", "avant", "arriere"):
            raise ValueError("etat invalide")
        self._etat = etat

    def get_moteur(self):
        return self._moteur

    def set_moteur(self, moteur):
        self._moteur = moteur

    def _appliquer_vitesse_driver(self, vitesse):
        if self._moteur is not None and hasattr(self._moteur, "set_speed"):
            self._moteur.set_speed(vitesse)
            return

        if self._moteur is not None and hasattr(self._moteur, "speed"):
            self._moteur.speed = vitesse
            return

        if self._moteur is not None and hasattr(self._moteur, "value"):
            self._moteur.value = vitesse / 100
            return

        if self._pwm is not None:
            duty_cycle = int((vitesse / 100.0) * 4095)
            # Applique le signal PWM sur chaque canal configuré (ENA et ENB)
            for c in self._canal:
                self._pwm.set_pwm(c, 0, duty_cycle)

    def _rampe_s(self, vitesse_cible):
        """Monte progressivement en vitesse pour éviter le patinage au démarrage."""
        if vitesse_cible <= 0:
            self._appliquer_vitesse_driver(0)
            return

        vitesse_depart = min(self._rampe_depart_min, vitesse_cible)
        progression = list(range(vitesse_depart, vitesse_cible + 1, self._rampe_pas))

        if not progression or progression[-1] != vitesse_cible:
            progression.append(vitesse_cible)

        for _ in range(self._rampe_palier):
            self._appliquer_vitesse_driver(vitesse_depart)

        for vitesse in progression[1:]:
            self._appliquer_vitesse_driver(vitesse)

    def regler_vitesse(self, vitesse):
        self.set_vitesse(vitesse)

    def lire_vitesse(self):
        return self.get_vitesse()

    def lire_etat(self):
        return self.get_etat()

    def avancer(self):
        self.set_etat("avant")
        
        # Actionnement des broches L298N pour la MARCHE AVANT
        if len(self._pins_direction) >= 2:
            self._pins_direction[0].on()   # IN1 = Vrai
            self._pins_direction[1].off()  # IN2 = Faux
        if len(self._pins_direction) >= 4:
            self._pins_direction[2].on()   # IN3 = Vrai
            self._pins_direction[3].off()  # IN4 = Faux

        self._rampe_s(self._vitesse)
        if self._moteur is not None and hasattr(self._moteur, "forward"):
            self._moteur.forward()

    def reculer(self):
        self.set_etat("arriere")
        
        # Actionnement des broches L298N pour la MARCHE ARRIÈRE
        if len(self._pins_direction) >= 2:
            self._pins_direction[0].off()  # IN1 = Faux
            self._pins_direction[1].on()   # IN2 = Vrai
        if len(self._pins_direction) >= 4:
            self._pins_direction[2].off()  # IN3 = Faux
            self._pins_direction[3].on()   # IN4 = Vrai

        self._rampe_s(self._vitesse)
        if self._moteur is not None and hasattr(self._moteur, "backward"):
            self._moteur.backward()

    def arreter(self):
        self.set_etat("stop")
        
        # Extinction complète des broches de direction
        for pin in self._pins_direction:
            pin.off()
            
        self._appliquer_vitesse_driver(0)
        
        if self._moteur is not None and hasattr(self._moteur, "stop"):
            self._moteur.stop()