class MoteurDC:
    def __init__(self):
        self.vitesse = 0
        self.etat = "stop"

    def regler_vitesse(self, vitesse):
        if vitesse < 0 or vitesse > 100:
            raise ValueError("vitesse invalide")
        self.vitesse = vitesse

    def avancer(self):
        self.etat = "avant"

    def reculer(self):
        self.etat = "arriere"

    def arreter(self):
        self.etat = "stop"
