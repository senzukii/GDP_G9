from app.controller.controleur import Controleur
from app.model.actionneurs.moteur import MoteurDC
from app.model.capteurs.capteur_ultrason import HCSR04
from logger import setup_logger

import threading
import time
import atexit
import signal

# ═══════════════════════════════════════════════════════════════════════════════
#  PARAMÈTRES AJUSTÉS (Ligne droite plus douce + détection murs arrondis)
# ═══════════════════════════════════════════════════════════════════════════════

VITESSE_COURSE  = 35    # On baisse à 35 pour donner le temps aux capteurs de lire
VITESSE_MIN     = 20    

# Ligne droite : KP plus bas pour éviter de slalomer, KD haut pour stabiliser
KP         = 0.7   
KD         = 1.2   

# Virage : On garde tes valeurs qui marchaient bien
KP_VIRAGE  = 0.6   
KD_VIRAGE  = 1.4   

SEUIL_AVANT_STOP   = 12   
SEUIL_LATERAL_MUR  = 8    
SEUIL_VIRAGE_DEG   = 18   
MAX_DELTA_ANGLE    = 7    
CYCLES_BLOQUE_MAX    = 5    
DUREE_MARCHE_ARRIERE = 0.6  

ANGLE_CENTRE = 90
ANGLE_MIN    = 50
ANGLE_MAX    = 130
FREQ_HZ = 50

# ═══════════════════════════════════════════════════════════════════════════════

class Course:

    def __init__(self):
        self._logger = setup_logger("COURSE")
        self._ctrl = Controleur()
        self._initialiser_materiel()

        # On stocke les dernières distances valides pour compenser les "None" dans les virages
        self._distances = {"avant": 100.0, "gauche": 20.0, "droite": 20.0}
        self._lock = threading.Lock()
        self._thread_actif = False
        self._angle_courant = ANGLE_CENTRE
        self._cycles_bloque = 0

        atexit.register(self._cleanup_gpio)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT,  self._signal_handler)

    def _initialiser_materiel(self):
        self._logger.info("Initialisation matérielle...")
        ctrl = self._ctrl
        ctrl.set_moteur(MoteurDC(canal=[5, 4], pins_direction=[18, 4, 22, 27]))
        ctrl.set_capteur_us_avant( HCSR04(trigger_pin=16, echo_pin=25))
        ctrl.set_capteur_us_gauche(HCSR04(trigger_pin=11, echo_pin=9))
        ctrl.set_capteur_us_droit( HCSR04(trigger_pin=26, echo_pin=19))
        if ctrl.capteur_ir:
            try: ctrl.capteur_ir.setup()
            except: pass

    def _lire_capteur_safe(self, capteur, timeout=0.06):
        if not self._thread_actif: return None
        resultat = [None]
        def _worker():
            try: resultat[0] = capteur.measure()
            except: pass
        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        t.join(timeout)
        return resultat[0]

    def _thread_ultrasons(self):
        ctrl = self._ctrl
        capteurs = [("avant", ctrl.capteur_us_avant), ("gauche", ctrl.capteur_us_gauche), ("droite", ctrl.capteur_us_droit)]
        while self._thread_actif:
            for nom, capteur in capteurs:
                if capteur is None: continue
                val = self._lire_capteur_safe(capteur)
                if val is not None and 2.0 < val < 400.0:
                    with self._lock:
                        self._distances[nom] = val
                # Si val est None, on ne fait rien : on garde l'ancienne valeur (Maintien de Cap)

    def _get_distances(self):
        with self._lock:
            return dict(self._distances)

    def _attendre_feu_vert(self):
        self._logger.info("Attente signal RGB...")
        while True:
            try:
                if self._ctrl.capteur_rgb.est_vert(): return
            except: pass
            time.sleep(0.05)

    def _pd_angle(self, gauche, droite, erreur_prec, dt):
        erreur = gauche - droite
        d_erreur = (erreur - erreur_prec) / dt if dt > 1e-4 else 0.0
        
        # Sélection des gains
        en_v = abs(self._angle_courant - ANGLE_CENTRE) > SEUIL_VIRAGE_DEG
        kp = KP_VIRAGE if en_v else KP
        kd = KD_VIRAGE if en_v else KD
        
        correction = kp * erreur + kd * d_erreur
        angle_cible = ANGLE_CENTRE - correction
        angle_cible = max(ANGLE_MIN, min(ANGLE_MAX, angle_cible))
        
        # Lissage du mouvement du servo
        delta = angle_cible - self._angle_courant
        delta = max(-MAX_DELTA_ANGLE, min(MAX_DELTA_ANGLE, delta))
        return self._angle_courant + delta, erreur

    def _marche_arriere(self, gauche, droite):
        self._logger.warning("BLOCAGE ! Recul de secours.")
        self._ctrl.moteur.arreter()
        time.sleep(0.1)
        # On tourne à l'opposé du mur le plus proche
        if gauche >= droite: self._ctrl.tourner(ANGLE_MAX)
        else: self._ctrl.tourner(ANGLE_MIN)
        self._ctrl.moteur.regler_vitesse(45)
        self._ctrl.moteur.reculer()
        time.sleep(DUREE_MARCHE_ARRIERE)
        self._ctrl.moteur.arreter()
        self._ctrl.tourner(ANGLE_CENTRE)
        time.sleep(0.1)

    def demarrer(self):
        self._attendre_feu_vert()
        self._thread_actif = True
        self._t_us = threading.Thread(target=self._thread_ultrasons, daemon=True)
        self._t_us.start()
        
        time.sleep(0.5)
        self._ctrl.moteur.regler_vitesse(VITESSE_COURSE)
        self._ctrl.moteur.avancer()

        erreur_prec = 0.0
        t_prec = time.monotonic()
        
        try:
            while True:
                dt = time.monotonic() - t_prec
                if dt < (1.0/FREQ_HZ): continue
                t_prec = time.monotonic()

                dist = self._get_distances()
                av, ga, dr = dist["avant"], dist["gauche"], dist["droite"]

                # --- LOGIQUE DE BLOCAGE AMÉLIORÉE ---
                # On recule si l'avant est < seuil OU si on est très près d'un mur latéral
                if av < SEUIL_AVANT_STOP or min(ga, dr) < 4.0: 
                    self._cycles_bloque += 1
                else:
                    self._cycles_bloque = 0

                if self._cycles_bloque >= CYCLES_BLOQUE_MAX:
                    self._marche_arriere(ga, dr)
                    self._ctrl.moteur.avancer()
                    continue

                # --- CALCUL DIRECTION ---
                angle, erreur_prec = self._pd_angle(ga, dr, erreur_prec, dt)
                self._angle_courant = angle
                self._ctrl.tourner(int(angle))

                # Vitesse adaptative
                v = VITESSE_COURSE
                if abs(angle - ANGLE_CENTRE) > 15: v = VITESSE_MIN + 5
                self._ctrl.moteur.regler_vitesse(int(v))

                self._logger.debug(f"RUN | G:{ga:.1f} D:{dr:.1f} AV:{av:.1f} | Ang:{int(angle)}")

        except Exception as e:
            self._logger.critical(f"Crash: {e}", exc_info=True)
            self._arreter()

    def _arreter(self, raison="Stop"):
        self._thread_actif = False
        self._ctrl.moteur.arreter()
        self._ctrl.tourner(ANGLE_CENTRE)

    def _cleanup_gpio(self):
        self._thread_actif = False
        try: self._ctrl.moteur.arreter()
        except: pass

    def _signal_handler(self, signum, frame):
        self._arreter()
        exit(0)

if __name__ == "__main__":
    Course().demarrer()
