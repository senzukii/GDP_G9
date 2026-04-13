from time import monotonic, sleep
from app.controller.controleur import Controleur
from app.model.actionneurs.moteur import MoteurDC
import signal
import sys
import threading


# Variables globales
ctrl = None
threads_actifs = False
angle_servo_cible = 90


def thread_maintien_servo():
    """Thread qui maintient le servo a sa position en continu"""
    global threads_actifs, angle_servo_cible
    while threads_actifs:
        try:
            if ctrl and ctrl.servo:
                ctrl.servo.tourner(angle_servo_cible)
        except:
            pass
        sleep(0.1)


def init_robot():
    """Initialise le robot avec tous ses composants"""
    global ctrl
    
    ctrl = Controleur()
    
    # Config moteur avec pins L298N
    ctrl.set_moteur(MoteurDC(
        canal=[5, 4],
        pins_direction=[18, 4, 22, 27]
    ))


def demarrer_threads():
    """Demarre le thread de maintien du servo"""
    global threads_actifs
    threads_actifs = True
    t = threading.Thread(target=thread_maintien_servo, daemon=True)
    t.start()
    sleep(0.3)


def arreter_threads():
    """Arrete proprement tous les threads"""
    global threads_actifs
    threads_actifs = False
    sleep(0.2)


def cleanup():
    """Arrete tout proprement et libere les GPIO"""
    global threads_actifs
    
    arreter_threads()
    
    if ctrl:
        print("\nArret du robot...")
        try:
            ctrl.moteur.arreter()
            sleep(0.1)
            ctrl.servo.milieu()
            sleep(0.2)
        except:
            pass
    
    # Libere les GPIO (gpiozero le fait auto mais on force)
    try:
        if ctrl and ctrl.moteur and hasattr(ctrl.moteur, '_pins_direction'):
            for pin in ctrl.moteur._pins_direction:
                try:
                    pin.close()
                except:
                    pass
    except:
        pass
    
    print("GPIO liberes - Termine")


def signal_handler(sig, frame):
    """Gere Ctrl+C"""
    cleanup()
    sys.exit(0)


def demi_tour():
    """Demi-tour en 3 points comme sur la route"""
    global angle_servo_cible
    
    print("\nDemi-tour en 3 points...")
    
    ctrl.moteur.regler_vitesse(30)
    
    # Point 1: Avance en tournant a gauche
    print("  Avance gauche")
    angle_servo_cible = 45
    sleep(0.2)
    ctrl.moteur.avancer()
    debut = monotonic()
    while monotonic() - debut < 2.0:
        sleep(0.01)
    ctrl.moteur.arreter()
    sleep(0.2)
    
    # Point 2: Recule en tournant a droite
    print("  Recule droite")
    angle_servo_cible = 135
    sleep(0.2)
    ctrl.moteur.reculer()
    debut = monotonic()
    while monotonic() - debut < 1.7:
        sleep(0.01)
    ctrl.moteur.arreter()
    sleep(0.2)
    
    # Point 3: Avance a gauche
    print("  Avance gauche")
    angle_servo_cible = 45
    sleep(0.2)
    ctrl.moteur.avancer()
    debut = monotonic()
    while monotonic() - debut < 1.2:
        sleep(0.01)
    
    ctrl.moteur.arreter()
    angle_servo_cible = 90
    sleep(0.2)
    
    print("Demi-tour termine\n")


def huit():
    """Trace un huit : cercle droit puis cercle gauche"""
    global angle_servo_cible
    
    print("\nHuit...")
    
    ctrl.moteur.regler_vitesse(50)
    ctrl.moteur.avancer()
    
    # Premier cercle COMPLET a droite
    print("  Cercle droit (360 degres)")
    angle_servo_cible = 135  # Braque a fond a droite
    sleep(0.3)
    debut = monotonic()
    while monotonic() - debut < 4.0:  # Temps pour 1 cercle complet
        sleep(0.01)
    
    # Deuxieme cercle COMPLET a gauche
    print("  Cercle gauche (360 degres)")
    angle_servo_cible = 45  # Braque a fond a gauche
    sleep(0.3)
    debut = monotonic()
    while monotonic() - debut < 3.0:  # Meme temps pour symetrie
        sleep(0.01)
    
    ctrl.moteur.arreter()
    angle_servo_cible = 90
    sleep(0.2)
    
    print("Huit termine\n")


def menu():
    """Menu principal"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\nInitialisation...")
    init_robot()
    demarrer_threads()
    print("Robot pret!\n")
    
    try:
        while True:
            print("--- MANOEUVRES ---")
            print("1. Demi-tour")
            print("2. Huit")
            print("0. Quitter")
            
            choix = input("\nChoix: ").strip()
            
            if choix == "0":
                break
            elif choix == "1":
                demi_tour()
            elif choix == "2":
                huit()
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    menu()
