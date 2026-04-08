from app.model.actionneurs.moteur import MoteurDC
from app.model.actionneurs.servomoteur import Servomoteur
from app.model.capteurs.capteur_infrarouge import CapteurInfrarouge
from app.model.capteurs.capteur_ultrason import HCSR04
from app.model.capteurs.capteur_rgb import CapteurRGB
from app.view.interface import Interface


class Controleur:
    def __init__(self, moteur=None, servo=None, capteur_ir=None,
                 capteur_us_avant=None, capteur_us_gauche=None, capteur_us_droit=None,
                 capteur_rgb=None, vue=None):
        self.__moteur = None
        self.__servo = None
        self.__capteur_ir = None
        self.__capteur_us_avant = None
        self.__capteur_us_gauche = None
        self.__capteur_us_droit = None
        self.__capteur_rgb = None
        self.__vue = None
        self.set_moteur(moteur or MoteurDC())
        self.set_servo(servo or Servomoteur())
        self.set_capteur_ir(capteur_ir or CapteurInfrarouge())
        self.set_capteur_us_avant(capteur_us_avant)
        self.set_capteur_us_gauche(capteur_us_gauche)
        self.set_capteur_us_droit(capteur_us_droit)
        self.set_capteur_rgb(capteur_rgb or CapteurRGB())
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
    def capteur_us_avant(self):
        return self.get_capteur_us_avant()

    @property
    def capteur_us_gauche(self):
        return self.get_capteur_us_gauche()

    @property
    def capteur_us_droit(self):
        return self.get_capteur_us_droit()

    @property
    def capteur_rgb(self):
        return self.get_capteur_rgb()

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

    def get_capteur_us_avant(self):
        return self.__capteur_us_avant

    def set_capteur_us_avant(self, capteur_us):
        self.__capteur_us_avant = capteur_us

    def get_capteur_us_gauche(self):
        return self.__capteur_us_gauche

    def set_capteur_us_gauche(self, capteur_us):
        self.__capteur_us_gauche = capteur_us

    def get_capteur_us_droit(self):
        return self.__capteur_us_droit

    def set_capteur_us_droit(self, capteur_us):
        self.__capteur_us_droit = capteur_us

    def get_capteur_rgb(self):
        return self.__capteur_rgb

    def set_capteur_rgb(self, capteur_rgb):
        self.__capteur_rgb = capteur_rgb

    def get_vue(self):
        return self.__vue

    def set_vue(self, vue):
        self.__vue = vue

    def mise_a_jour(self, valeur_ir=None, distance_avant=None):
        obstacle = self.__capteur_ir.detecter(valeur_ir)

        if distance_avant is not None:
            distance = distance_avant
        elif self.__capteur_us_avant is not None:
            distance = self.__capteur_us_avant.measure() or 999
        else:
            distance = 999

        if obstacle or distance < 20:
            self.__moteur.arreter()
        else:
            self.__moteur.avancer()

        return self.__vue.afficher_etat(self.__moteur.vitesse, obstacle, distance)

    def tourner(self, angle):
        self.__servo.tourner(angle)
