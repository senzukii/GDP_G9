try:
    import board  # type: ignore
    import busio  # type: ignore
    import adafruit_tcs34725  # type: ignore
except ImportError:
    board = None
    busio = None
    adafruit_tcs34725 = None


class CapteurRGB:
    def __init__(self, seuil=3):
        self.seuil = seuil
        self.capteur = None
        self.i2c = None

        if board is None or busio is None or adafruit_tcs34725 is None:
            return

        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.capteur = adafruit_tcs34725.TCS34725(self.i2c)
            self.capteur.integration_time = 50
            self.capteur.gain = 4
        except Exception:
            self.capteur = None

    def disponible(self):
        return self.capteur is not None

    def lire_rgb(self):
        if self.capteur is None:
            return (0, 0, 0)
        try:
            return self.capteur.color_rgb_bytes
        except Exception:
            return (0, 0, 0)

    def est_vert(self):
        r, g, b = self.lire_rgb()
        total = r + g + b

        if total < 35:
            return False

        return g > r + self.seuil and g > b + self.seuil and g / total > 0.36

    def est_rouge(self):
        r, g, b = self.lire_rgb()
        total = r + g + b

        if total < 35:
            return False

        return r > g + 5 and r > b + 5 and r / total > 0.40

    def est_bleu(self):
        r, g, b = self.lire_rgb()
        total = r + g + b

        if total < 35:
            return False

        return b > r + 5 and b > g + 5 and b / total > 0.40
