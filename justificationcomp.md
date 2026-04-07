# RAPPORT TECHNIQUE : DOCUMENTATION DES CAPTEURS (US3)

Ce document détaille les raisons justifiant la sélection de chaque capteur pour le projet de module mobile.

---

## 1. HC-SR04 (x3)
**Pourquoi celui-là :** * **Détection d'obstacles :** Excellent rapport qualité-prix pour garantir l'évitement d'obstacles à 10 cm minimum.
* **Configuration :** L'utilisation de trois modules permet une couverture spatiale (frontale et latérale) optimisant les trajectoires sur le circuit.
* **Simplicité :** Interfaçage direct via les broches GPIO (TRIG/ECHO) permettant une lecture rapide de la distance par ultrasons.

**Pourquoi pas un autre :** * **VL53L0X (ToF) :** Plus précis mais beaucoup plus coûteux pour un usage robotique de base.
* **Capteur IR de distance :** Trop sensible à la lumière ambiante et à la couleur des obstacles pour une détection anti-collision fiable.

---

