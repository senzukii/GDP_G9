try:
    from gpiozero import InputDevice
except ImportError:
    InputDevice = None  # sur PC pas de gpiozero


class CapteurInfrarouge:

    def __init__(self, pin: int = 20, seuil: float = 0.5, capteur=None):
        self._pin = pin
        self._seuil = 0.5
        self._capteur = None
        self.seuil = seuil
        self.capteur = capteur

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

    @property
    def seuil(self):
        return self._seuil

    @seuil.setter
    def seuil(self, valeur):
        if not isinstance(valeur, (int, float)):
            raise TypeError("seuil invalide")
        self._seuil = float(valeur)

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

    def detecter(self, valeur=None, seuil: float = None) -> bool:
        """
        Détecte un obstacle/ligne noire.

        - Sans argument, utilise la lecture matérielle (0/1).
        - Avec argument, accepte une valeur simulée (int/float/bool).
        """
        seuil_actif = self._seuil if seuil is None else seuil
        if not isinstance(seuil_actif, (int, float)):
            raise TypeError("seuil invalide")

        if valeur is None:
            if self._capteur is None:
                raise TypeError("valeur invalide")
            valeur = self._capteur.value

        if isinstance(valeur, bool):
            return valeur

        if not isinstance(valeur, (int, float)):
            raise TypeError("valeur invalide")

        return valeur < float(seuil_actif)
