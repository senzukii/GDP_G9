try:
    from gpiozero import InputDevice
except ImportError:
    InputDevice = None  # sur PC pas de gpiozero


class CapteurInfrarouge:

    def __init__(self, pin: int = 20):
        self._pin = pin
        self._capteur = None

    # ── Getters / Setters 

    @property
    def pin(self) -> int:
        """Numéro de la broche GPIO."""
        return self._pin

    @pin.setter
    def pin(self, valeur: int):
        if not isinstance(valeur, int) or valeur < 0:
            raise ValueError(f"Le numéro de broche doit être un entier positif, reçu : {valeur}")
        self._pin = valeur

    @property
    def capteur(self):
        """Instance InputDevice du capteur."""
        return self._capteur

    @capteur.setter
    def capteur(self, valeur):
        self._capteur = valeur

    # ── Méthodes ─────────────────────────────────────────────────────────────

    def setup(self):
        """Initialise le périphérique GPIO pour le capteur."""
        if InputDevice is None:
            raise RuntimeError("gpiozero n'est pas disponible sur cette plateforme.")
        self._capteur = InputDevice(self._pin)

    def lire(self) -> int:
        """
        Lit la valeur brute du capteur.

        Returns
        -------
        int
            0 ou 1 selon l'état du capteur.
        """
        return int(self._capteur.value)

    def ligne_detectee(self) -> bool:
        """
        Indique si la ligne noire est détectée.

        Returns
        -------
        bool
            True si la ligne est détectée, False sinon.

        Raises
        ------
        ValueError
            Si la valeur lue n'est pas 0 ou 1.
        """
        valeur = self.lire()
        if valeur not in [0, 1]:
            raise ValueError(f"Valeur invalide reçue : {valeur}")
        return valeur == 0