from app.model.actionneurs.moteur import MoteurDC
from app.model.actionneurs.servomoteur import Servomoteur
from app.model.capteurs.capteur_infrarouge import CapteurInfrarouge
from app.model.capteurs.capteur_ultrason import CapteurUltrason
from app.view.interface import Interface


class Controleur:
    def __init__(self, moteur=None, servo=None, capteur_ir=None, capteur_us=None, vue=None):
        self.__moteur = None
        self.__servo = None
        self.__capteur_ir = None
        self.__capteur_us = None
        self.__vue = None
        self.set_moteur(moteur or MoteurDC())
        self.set_servo(servo or Servomoteur())
        self.set_capteur_ir(capteur_ir or CapteurInfrarouge())
        self.set_capteur_us(capteur_us or CapteurUltrason())
        self.set_vue(vue or Interface())

    @property
    def moteur(self):
        return self.get_moteur()

    @property
    def servo(self):
        return self.get_servo()

    @property
    def capteur_ir(self):
        return self.get_capteur_ir()

    @property
    def capteur_us(self):
        return self.get_capteur_us()

    def get_moteur(self):
        return self.__moteur

    def set_moteur(self, moteur):
        self.__moteur = moteur

    def get_servo(self):
        return self.__servo

    def set_servo(self, servo):
        self.__servo = servo

    def get_capteur_ir(self):
        return self.__capteur_ir

    def set_capteur_ir(self, capteur_ir):
        self.__capteur_ir = capteur_ir

    def get_capteur_us(self):
        return self.__capteur_us

    def set_capteur_us(self, capteur_us):
        self.__capteur_us = capteur_us

    def get_vue(self):
        return self.__vue

    def set_vue(self, vue):
        self.__vue = vue

    def mise_a_jour(self, valeur_ir, distance_cm):
        obstacle = self.__capteur_ir.detecter(valeur_ir)
        distance = self.__capteur_us.lire_distance(distance_cm)

        if obstacle or distance < 20:
            self.__moteur.arreter()
        else:
            self.__moteur.avancer()

        return self.__vue.afficher_etat(self.__moteur.vitesse, obstacle, distance)

    def tourner(self, angle):
        self.__servo.tourner(angle)
