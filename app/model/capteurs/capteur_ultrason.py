try:
    from gpiozero import DistanceSensor  # type: ignore
except ImportError:
    DistanceSensor = None


class HCSR04:
    """
        Module HCSR04 - Capteur ultrasonique HC-SR04

        Gère la lecture de distance via gpiozero sur Raspberry Pi.
        Applique une moyenne mobile sur les N dernières mesures pour lisser le bruit,
        et ignore les valeurs hors limites (< 10 cm ou > 200 cm).
    """
     
    MIN_DISTANCE = 10
    MAX_DISTANCE = 200

    def __init__(self, trigger_pin=None, echo_pin=None, N=5, offset=0.0):
        self._trigger_pin = trigger_pin
        self._echo_pin = echo_pin
        self._N = N
        self._offset = offset
        self._recent_distances = []
        self._last_valid = None
        self._simulated_distance = 100.0
        self._sensor = None

        if trigger_pin is not None and echo_pin is not None and DistanceSensor is not None:
            self._sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=2)

    @property
    def trigger_pin(self):
        return self._trigger_pin

    @trigger_pin.setter
    def trigger_pin(self, value):
        self._trigger_pin = value

    @property
    def echo_pin(self):
        return self._echo_pin

    @echo_pin.setter
    def echo_pin(self, value):
        self._echo_pin = value

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, value):
        self._N = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    def _measure_pulse(self):
        if self._sensor is not None:
            return self._sensor.distance * 100
        return self._simulated_distance

    def _is_outlier(self, value):
        return value < self.MIN_DISTANCE or value > self.MAX_DISTANCE

    def measure(self):
        raw = self._measure_pulse() - self._offset

        if self._is_outlier(raw):
            if self._last_valid is None:
                return None
            raw = self._last_valid

        self._last_valid = raw
        self._recent_distances.append(raw)
        if len(self._recent_distances) > self._N:
            self._recent_distances = self._recent_distances[-self._N:]

        return round(sum(self._recent_distances) / len(self._recent_distances), 2)

    def lire_distance(self, distance_cm=None):
        if distance_cm is not None:
            if not isinstance(distance_cm, (int, float)):
                raise TypeError("distance invalide")
            if distance_cm < 0:
                raise ValueError("distance invalide")
            return distance_cm
        return self.measure()

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

        angle = 30 if dist_right > threshold_cm * 2 else 15
        return "right", angle

    def scan(self, sensors):
        result = {}

        for name, sensor in sensors.items():
            result[name] = sensor.measure()

        return result

    def cleanup(self):
        if self._sensor is not None:
            self._sensor.close()
