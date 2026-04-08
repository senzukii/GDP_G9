import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from gpiozero import OutputDevice
except ImportError:
    print("Ce script doit être exécuté sur le Raspberry Pi (gpiozero requis).")
    sys.exit(1)

# GPIO déjà utilisés ou sensibles — NE PAS TOUCHER
PINS_ULTRASON = {5, 6, 9, 11, 19, 26}     # trig/echo des 3 ultrason
PINS_IR = {20}                              # capteur infrarouge
PINS_I2C = {2, 3}                           # SDA/SCL (PCA9685, RGB, servo)
PINS_SERIE = {14, 15}                       # TX/RX série
PINS_SPI = {7, 8, 10, 25}                  # SPI (ne pas toucher)
PINS_RESERVES = PINS_ULTRASON | PINS_IR | PINS_I2C | PINS_SERIE | PINS_SPI

# Candidats restants pour IN1-IN4
PINS_A_TESTER = sorted([pin for pin in range(4, 28) if pin not in PINS_RESERVES])


def tester_pin(pin):
    try:
        device = OutputDevice(pin)
        device.on()
        print(f"  GPIO {pin} : ACTIVÉ → regarde si un moteur réagit")
        input("  Appuie sur Entrée pour désactiver...")
        device.off()
        device.close()

        reponse = input(f"  Est-ce qu'un moteur a bougé ? (o/n) : ").strip().lower()
        if reponse == "o":
            quel = input(f"  Quel moteur ? (gauche/droit) : ").strip().lower()
            direction = input(f"  Quelle direction ? (avant/arriere) : ").strip().lower()
            return {"pin": pin, "moteur": quel, "direction": direction}
    except Exception as e:
        print(f"  GPIO {pin} : erreur ({e})")
    return None


def main():
    print("=== DÉTECTION DES PINS IN1, IN2, IN3, IN4 ===")
    print("On va activer chaque GPIO un par un.")
    print("Regarde si un moteur tourne à chaque fois.\n")

    resultats = []

    for pin in PINS_A_TESTER:
        print(f"\nTest GPIO {pin} :")
        resultat = tester_pin(pin)
        if resultat:
            resultats.append(resultat)
            print(f"  → Noté : GPIO {pin} = moteur {resultat['moteur']} {resultat['direction']}")

        if len(resultats) == 4:
            print("\n4 pins trouvés, on arrête !")
            break

    print("\n=== RÉSULTAT ===")
    if resultats:
        for r in resultats:
            print(f"  GPIO {r['pin']} → moteur {r['moteur']} ({r['direction']})")
        print("\nReporte ces valeurs dans service/routine.py à la place des TODO.")
    else:
        print("Aucun pin trouvé. Vérifie le câblage.")


if __name__ == "__main__":
    main()
