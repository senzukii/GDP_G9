class MoteurDC:
    def __init__(self, moteur=None):
        self.__vitesse = 0
        self.__etat = "stop"
        self.__moteur = moteur

    @property
    def vitesse(self):
        return self.get_vitesse()

    @property
    def etat(self):
        return self.get_etat()

    def get_vitesse(self):
        return self.__vitesse

    def set_vitesse(self, vitesse):
        self.regler_vitesse(vitesse)

    def get_etat(self):
        return self.__etat

    def set_etat(self, etat):
        if etat not in ("stop", "avant", "arriere"):
            raise ValueError("etat invalide")
        self.__etat = etat

    def regler_vitesse(self, vitesse):
        if not isinstance(vitesse, (int, float)):
            raise TypeError("vitesse invalide")

        if vitesse < 0 or vitesse > 100:
            raise ValueError("vitesse invalide")
        self.__vitesse = vitesse

        if self.__moteur is not None:
            if hasattr(self.__moteur, "set_speed"):
                self.__moteur.set_speed(vitesse)
            elif hasattr(self.__moteur, "speed"):
                self.__moteur.speed = vitesse
            elif hasattr(self.__moteur, "value"):
                self.__moteur.value = vitesse / 100

    def avancer(self):
        self.set_etat("avant")
        if self.__moteur is not None and hasattr(self.__moteur, "forward"):
            self.__moteur.forward()

    def reculer(self):
        self.set_etat("arriere")
        if self.__moteur is not None and hasattr(self.__moteur, "backward"):
            self.__moteur.backward()

    def arreter(self):
        self.set_etat("stop")
        if self.__moteur is not None and hasattr(self.__moteur, "stop"):
            self.__moteur.stop()
