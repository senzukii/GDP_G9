class Servomoteur:
    def __init__(self, servo=None):
        self.__angle = 90
        self.__servo = servo

    @property
    def angle(self):
        return self.get_angle()

    def get_angle(self):
        return self.__angle

    def set_angle(self, angle):
        self.tourner(angle)

    def tourner(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError("angle invalide")

        if angle < 0 or angle > 180:
            raise ValueError("angle invalide")
        self.__angle = angle

        if self.__servo is not None:
            self.__servo.angle = angle
