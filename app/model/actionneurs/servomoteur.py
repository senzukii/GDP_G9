class Servomoteur:
    def __init__(self):
        self.angle = 90

    def tourner(self, angle):
        if angle < 0 or angle > 180:
            raise ValueError("angle invalide")
        self.angle = angle
