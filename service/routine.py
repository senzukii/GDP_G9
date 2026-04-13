from app.controller.controleur import Controleur
from app.model.actionneurs.moteur import MoteurDC
from app.model.capteurs.capteur_ultrason import HCSR04
from logger import setup_logger

import threading
import time
from datetime import datetime


class Routine:
    def __init__(self, controleur=None):
        self.__controleur = controleur or Controleur()
        self.__resultats = {}
        self.__logs = []

        self.__distances = {"avant": None, "gauche": None, "droite": None}
        self.__distances_lock = threading.Lock()
        self.__threads_actifs = False

        self._initialiser_materiel_concret()
        self._init_logger()

    def _initialiser_materiel_concret(self):
        ctrl = self.__controleur
        self._initialiser_capteur_infrarouge(ctrl)
        self._initialiser_capteurs_ultrason(ctrl)
        self._initialiser_moteur_physique(ctrl)

    def _initialiser_moteur_physique(self, ctrl):
        ctrl.set_moteur(MoteurDC(
            canal=[5, 4],
            pins_direction=[18, 4, 22, 27]
        ))

    def _initialiser_capteur_infrarouge(self, ctrl):
        if ctrl.capteur_ir is None:
            return
        try:
            ctrl.capteur_ir.setup()
        except Exception as e:
            print(f"WARN: Capteur infrarouge indisponible ({e})")

    def _creer_capteur_ultrason(self, trigger_pin, echo_pin):
        return HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin)

    def _initialiser_capteurs_ultrason(self, ctrl):
        ctrl.set_capteur_us_avant(self._creer_capteur_ultrason(16, 25))
        ctrl.set_capteur_us_gauche(self._creer_capteur_ultrason(11, 9))
        ctrl.set_capteur_us_droit(self._creer_capteur_ultrason(26, 19))

    def _init_logger(self):
        self.__logger = setup_logger("ROUTINE")

    def _log(self, niveau, message):
        self.__logs.append(f"{datetime.now().strftime('%H:%M:%S')} | {niveau} | {message}")
        getattr(self.__logger, {
            "OK": "info",
            "ERREUR": "error",
            "DEBUG": "debug",
            "WARN": "warning",
            "INFO": "info"
        }.get(niveau, "info"))(message)

    def _mesurer_ultrason_avec_timeout(self, capteur, timeout=1.0):
        resultat = {"valeur": None, "erreur": None}

        def _worker():
            try:
                resultat["valeur"] = capteur.measure()
            except Exception as e:
                resultat["erreur"] = e

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        t.join(timeout)

        if t.is_alive():
            return None

        if resultat["erreur"] is not None:
            return None

        return resultat["valeur"]

    def _thread_lecture_ultrasons(self):
        ctrl = self.__controleur
        capteurs = [
            ("avant", ctrl.capteur_us_avant),
            ("gauche", ctrl.capteur_us_gauche),
            ("droite", ctrl.capteur_us_droit),
        ]

        while self.__threads_actifs:
            for nom, capteur in capteurs:
                if capteur is None:
                    continue
                try:
                    dist = self._mesurer_ultrason_avec_timeout(capteur, timeout=0.8)
                    with self.__distances_lock:
                        self.__distances[nom] = dist
                except Exception:
                    pass
            time.sleep(0.05)

    def _thread_servo_evitement(self):
        ctrl = self.__controleur
        seuil = 30.0

        while self.__threads_actifs:
            with self.__distances_lock:
                avant = self.__distances["avant"]
                gauche = self.__distances["gauche"]
                droite = self.__distances["droite"]

            if avant is None:
                time.sleep(0.1)
                continue

            try:
                if avant > seuil:
                    ctrl.tourner(90)
                else:
                    g = gauche if gauche is not None else 0
                    d = droite if droite is not None else 0

                    if g >= d:
                        ctrl.tourner(45)
                    else:
                        ctrl.tourner(135)
            except Exception as e:
                self._log("ERREUR", f"Thread servo : {e}")

            time.sleep(0.1)

    def _demarrer_threads(self):
        self.__threads_actifs = True
        self.__t_us = threading.Thread(target=self._thread_lecture_ultrasons, daemon=True)
        self.__t_servo = threading.Thread(target=self._thread_servo_evitement, daemon=True)
        self.__t_us.start()
        self.__t_servo.start()

    def _arreter_threads(self):
        self.__threads_actifs = False

    def lancer_routine(self):
        print("\n=== LANCEMENT AUTOMATIQUE DE LA ROUTINE ===")
        self._log("INFO", "Début routine automatique")

        tests = [
            self.test_moteur,
            self.test_servo,
            self.test_capteur_ir,
            self.test_capteurs_ultrason,
            self.test_demarrage_vert,
            self.test_servo_ultrasons_threade,
            self.identifier_capteurs_ultrason
        ]

        try:
            for test in tests:
                try:
                    test()
                except Exception as e:
                    print(f"ERREUR : {e}")
                    self._log("ERREUR", f"Erreur pendant {test.__name__} : {e}")

                time.sleep(1)

        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur.")
            self._log("WARN", "Routine interrompue manuellement")

        finally:
            self._arreter_threads()
            try:
                self.__controleur.moteur.arreter()
            except Exception:
                pass

    def test_moteur(self):
        print("\n--- Test Moteur ---")
        ctrl = self.__controleur
        self._log("INFO", "Démarrage test moteur")
        ctrl.moteur.regler_vitesse(50)

        print("Avance...")
        ctrl.moteur.avancer()
        time.sleep(2)

        print("Recule...")
        ctrl.moteur.reculer()
        time.sleep(2)

        ctrl.moteur.arreter()
        self._log("OK", "Test moteur réussi")

    def test_servo(self):
        print("\n--- Test Servomoteur ---")
        servo = self._Routine__controleur.servo

        try:
            print("Gauche SAFE (45°)")
            servo.gauche()
            time.sleep(2)

            print("Centre (90°)")
            servo.milieu()
            time.sleep(2)

            print("Droite SAFE (135°)")
            servo.droite()
            time.sleep(2)

            print("Centre (90°)")
            servo.milieu()
            time.sleep(2)

            self._log("OK", "Test servomoteur réussi")
        except Exception as e:
            print(f"Erreur servo : {e}")
            self._log("ERREUR", f"Erreur test servo : {e}")

    def test_servo_ultrasons_threade(self):
        print("\n--- Test Servo + Ultrasons ---")
        print("Le servo s'oriente selon les distances mesurées.")
        self._demarrer_threads()

        try:
            for _ in range(10):
                with self.__distances_lock:
                    d = dict(self.__distances)

                print(f"avant={d['avant']} | gauche={d['gauche']} | droite={d['droite']}", end="\r")
                time.sleep(1)
            print()
        finally:
            self._arreter_threads()

    def test_capteur_ir(self):
        print("\n--- Test Capteur Infrarouge ---")
        print("Le robot avance et doit s'arrêter seulement sur la ligne noire.\n")

        ctrl = self.__controleur
        ctrl.moteur.regler_vitesse(25)
        ctrl.moteur.avancer()
        debut = time.time()

        try:
            while (time.time() - debut) < 10:
                brut = ctrl.capteur_ir.lire()
                detecte = ctrl.capteur_ir.detecter()

                print(f"IR brut={brut} | ligne_noire={detecte}", end="\r")

                if detecte:
                    time.sleep(0.05)
                    if ctrl.capteur_ir.detecter():
                        ctrl.moteur.arreter()
                        print("\nLigne noire détectée !")
                        self._log("OK", "Ligne noire détectée")
                        return

                time.sleep(0.05)

            ctrl.moteur.arreter()
            print("\nTimeout - Aucune ligne noire détectée")
            self._log("WARN", "Timeout capteur IR")
        finally:
            ctrl.moteur.arreter()

    def test_capteurs_ultrason(self):
        print("\n--- Test Capteurs Ultrason ---")
        print("Approche un objet devant chaque capteur pour vérifier sa lecture.\n")

        ctrl = self.__controleur
        for nom, capteur in [
            ("AVANT", ctrl.capteur_us_avant),
            ("GAUCHE", ctrl.capteur_us_gauche),
            ("DROITE", ctrl.capteur_us_droit)
        ]:
            try:
                dist = self._mesurer_ultrason_avec_timeout(capteur, timeout=1.0)
                if dist is None:
                    print(f"Ultrason {nom} : aucune réponse / timeout")
                else:
                    print(f"Ultrason {nom} : {dist:.1f} cm")
            except Exception as e:
                print(f"Ultrason {nom} : erreur ({e})")

    def identifier_capteurs_ultrason(self):
        print("\n--- Identification des capteurs ultrasons ---")
        print("Place un objet très près d'UN SEUL capteur à la fois.")
        print("Observe quel nom voit la petite distance.\n")

        ctrl = self.__controleur
        for i in range(8):
            mesures = {}
            for nom, capteur in [
                ("AVANT", ctrl.capteur_us_avant),
                ("GAUCHE", ctrl.capteur_us_gauche),
                ("DROITE", ctrl.capteur_us_droit)
            ]:
                dist = self._mesurer_ultrason_avec_timeout(capteur, timeout=0.8)
                mesures[nom] = dist

            print(f"Mesure {i+1}: {mesures}")
            time.sleep(1)

    def test_demarrage_vert(self):
        print("\n--- TEST DEMARRAGE AU VERT ---")
        print("Le robot attend le vert puis avance 5 secondes\n")

        ctrl = self.__controleur
        ctrl.moteur.arreter()

        try:
            while True:
                r, g, b = ctrl.capteur_rgb.lire_rgb()
                vert = ctrl.capteur_rgb.est_vert()

                print(f"RGB=({r},{g},{b}) | vert={vert}", end="\r")

                if vert:
                    print("\n✓ Vert détecté → démarrage !")
                    ctrl.moteur.regler_vitesse(40)
                    ctrl.moteur.avancer()
                    time.sleep(5)
                    ctrl.moteur.arreter()
                    print("✓ Arrêt après 5 secondes")
                    return

                time.sleep(0.1)

        except KeyboardInterrupt:
            ctrl.moteur.arreter()
            print("\nArrêt manuel")

    def tout_tester(self):
        print("\n--- Lancement des tests principaux ---")
        for test in [self.test_moteur, self.test_servo, self.test_capteurs_ultrason]:
            try:
                test()
            except Exception as e:
                print(f"Erreur pendant tout_tester : {e}")
                self._log("ERREUR", f"tout_tester : {e}")


if __name__ == "__main__":
    routine = Routine()
    routine.lancer_routine()
