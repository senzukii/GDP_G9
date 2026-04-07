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

## 2. Capteur Infrarouge (Suiveur de ligne)
**Pourquoi celui-là :** * **Précision :** Indispensable pour reconnaître la ligne d'arrivée avec un arrêt immédiat et précis à moins de 5 cm.
* **Réactivité :** Fournit un signal binaire instantané pour une détection de ligne en temps réel sans latence de traitement.

**Pourquoi pas un autre :** * **Caméra OpenCV :** Trop gourmande en ressources processeur, risquant de ralentir la boucle de contrôle principale.
* **Capteur de couleur :** Moins réactif que l'infrarouge spécifique pour le suivi de ligne à haute vitesse.

---

## 3. TCS3472 (Capteur de couleur RGB)
**Pourquoi celui-là :** * **Automatisation :** Permet au module de détecter un signal de départ (comme un feu vert) pour un démarrage automatisé sans intervention humaine.
* **Protocole :** Utilise le bus I2C (SDA/SCL), garantissant une lecture numérique stable et précise des composantes colorimétriques.

**Pourquoi pas un autre :** * **TCS3200 :** Produit une fréquence proportionnelle à l'intensité, ce qui est techniquement plus complexe à traiter que l'interface I2C.

---

## 4. INA219 (Moniteur d'énergie)
**Pourquoi celui-là :** * **Télémétrie :** Mesure la tension et le courant via I2C pour surveiller l'état des batteries 18650 en temps réel.
* **Diagnostic :** Crucial pour identifier les baisses de tension lors des accélérations et alimenter les logs et diagnostics exigés.

**Pourquoi pas un autre :** * **ACS712 :** Sortie analogique nécessitant un convertisseur externe, compliquant l'intégration sur une architecture numérique sans entrées analogiques natives.

---
