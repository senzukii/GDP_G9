class CapteurUltrason:
    def lire_distance(self, distance_cm):
        if distance_cm < 0:
            raise ValueError("distance negative interdite")
        return distance_cm
