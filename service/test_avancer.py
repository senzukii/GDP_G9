#!/usr/bin/env python3
"""
Test ULTRA simple - juste gauche/droite
"""

from app.model.actionneurs.servomoteur import Servomoteur
import time

print("Test ultra-simple du servo\n")

# Changez le canal si nécessaire (0, 1, 2, ou 3)
servo = Servomoteur(canal=0)

print("Milieu (90°)...")
servo.milieu()
time.sleep(2)

print("Gauche (45°)...")
servo.gauche()
time.sleep(2)

print("Droite (135°)...")
servo.droite()
time.sleep(2)

print("Retour milieu (90°)...")
servo.milieu()

print("\nTerminé !")