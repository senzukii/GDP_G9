# DOCUMENTATION TECHNIQUE : SÉCURITÉ ET SOURCES (US3)

Ce document regroupe les seuils de sécurité critiques pour la préservation du matériel ainsi que les ressources documentaires utilisées pour le développement du module mobile.

---

## 1. VALEURS CRITIQUES ET PRÉCAUTIONS DE SÉCURITÉ

Il est impératif de respecter les seuils de tolérance suivants pour éviter la destruction du matériel SunFounder mis à disposition, conformément aux règles de responsabilité du cahier des charges.

### 1.1. Protection du Raspberry Pi (Niveau Logique)
* **Signal ECHO des HC-SR04 :** Ces capteurs sont alimentés en 5V et renvoient un signal de 5V sur la broche ECHO.
* **Danger :** Les entrées GPIO du Raspberry Pi ne tolèrent que **3.3V** maximum.
* **Mesure de sécurité :** Un pont diviseur de tension est obligatoire entre la broche ECHO et le Raspberry Pi pour ne pas détruire le processeur.

### 1.2. Limites des Moteurs et Drivers
* **Courant de blocage (Stall Current) :** Si un moteur DC est bloqué mécaniquement, sa consommation augmente brusquement.
* **Seuil critique :** Ne pas dépasser **2.0A** par canal sur le driver L298N pour éviter une surchauffe irréversible.
* **Surveillance :** Utilisez les relevés en temps réel du capteur INA219 pour couper l'alimentation en cas de pic anormal.

### 1.3. Butées Mécaniques des Servomoteurs
* **Plage Angulaire :** Les servomoteurs sont conçus pour une rotation de **0° à 180°**.
* **Risque de casse :** Envoyer une commande PWM en dehors de ces bornes force sur les engrenages. 
* **Signal d'alerte :** Si le servomoteur émet un grognement continu, il est en butée forcée ; la commande doit être immédiatement corrigée.

### 1.4. Gestion des Batteries 18650 et PiJuice
* **Tension de seuil :** Les batteries lithium 18650 ne doivent jamais descendre en dessous de **3.0V**.
* **Danger :** Une décharge profonde rend la cellule instable et dangereuse à recharger (risque d'incendie).
* **Vérification :** Contrôlez régulièrement la tension totale via l'INA219 ou les outils de gestion du PiJuice.

| Composant | Paramètre critique | Valeur Maximale | Risque encouru |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi** | Tension GPIO (Input) | **3.3 V** | Destruction de la carte mère |
| **L298N** | Intensité par moteur | **2.0 A** | Surchauffe et court-circuit |
| **HC-SR04** | Tension d'entrée (VCC) | **5.0 V** | Destruction du capteur |
| **INA219** | Tension de bus I2C | **26.0 V** | Destruction du module de mesure |
| **Batterie 18650** | Tension de décharge | **Min 3.0 V** | Mort de la cellule |
| **Servomoteur** | Signal PWM (Angle) | **180°** | Casse des Servomoteurs |

---

## 2. SOURCES ET RESSOURCES DOCUMENTAIRES

### 2.1. Documentations Techniques (Datasheets)
* **HC-SR04 (Ultrason) :** [Lien vers la documentation](https://www.electroschematics.com/wp-content/uploads/2013/07/HCSR04-datasheet-version-1.pdf) - Détails sur la fréquence de 40 kHz et la mesure de distance.
* **TCS34725 (Couleur RGB) :** [Lien vers la documentation](https://cdn-shop.adafruit.com/datasheets/TCS34725.pdf) - Indispensable pour la détection du signal de départ.
* **INA219 (Courant/Tension) :** [Lien vers la documentation](https://www.ti.com/lit/ds/symlink/ina219.pdf) - Utilisation pour la télémétrie de la batterie.
* **PCA9685 (Driver PWM) :** [Lien vers la documentation](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf) - Gestion des signaux pour servomoteurs et moteurs DC.