class CapteurInfrarouge:
    def __init__(self, seuil=0.5):
        self.seuil = seuil

    def detecter(self, valeur):
        return valeur < self.seuil
