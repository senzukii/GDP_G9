class CapteurInfrarouge:
    def __init__(self, seuil=0.5, capteur=None):
        self.__seuil = 0.5
        self.__capteur = None
        self.set_seuil(seuil)
        self.set_capteur(capteur)

    @property
    def seuil(self):
        return self.get_seuil()

    def get_seuil(self):
        return self.__seuil

    def set_seuil(self, seuil):
        if not isinstance(seuil, (int, float)):
            raise TypeError("seuil invalide")
        self.__seuil = seuil

    def get_capteur(self):
        return self.__capteur

    def set_capteur(self, capteur):
        self.__capteur = capteur

    def detecter(self, valeur=None):
        if valeur is None:
            if self.__capteur is None:
                raise TypeError("valeur invalide")
            valeur = self.__capteur.value

        if not isinstance(valeur, (int, float)):
            raise TypeError("valeur invalide")

        return valeur < self.__seuil
