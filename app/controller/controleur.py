from app.model.actionneurs.moteur import MoteurDC
from app.model.actionneurs.servomoteur import Servomoteur
from app.model.capteurs.capteur_infrarouge import CapteurInfrarouge
from app.model.capteurs.capteur_ultrason import CapteurUltrason
from app.view.interface import Interface


class Controleur:
    def __init__(self, moteur=None, servo=None, capteur_ir=None, capteur_us=None, vue=None):
        self.moteur = moteur or MoteurDC()
        self.servo = servo or Servomoteur()
        self.capteur_ir = capteur_ir or CapteurInfrarouge()
        self.capteur_us = capteur_us or CapteurUltrason()
        self.vue = vue or Interface()

    def mise_a_jour(self, valeur_ir, distance_cm):
        obstacle = self.capteur_ir.detecter(valeur_ir)
        distance = self.capteur_us.lire_distance(distance_cm)

        if obstacle or distance < 20:
            self.moteur.arreter()
        else:
            self.moteur.avancer()

        return self.vue.afficher_etat(self.moteur.vitesse, obstacle, distance)

    def tourner(self, angle):
        self.servo.tourner(angle)
