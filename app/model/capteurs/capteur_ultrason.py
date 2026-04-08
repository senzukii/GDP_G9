"""
Module HCSR04 - Capteur ultrasonique HC-SR04

Gère la lecture de distance via gpiozero sur Raspberry Pi.
Applique une moyenne mobile sur les N dernières mesures pour lisser le bruit,
et ignore les valeurs hors limites (< 10 cm ou > 200 cm).

Broches utilisées (BCM) :
    - Front : TRIG=11, ECHO=9
    - Left  : TRIG=6,  ECHO=5
    - Right : TRIG=26, ECHO=19

Utilisation :
    front = HCSR04(trigger_pin=11, echo_pin=9)
    print(front.measure())              # distance en cm
    print(front.get_obstacle_status())  # "clear", "warning" ou "critical"
"""

import time
try:
    from gpiozero import DistanceSensor  # type: ignore
except ImportError:
    DistanceSensor = None

class HCSR04:
    MIN_DISTANCE = 10
    MAX_DISTANCE = 200

    def __init__(self, trigger_pin, echo_pin, N=5, offset=0.0): # on choisit offset ici si valeur décalée fixe
        self._trigger_pin = trigger_pin
        self._echo_pin = echo_pin
        self._N = N
        self._offset = offset
        self._recent_distances = []
        self._last_valid = None
        if DistanceSensor is not None:
            self._sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=2)
        else:
            self._sensor = None
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
        if self._sensor is None:
            raise RuntimeError("DistanceSensor indisponible")
        return self._sensor.distance * 100 # 2 * 100 = 200 cm

    def _is_outlier(self, value):
        return value < self.MIN_DISTANCE or value > self.MAX_DISTANCE

    def measure(self):
        raw = self._measure_pulse() - self._offset

        if self._is_outlier(raw): # si + grand que 200 ou + petit que 10, ca remplace par derniere mesure valide
            if self._last_valid is None:
                return None
            raw = self._last_valid

        self._last_valid = raw
        self._recent_distances.append(raw)
        if len(self._recent_distances) > self._N:
            self._recent_distances = self._recent_distances[-self._N:] #Si [1,2,3,4,5,6,7] => [3,4,5,6,7] car N = 5

        return round(sum(self._recent_distances) / len(self._recent_distances), 2) # moyenne mobile

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
            if dist_left > threshold_cm * 2:
                angle = -30
            else:
                angle = -15

            return "left", angle
        else:
            if dist_right > threshold_cm * 2:
                angle = 30
            else:
                angle = 15

            return "right", angle

    def scan(self, sensors):
        result = {}

        for name, sensor in sensors.items():
            result[name] = sensor.measure()

        return result

    def cleanup(self):
        if self._sensor is not None:
            self._sensor.close()