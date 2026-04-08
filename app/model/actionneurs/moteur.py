class MoteurDC:
    def __init__(self, moteur=None):
        self.vitesse = 0
        self.etat = "stop"
        self.moteur = moteur

    def regler_vitesse(self, vitesse):
        if not isinstance(vitesse, (int, float)):
            raise TypeError("vitesse invalide")

        if vitesse < 0 or vitesse > 100:
            raise ValueError("vitesse invalide")
        self.vitesse = vitesse

        if self.moteur is not None:
            if hasattr(self.moteur, "set_speed"):
                self.moteur.set_speed(vitesse)
            elif hasattr(self.moteur, "speed"):
                self.moteur.speed = vitesse
            elif hasattr(self.moteur, "value"):
                self.moteur.value = vitesse / 100

    def avancer(self):
        self.etat = "avant"
        if self.moteur is not None and hasattr(self.moteur, "forward"):
            self.moteur.forward()

    def reculer(self):
        self.etat = "arriere"
        if self.moteur is not None and hasattr(self.moteur, "backward"):
            self.moteur.backward()

    def arreter(self):
        self.etat = "stop"
        if self.moteur is not None and hasattr(self.moteur, "stop"):
            self.moteur.stop()
