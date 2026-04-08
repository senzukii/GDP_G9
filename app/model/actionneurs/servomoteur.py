class Servomoteur:
    def __init__(self, servo=None):
        self.angle = 90
        self.servo = servo

    def tourner(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError("angle invalide")

        if angle < 0 or angle > 180:
            raise ValueError("angle invalide")
        self.angle = angle

        if self.servo is not None:
            self.servo.angle = angle
