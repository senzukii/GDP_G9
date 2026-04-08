try:
    import board #type: ignore
    import adafruit_tcs34725 #type: ignore
except ImportError:
    board = adafruit_tcs34725 = None

class CapteurRGB:
    def __init__(self, seuil=30):
        self.seuil = seuil
        try:
            self.capteur = adafruit_tcs34725.TCS34725(board.I2C()) if board else None #type: ignore
            # Si board ou adafruit_tcs34725 n'est pas disponible, capteur sera None
            #le board est utilisé pour vérifier la présence du matériel, gpio, i2c, etc
            #adafruit_tcs34725 est la bibliothèque qui gère le capteur de couleur.
        except Exception:
            self.capteur = None

    def lire_rgb(self):
        """Retourne (R, G, B) ou (0, 0, 0) si erreur."""
        #.color_rgb_bytes est une propriété de la bibliothèque adafruit qui retourne les valeurs RGB
        if not self.capteur:
            return (0, 0, 0)
        try:
            return self.capteur.color_rgb_bytes
        except Exception:
            return (0, 0, 0)

    def est_vert(self):
        """Vrai si le Vert domine largement le Rouge et le Bleu."""
        r, g, b = self.lire_rgb()
        return g > max(r, b) + self.seuil

    def est_rouge(self):
        """Vrai si le Rouge domine largement le Vert et le Bleu."""
        r, g, b = self.lire_rgb()
        return r > max(g, b) + self.seuil
    
