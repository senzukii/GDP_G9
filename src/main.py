import time
from HCSR04 import HCSR04
# from Servo import Servo  <- quand le module servo sera prêt

front = HCSR04(trigger_pin=11, echo_pin=9)
left  = HCSR04(trigger_pin=6,  echo_pin=5)
right = HCSR04(trigger_pin=26, echo_pin=19)

# servo = Servo()  <- qd le module servo sera prêt

try:
    while True:
        direction, angle = front.get_best_direction(left, right)

        print(f"Front: {front.measure()} cm      ")
        print(f"Left:  {left.measure()} cm       ")
        print(f"Right: {right.measure()} cm      ")
        print(f"→ {direction} | angle: {angle}°  ")

        # servo.angle = angle  <- qd le module servo sera prêt

        status = front.get_obstacle_status()
        print(f"Status: {status}      ")

        print("\033[5A", end="")  # 5 maintenant car une ligne de plus
        time.sleep(0.1)

except KeyboardInterrupt:
    front.cleanup()
    left.cleanup()
    right.cleanup()