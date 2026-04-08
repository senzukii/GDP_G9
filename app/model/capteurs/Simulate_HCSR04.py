import random
import time

#pas oublier que capteurs ultra-sons fonctionnent avec 5 V et faut max 3,3 V !!

class HCSR04:
    """
        SIMULATION du Module HCSR04 - Capteur ultrasonique HC-SR04

        Gère la lecture de distance via gpiozero sur Raspberry Pi.
        Applique une moyenne mobile sur les N dernières mesures pour lisser le bruit,
        et ignore les valeurs hors limites (< 10 cm ou > 200 cm).
    """
    MIN_DISTANCE = 10
    MAX_DISTANCE = 200

    def __init__(self, N=5, offset=0.0):
        self.N = N
        self.offset = offset
        self._recent_distances = []
        self._simulated_distance = 100.0
        self._last_valid = None

    def _simulate_pulse(self):
        noise = random.uniform(-0.5, 0.5)
        return self._simulated_distance + noise

    def _is_outlier(self, value):
        return value < self.MIN_DISTANCE or value > self.MAX_DISTANCE

    def measure(self):
        raw = self._simulate_pulse() - self.offset

        if self._is_outlier(raw):
            if self._last_valid is None:
                return None
            raw = self._last_valid

        self._last_valid = raw
        self._recent_distances.append(raw)
        if len(self._recent_distances) > self.N:
            self._recent_distances.pop(0)

        return round(sum(self._recent_distances) / len(self._recent_distances), 2) #moyenne mobile

    def set_simulated_distance(self, distance):
        self._simulated_distance = float(distance)

    def get_obstacle_status(self, threshold_cm=15.0):
        distance = self.measure()
        if distance is None:
            return "unknown"
        if distance <= threshold_cm:
            return "critical"
        if distance <= threshold_cm * 2: 
            return "warning"
        return "clear"

    def get_best_direction(self, left_sensor, right_sensor, threshold_cm=15.0):
        dist_front = self.measure()
        if dist_front is None or dist_front > threshold_cm:
            return "forward", 0

        dist_left = left_sensor.measure() or 0
        dist_right = right_sensor.measure() or 0

        if dist_left >= dist_right:
            angle = -30 if dist_left > threshold_cm * 2 else -15
            return "left", angle
        else:
            angle = 30 if dist_right > threshold_cm * 2 else 15
            return "right", angle

    def scan(self, sensors):
        result = {}

        for name, sensor in sensors.items():
            result[name] = sensor.measure()

        return result