try:
    from gpiozero import InputDevice  # type: ignore
except ImportError:
    InputDevice = None


class CapteurInfrarouge:
    def __init__(self, pin: int = 21, seuil: float = 0.5, capteur=None):
        self._pin = pin
        self._seuil = 0.5
        self._capteur = None
        self.seuil = seuil
        self.capteur = capteur

    @property
    def pin(self) -> int:
        return self._pin

    @pin.setter
    def pin(self, valeur: int):
        if not isinstance(valeur, int) or valeur < 0:
            raise ValueError(f"Le numéro de broche doit être un entier positif, reçu : {valeur}")
        self._pin = valeur

    @property
    def capteur(self):
        return self._capteur

    @capteur.setter
    def capteur(self, valeur):
        self._capteur = valeur

    @property
    def seuil(self):
        return self._seuil

    @seuil.setter
    def seuil(self, valeur):
        if not isinstance(valeur, (int, float)):
            raise TypeError("seuil invalide")
        self._seuil = float(valeur)

    def setup(self):
        if InputDevice is None:
            raise RuntimeError("gpiozero n'est pas disponible sur cette plateforme.")
        self._capteur = InputDevice(self._pin)

    def lire(self) -> int:
        if self._capteur is None:
            raise RuntimeError("Le capteur infrarouge n'est pas initialisé.")
        return int(self._capteur.value)

    def ligne_detectee(self) -> bool:
        valeur = self.lire()
        if valeur not in [0, 1]:
            raise ValueError(f"Valeur invalide reçue : {valeur}")
        return valeur == 1

    def detecter(self, valeur=None, seuil: float = None) -> bool:
        if valeur is None:
            if self._capteur is None:
                raise RuntimeError("Le capteur infrarouge n'est pas initialisé.")
            valeur = self._capteur.value

        if isinstance(valeur, bool):
            return valeur

        if not isinstance(valeur, (int, float)):
            raise TypeError("valeur invalide")

        valeur = int(valeur)
        if valeur not in [0, 1]:
            raise ValueError(f"Valeur invalide reçue : {valeur}")

        # 1 = noir, 0 = blanc
        return valeur == 1
