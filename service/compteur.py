from app.controller.controleur import Controleur
from app.model.actionneurs.moteur import MoteurDC
import time


class TestInfrarouge3Passages:
    def __init__(self):
        self.controleur = Controleur()

        # Initialise le moteur physique si nécessaire
        self.controleur.set_moteur(
            MoteurDC(
                canal=[5, 4],
                pins_direction=[18, 4, 22, 27]
            )
        )

        # Initialise le capteur IR si nécessaire
        if self.controleur.capteur_ir is not None:
            try:
                self.controleur.capteur_ir.setup()
            except Exception as e:
                print(f"Erreur initialisation capteur IR : {e}")

    def lancer(self):
        print("\n=== TEST CAPTEUR INFRAROUGE : ARRET APRES 3 PASSAGES ===")
        print("Le robot démarre derrière la ligne noire.")
        print("Le premier passage détecté est ignoré grâce au compteur à -1.")
        print("Le robot s'arrête au 3e vrai passage sur la ligne noire.\n")

        moteur = self.controleur.moteur
        capteur_ir = self.controleur.capteur_ir

        if moteur is None:
            print("Erreur : moteur non initialisé.")
            return

        if capteur_ir is None:
            print("Erreur : capteur infrarouge non initialisé.")
            return

        compteur_passages = -1
        etat_precedent = False

        try:
            moteur.regler_vitesse(25)
            moteur.avancer()

            while True:
                etat_actuel = capteur_ir.detecter()  # True si ligne noire détectée
                valeur_brute = capteur_ir.lire()

                print(
                    f"IR brut={valeur_brute} | ligne_noire={etat_actuel} | passages={compteur_passages}",
                    end="\r"
                )

                # On compte uniquement lors du front montant : blanc -> noir
                if etat_actuel and not etat_precedent:
                    compteur_passages += 1
                    print(f"\nPassage détecté ! Compteur = {compteur_passages}")

                    if compteur_passages >= 3:
                        moteur.arreter()
                        print("\n✅ Arrêt du robot : 3 passages sur la ligne noire détectés.")
                        break

                etat_precedent = etat_actuel
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\nArrêt manuel demandé.")
        except Exception as e:
            print(f"\nErreur pendant le test : {e}")
        finally:
            try:
                moteur.arreter()
            except Exception:
                pass


if __name__ == "__main__":
    test = TestInfrarouge3Passages()
    test.lancer()