class CapteurUltrason:
    def __init__(self, sensor=None, max_distance_cm=100):
        self.__sensor = None
        self.__max_distance_cm = 100
        self.set_sensor(sensor)
        self.set_max_distance_cm(max_distance_cm)

    @property
    def max_distance_cm(self):
        return self.get_max_distance_cm()

    def get_sensor(self):
        return self.__sensor

    def set_sensor(self, sensor):
        self.__sensor = sensor

    def get_max_distance_cm(self):
        return self.__max_distance_cm

    def set_max_distance_cm(self, max_distance_cm):
        if not isinstance(max_distance_cm, (int, float)):
            raise TypeError("distance max invalide")
        if max_distance_cm <= 0:
            raise ValueError("distance max invalide")
        self.__max_distance_cm = max_distance_cm

    def lire_distance(self, distance_cm=None):
        if distance_cm is None:
            if self.__sensor is None:
                raise TypeError("distance invalide")
            distance_cm = self.__sensor.distance * self.__max_distance_cm

        if not isinstance(distance_cm, (int, float)):
            raise TypeError("distance invalide")

        if distance_cm < 0:
            raise ValueError("distance negative interdite")
        return distance_cm
