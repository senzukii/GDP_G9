#!/usr/bin/env python3
"""
Test physique simple du moteur DC
Ce script fait avancer puis reculer le robot pendant 1 seconde chaque fois.
Utilisation sécurisée avec vitesse modérée.
"""

import time
import sys
from pathlib import Path

# Ajouter le chemin du module moteur si nécessaire
# sys.path.append('/chemin/vers/votre/module')

from app.model.actionneurs.moteur import MoteurDC

def test_avancer_reculer():
    """
    Test simple : avancer 1s puis reculer 1s
    Vitesse modérée pour la sécurité du matériel
    """
    print("=== Test Moteur DC ===")
    print("Ce test va faire avancer puis reculer le robot")
    print("Assurez-vous que le robot a de l'espace!\n")
    
    # Attendre confirmation
    input("Appuyez sur ENTER pour démarrer le test...")
    
    try:
        # Initialisation du moteur
        # Configuration pour L298N avec PCA9685
        print("\n1. Initialisation du moteur...")
        moteur = MoteurDC(
            canal=[5, 4],  # ENA et ENB sur canaux 5 et 4
            pins_direction=[17, 27, 22, 23]  # IN1, IN2, IN3, IN4
        )
        print("Moteur initialisé")
        
        # Vitesse sécurisée (30% de la puissance max)
        vitesse_test = 30
        moteur.regler_vitesse(vitesse_test)
        print(f"✓ Vitesse réglée à {vitesse_test}%")
        
        # Phase 1: Avancer
        print("\n2. AVANT pendant 1 seconde...")
        moteur.avancer()
        time.sleep(1.0)
        
        # Arrêt intermédiaire pour sécurité
        print("Arrêt")
        moteur.arreter()
        time.sleep(0.5)
        
        # Phase 2: Reculer
        print("\n3. ARRIÈRE pendant 1 seconde...")
        moteur.reculer()
        time.sleep(1.0)
        
        # Arrêt final
        print("Arrêt final")
        moteur.arreter()
        
        print("\n=== Test terminé avec succès ===")
        print(f"État final: {moteur.lire_etat()}")
        print(f"Vitesse: {moteur.lire_vitesse()}%")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrompu par l'utilisateur")
        moteur.arreter()
        print("Moteur arrêté en urgence")
        
    except Exception as e:
        print(f"\n Erreur durant le test: {e}")
        print("Arrêt du moteur par sécurité...")
        try:
            moteur.arreter()
        except:
            pass
        sys.exit(1)

def test_vitesse_progressive():
    """
    Test optionnel: augmentation progressive de la vitesse
    Permet de vérifier le bon fonctionnement à différentes puissances
    """
    print("\n=== Test Vitesse Progressive ===")
    input("Appuyez sur ENTER pour démarrer...")
    
    try:
        moteur = MoteurDC(
            canal=[5, 4],
            pins_direction=[17, 27, 22, 23]
        )
        
        vitesses = [20, 30, 40, 50]
        
        for v in vitesses:
            print(f"\nTest à {v}% de vitesse...")
            moteur.regler_vitesse(v)
            
            print("  Avant...")
            moteur.avancer()
            time.sleep(0.5)
            
            moteur.arreter()
            time.sleep(0.3)
            
        print("\n✓ Test terminé")
        moteur.arreter()
        
    except KeyboardInterrupt:
        print("\nTest interrompu")
        moteur.arreter()
    except Exception as e:
        print(f"Erreur: {e}")
        try:
            moteur.arreter()
        except:
            pass

if __name__ == "__main__":
    print("Tests disponibles:")
    print("1. Test simple (avancer/reculer 1s)")
    print("2. Test vitesse progressive")
    print("3. Les deux tests")
    
    choix = input("\nVotre choix (1/2/3): ").strip()
    
    if choix == "1":
        test_avancer_reculer()
    elif choix == "2":
        test_vitesse_progressive()
    elif choix == "3":
        test_avancer_reculer()
        print("\n" + "="*50 + "\n")
        test_vitesse_progressive()
    else:
        print("Choix invalide")