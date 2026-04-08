class CapteurUltrason:
    def __init__(self, sensor=None, max_distance_cm=100):
        self.sensor = sensor
        self.max_distance_cm = max_distance_cm

    def lire_distance(self, distance_cm=None):
        if distance_cm is None:
            if self.sensor is None:
                raise TypeError("distance invalide")
            distance_cm = self.sensor.distance * self.max_distance_cm

        if not isinstance(distance_cm, (int, float)):
            raise TypeError("distance invalide")

        if distance_cm < 0:
            raise ValueError("distance negative interdite")
        return distance_cm
