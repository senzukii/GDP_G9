"""
Module : capteur_infrarouge.py
Description : Gestion du capteur infrarouge LINE FOLLOWER
              Permet de détecter la ligne d'arrivée sur le circuit.

"""

try:
    from gpiozero import InputDevice
except ImportError:
    InputDevice = None

class CapteurInfrarouge:
    """
    Classe représentant le capteur infrarouge (LINE FOLLOWER).
    Permet de détecter la ligne d'arrivée sur le circuit.
    GPIO BCM : 20
    """

    def __init__(self, pin):
        """
        Initialise le capteur infrarouge.
        
        Args:
            pin (int): Numéro du pin GPIO BCM (20 selon schéma de câblage)
        """
        self.pin = pin
        self.capteur = None

    def setup(self):
        """
        Configure le pin GPIO en entrée.
        A appeler une seule fois au démarrage dans main.py
        """
        self.capteur = InputDevice(self.pin)

    def lire(self):
        """
        Lit la valeur brute du capteur.
        
        Returns:
            int: 0 si ligne noire détectée, 1 sinon
        """
        return int(self.capteur.value)

    def ligne_detectee(self):
        """
        Détermine si la ligne d'arrivée est détectée.
        
        Returns:
            bool: True si ligne détectée, False sinon
            
        Raises:
            ValueError: Si la valeur lue n'est pas 0 ou 1
        """
        valeur = self.lire()
        if valeur not in [0, 1]:
            raise ValueError(f"Valeur invalide reçue : {valeur}")
        return valeur == 0