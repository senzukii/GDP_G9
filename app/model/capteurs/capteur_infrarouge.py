class CapteurInfrarouge:
    def __init__(self, seuil=0.5, capteur=None):
        self.seuil = seuil
        self.capteur = capteur

    def detecter(self, valeur=None):
        if valeur is None:
            if self.capteur is None:
                raise TypeError("valeur invalide")
            valeur = self.capteur.value

        if not isinstance(valeur, (int, float)):
            raise TypeError("valeur invalide")

        return valeur < self.seuil
