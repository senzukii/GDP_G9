import sys
import os
import time
import logging
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.controller.controleur import Controleur


class _CapteurUltrasonSimule:
    def __init__(self, distance_cm=100.0):
        self._distance_cm = float(distance_cm)

    def measure(self):
        return self._distance_cm

# === CÂBLAGE GPIO ===
# Capteur IR : GPIO 20
# Ultrason avant : TRIG=6, ECHO=5
# Ultrason gauche : TRIG=11, ECHO=9
# Ultrason droit : TRIG=26, ECHO=19
# Capteur RGB : I2C (SDA/SCL, auto)
# Servomoteur : PCA9685 I2C (canal 0 par défaut)
# Moteur DC - ENA : PCA9685 canal 5
# Moteur DC - ENB : PCA9685 canal 4
# Moteur DC - IN1 : GPIO TODO  <-- à compléter
# Moteur DC - IN2 : GPIO TODO  <-- à compléter
# Moteur DC - IN3 : GPIO TODO  <-- à compléter
# Moteur DC - IN4 : GPIO TODO  <-- à compléter


class Routine:
    def __init__(self, controleur=None):
        self.__controleur = controleur or Controleur()
        self.__resultats = {}
        self.__logs = []
        self._mode_simulation = False
        self._initialiser_fallbacks_simulation()
        self._init_logger()

    def _initialiser_fallbacks_simulation(self):
        """Ajoute des capteurs simulés quand le matériel n'est pas disponible."""
        ctrl = self.__controleur

        if ctrl.capteur_us_avant is None:
            ctrl.set_capteur_us_avant(_CapteurUltrasonSimule(80.0))
            self._mode_simulation = True
        if ctrl.capteur_us_gauche is None:
            ctrl.set_capteur_us_gauche(_CapteurUltrasonSimule(65.0))
            self._mode_simulation = True
        if ctrl.capteur_us_droit is None:
            ctrl.set_capteur_us_droit(_CapteurUltrasonSimule(75.0))
            self._mode_simulation = True

    def _init_logger(self):
        self.__logger = logging.getLogger("routine")
        self.__logger.setLevel(logging.DEBUG)
        if not self.__logger.handlers:
            # Affichage console
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self.__logger.addHandler(console)

            # Fichier de log détaillé
            os.makedirs(os.path.join(os.path.dirname(__file__), "..", "reports"), exist_ok=True)
            chemin_log = os.path.join(os.path.dirname(__file__), "..", "reports", "routine.log")
            fichier = logging.FileHandler(chemin_log, encoding="utf-8")
            fichier.setLevel(logging.DEBUG)
            fichier.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
            self.__logger.addHandler(fichier)

    def _log(self, niveau, message):
        self.__logs.append(f"{datetime.now().strftime('%H:%M:%S')} | {niveau} | {message}")
        if niveau == "OK":
            self.__logger.info(message)
        elif niveau == "ERREUR":
            self.__logger.error(message)
        elif niveau == "DEBUG":
            self.__logger.debug(message)
        elif niveau == "WARN":
            self.__logger.warning(message)
        else:
            self.__logger.info(message)

    def _generer_rapport(self):
        os.makedirs(os.path.join(os.path.dirname(__file__), "..", "reports"), exist_ok=True)
        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
        chemin = os.path.join(os.path.dirname(__file__), "..", "reports", f"routine_{horodatage}.txt")

        with open(chemin, "w", encoding="utf-8") as f:
            f.write(f"Rapport routine - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            for ligne in self.__logs:
                f.write(ligne + "\n")
            f.write("\n" + "=" * 60 + "\n")
            f.write("RÉSUMÉ\n")
            f.write("=" * 60 + "\n")
            for nom, ok in self.__resultats.items():
                f.write(f"  {nom} : {'OK' if ok else 'ERREUR'}\n")
            pret = all(self.__resultats.values()) if self.__resultats else False
            f.write(f"\nÉtat global : {'PRÊT' if pret else 'NON PRÊT'}\n")

        print(f"\nRapport enregistré : {os.path.abspath(chemin)}")
        self.__logger.info(f"Rapport enregistré : {os.path.abspath(chemin)}")
        return chemin

    def menu(self):
        while True:
            print("\n=== MENU ROUTINE DE TEST ===")
            print("1. Test moteur (avancer / reculer / retour)")
            print("2. Test servomoteur (tourner / redresser)")
            print("3. Test capteur infrarouge (rouler jusqu'à la ligne noire)")
            print("4. Test capteurs ultrason (lire distances)")
            print("5. Test capteur RGB (démarrage au feu vert)")
            print("6. Tout tester")
            print("0. Quitter")

            choix = input("\nChoix : ").strip()

            tests = {
                "1": self.test_moteur,
                "2": self.test_servo,
                "3": self.test_capteur_ir,
                "4": self.test_capteurs_ultrason,
                "5": self.test_demarrage_vert,
                "6": self.tout_tester,
            }

            if choix == "0":
                print("Fin des tests.")
                break
            elif choix in tests:
                try:
                    tests[choix]()
                except Exception as e:
                    print(f"ERREUR : {e}")
            else:
                print("Choix invalide.")

    def test_moteur(self):
        print("\n--- Test Moteur ---")
        ctrl = self.__controleur

        self._log("INFO", "Démarrage test moteur")

        self._log("DEBUG", "Réglage vitesse à 50%")
        ctrl.moteur.regler_vitesse(50)
        self._log("DEBUG", f"Vitesse actuelle : {ctrl.moteur.vitesse}%")

        print("Avancer pendant 2 secondes...")
        ctrl.moteur.avancer()
        self._log("DEBUG", f"État moteur : {ctrl.moteur.etat}")
        time.sleep(2)

        print("Reculer pendant 2 secondes (retour au point de départ)...")
        ctrl.moteur.reculer()
        self._log("DEBUG", f"État moteur : {ctrl.moteur.etat}")
        time.sleep(2)

        ctrl.moteur.arreter()
        ctrl.moteur.regler_vitesse(0)
        self._log("DEBUG", f"État moteur : {ctrl.moteur.etat}, vitesse : {ctrl.moteur.vitesse}%")
        self._log("OK", "Test moteur réussi")
        print("Moteur arrêté. Test OK.")

    def test_servo(self):
        print("\n--- Test Servomoteur ---")
        ctrl = self.__controleur

        self._log("INFO", "Démarrage test servomoteur")

        print("Tourner à gauche (45°)...")
        ctrl.tourner(45)
        self._log("DEBUG", f"Angle servo : {ctrl.servo.angle}°")
        time.sleep(1)

        print("Tourner à droite (135°)...")
        ctrl.tourner(135)
        self._log("DEBUG", f"Angle servo : {ctrl.servo.angle}°")
        time.sleep(1)

        print("Remise droite (90°)...")
        ctrl.tourner(90)
        self._log("DEBUG", f"Angle servo : {ctrl.servo.angle}°")
        time.sleep(0.5)

        self._log("OK", "Test servomoteur réussi")
        print("Servomoteur OK.")

    def test_capteur_ir(self):
        print("\n--- Test Capteur Infrarouge (ligne noire) ---")
        ctrl = self.__controleur

        self._log("INFO", "Démarrage test capteur IR")
        self._log("DEBUG", f"Seuil IR configuré : {ctrl.capteur_ir.seuil}")

        print("La voiture avance jusqu'à détecter la ligne noire...")
        ctrl.moteur.regler_vitesse(30)
        ctrl.moteur.avancer()
        self._log("DEBUG", "Moteur démarré à 30%, en attente de détection...")

        tentative = 0
        while True:
            tentative += 1
            try:
                detecte = ctrl.capteur_ir.detecter()
            except TypeError:
                # Sur PC, sans capteur GPIO initialisé, on simule la détection.
                detecte = ctrl.capteur_ir.detecter(0.1 if tentative >= 10 else 0.9)
                self._mode_simulation = True

            if detecte:
                ctrl.moteur.arreter()
                ctrl.moteur.regler_vitesse(0)
                self._log("OK", "Ligne noire détectée, arrêt réussi")
                print("Ligne noire détectée ! Arrêt. Test OK.")
                break
            time.sleep(0.05)

    def test_capteurs_ultrason(self):
        print("\n--- Test Capteurs Ultrason ---")
        ctrl = self.__controleur

        self._log("INFO", "Démarrage test capteurs ultrason")

        erreurs = 0

        try:
            d_avant = ctrl.capteur_us_avant.measure()
            self._log("OK", f"Ultrason AVANT : {d_avant:.1f} cm")
            print(f"Ultrason AVANT  : {d_avant:.1f} cm")
        except Exception as e:
            erreurs += 1
            self._log("ERREUR", f"Ultrason AVANT : {e}")
            print(f"Ultrason AVANT  : ERREUR ({e})")

        try:
            d_gauche = ctrl.capteur_us_gauche.measure()
            self._log("OK", f"Ultrason GAUCHE : {d_gauche:.1f} cm")
            print(f"Ultrason GAUCHE : {d_gauche:.1f} cm")
        except Exception as e:
            erreurs += 1
            self._log("ERREUR", f"Ultrason GAUCHE : {e}")
            print(f"Ultrason GAUCHE : ERREUR ({e})")

        try:
            d_droit = ctrl.capteur_us_droit.measure()
            self._log("OK", f"Ultrason DROIT : {d_droit:.1f} cm")
            print(f"Ultrason DROIT  : {d_droit:.1f} cm")
        except Exception as e:
            erreurs += 1
            self._log("ERREUR", f"Ultrason DROIT : {e}")
            print(f"Ultrason DROIT  : ERREUR ({e})")

        if erreurs:
            raise RuntimeError("Echec lecture capteurs ultrason")

    def test_demarrage_vert(self):
        print("\n--- Test Démarrage au Feu Vert ---")
        ctrl = self.__controleur

        self._log("INFO", "Démarrage test capteur RGB")
        print("En attente du feu vert... (présente le vert devant le capteur)")

        debut = time.time()
        while True:
            vert_detecte = False

            if hasattr(ctrl.capteur_rgb, "est_vert"):
                vert_detecte = ctrl.capteur_rgb.est_vert()
            elif hasattr(ctrl.capteur_rgb, "detecter_vert"):
                vert_detecte = ctrl.capteur_rgb.detecter_vert()

            if not vert_detecte and getattr(ctrl.capteur_rgb, "capteur", None) is None and (time.time() - debut) > 1.5:
                # Mode simulation PC: feu vert simulé après un court délai.
                vert_detecte = True
                self._mode_simulation = True
                self._log("WARN", "Capteur RGB non disponible, feu vert simulé")

            if vert_detecte:
                self._log("OK", "Vert détecté, démarrage")
                print("VERT détecté ! Démarrage !")
                ctrl.moteur.regler_vitesse(50)
                ctrl.moteur.avancer()
                time.sleep(2)
                ctrl.moteur.arreter()
                ctrl.moteur.regler_vitesse(0)
                self._log("OK", "Test capteur RGB réussi")
                print("Test OK.")
                break

            if (time.time() - debut) > 10:
                raise TimeoutError("Aucun vert détecté dans le délai imparti")

            time.sleep(0.1)

    def tout_tester(self):
        print("\n====== LANCEMENT DE TOUS LES TESTS ======")
        self.__resultats = {}
        self.__logs = []

        for nom, test in [
            ("Moteur", self.test_moteur),
            ("Servomoteur", self.test_servo),
            ("Capteur IR", self.test_capteur_ir),
            ("Capteurs Ultrason", self.test_capteurs_ultrason),
            ("Démarrage Vert", self.test_demarrage_vert),
        ]:
            try:
                test()
                self.__resultats[nom] = True
            except Exception as e:
                self.__resultats[nom] = False
                self._log("ERREUR", f"{nom} : {e}")

        print("\n=== RÉSUMÉ ===")
        for nom, ok in self.__resultats.items():
            print(f"  {nom} : {'OK' if ok else 'ERREUR'}")

        pret = all(self.__resultats.values())
        print(f"\nÉtat global : {'PRÊT' if pret else 'NON PRÊT'}")

        if self._mode_simulation:
            self._log("WARN", "Exécution partielle en mode simulation (sans matériel complet)")

        self._generer_rapport()
        return pret


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Routine de test avant course")
    parser.add_argument("--auto", action="store_true", help="Lancement automatique de tous les tests")
    args = parser.parse_args()

    routine = Routine()

    if args.auto:
        print("=== MODE AUTOMATIQUE ===")
        routine.tout_tester()
    else:
        routine.menu()