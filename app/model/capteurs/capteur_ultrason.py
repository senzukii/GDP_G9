try:
    from gpiozero import InputDevice
except ImportError:
    InputDevice = None  # sur PC, pas de gpiozero

class CapteurInfrarouge:
    def __init__(self, pin):
        self.pin = pin
        self.capteur = None

    def setup(self):
        self.capteur = InputDevice(self.pin)

    def lire(self):
        return int(self.capteur.value)

    def ligne_detectee(self):
        valeur = self.lire()
        if valeur not in [0, 1]:
            raise ValueError(f"Valeur invalide reçue : {valeur}")
        return valeur == 0