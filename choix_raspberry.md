# RAPPORT TECHNIQUE : DOCUMENTATION DES CHOIX TECHNIQUES (US2)

# Justification du choix matériel : Le Raspberry Pi 3 pour notre véhicule robotisé

Le développement d'un projet de voiture intelligente implique des contraintes techniques fortes : le système doit pouvoir gérer plusieurs actions simultanément (piloter les moteurs, lire des capteurs, transmettre des données) tout en étant contrôlable à distance. 

Pour répondre à ce cahier des charges, nous avons comparé plusieurs plateformes embarquées. Le **Raspberry Pi 3** a été retenu car il offre l'architecture matérielle et logicielle la plus adaptée à un véhicule autonome, avec un rapport qualité/prix imbattable.

---

## 1. Comparaison des plateformes pour la robotique mobile

Le tableau ci-dessous confronte le Raspberry Pi 3 aux microcontrôleurs classiques (souvent utilisés en robotique basique) et à d'autres nano-ordinateurs concurrents :

| Plateforme | Multitâche (OS) | Mémoire (RAM) | Connectivité Native | Broches (GPIO) | Prix estimé |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Raspberry Pi 3 (Choisi)** | **Oui (Linux / Quad-Core)** | **1 GB** | **Wi-Fi, Bluetooth, 4x USB** | **40** | **~40€** |
| **Arduino Uno R3** | Non  | 2 KB | Aucune | 20 | ~25€ |
| **BeagleBone Black** | Oui (Linux / Single-Core) | 512 MB | Ethernet, 1x USB | 65 | ~60€ |
| **Orange Pi PC** | Oui (Linux / Quad-Core) | 1 GB | Ethernet, 3x USB | 40 | ~30€ |

---

## 2. Analyse des résultats et adéquation avec le projet "Voiture"

L'analyse de ces critères démontre que le Raspberry Pi 3 est la solution idéale pour motoriser et piloter notre véhicule, pour les raisons suivantes :

### A. La nécessité vitale du Multitâche (Victoire face à l'Arduino)
Dans une voiture, il est impossible d'attendre. Le système ne peut pas bloquer l'exécution du code pour attendre la réponse d'un capteur (comme un radar de recul ultrason) alors que les moteurs tournent à pleine vitesse. 
* L'Arduino exécute les instructions les unes après les autres de manière linéaire. 
* **Le Raspberry Pi 3**, grâce à son système d'exploitation Linux et son processeur à 4 cœurs (Quad-Core), gère le **multitâche de manière fluide**. Il peut exécuter un script Python pour analyser un flux vidéo (caméra), pendant qu'un autre script lit les capteurs de distance, et qu'un troisième ajuste la vitesse des roues (PWM).

### B. Le pilotage et WiFi (Victoire face à l'Orange Pi et BeagleBone)
Un véhicule est par nature mobile : il ne peut pas être relié par un câble réseau (Ethernet). 
* L'Orange Pi PC et le BeagleBone Black nécessiteraient l'ajout de clés USB Wi-Fi ou Bluetooth externes, ce qui occupe de la place sur le châssis, consomme plus d'énergie et pose des problèmes de pilotes.
* **Le Raspberry Pi 3 intègre nativement le Wi-Fi et le Bluetooth.** 

### C. RAM et GPIO : Le dimensionnement parfait
Pour une voiture, nous avons besoin de mémoire pour le traitement de données (ex: analyse d'images, cartographie, serveur web embarqué) et de broches physiques pour le matériel.
* Avec ses **40 broches GPIO**, le Raspberry Pi permet de brancher directement les contrôleurs de moteurs (ex: pont en H L298N), les servos de direction et de multiples capteurs.
* Son **1 GB de RAM** est amplement suffisant pour faire tourner nos algorithmes de contrôle en Python, là où les 512 MB du BeagleBone risqueraient de saturer en cas d'utilisation d'une caméra.

---

## Conclusion

Le **Raspberry Pi 3** a été choisi car c'est le "cerveau" parfait pour notre voiture. Il écrase les microcontrôleurs grâce à sa capacité à gérer le multitâche complexe (vision + déplacement simultanés), et il bat ses concurrents SBC grâce à son Wi-Fi/Bluetooth natif indispensable pour un véhicule sans fil, le tout en respectant notre budget.

## 3. Justification du choix de Python

### Pourquoi celui-là :
* **Support officiel :** Python est le langage recommandé par la Raspberry Pi Foundation.
* **Lisibilité et rapidité de développement :** Permet une implémentation rapide pour un projet court (Scrum).
* **Écosystème riche :** Large disponibilité de bibliothèques adaptées au matériel embarqué.
* **Communauté :** Documentation abondante facilitant la résolution de problèmes.

### Pourquoi pas un autre :
* **C/C++ :** Plus performant mais plus complexe à développer et maintenir dans un temps limité.
* **Java :** Moins utilisé pour l’interaction bas niveau avec le matériel Raspberry Pi.
* **Langages bas niveau :** Moins adaptés à un projet nécessitant rapidité de développement et flexibilité.

---

## 4. Bibliothèques Python utilisées

## 4.1 gpiozero
**Pourquoi celle-là :**
* Bibliothèque moderne pour le contrôle des GPIO.
* Fournit des objets "prêts à l'emploi" (ex: `AngularServo` pour le servomoteur, `DistanceSensor` pour les capteurs ultrasons).
* Facilite grandement l'écriture de tests unitaires (via les *mocks*).

**Pourquoi pas une autre :**
* **RPi.GPIO :** Bibliothèque vieillissante et de plus bas niveau.  Ce qui rend le code plus lourd, moins lisible et plus difficile à maintenir.

---

### 4.2 time
**Pourquoi celle-là :**
* Gestion des délais et mesure des durées.
* Utilisée pour le calcul de distance avec les capteurs ultrason.

**Pourquoi pas une autre :**
* Bibliothèque native suffisante, aucune alternative nécessaire.

---

### 4.3 threading
**Pourquoi celle-là :**
* Permet l’exécution simultanée de plusieurs tâches.
* Indispensable pour gérer capteurs et moteurs en parallèle.

**Pourquoi pas une autre :**
* **multiprocessing :** Plus lourd et inutile pour ce type d’application embarquée légère.

---

### 4.4 logging
**Pourquoi celle-là :**
* Mise en place d’un système de logs structuré.
* Permet le diagnostic à distance via SSH.

**Pourquoi pas une autre :**
* Utilisation de `print()` insuffisante pour un suivi structuré et professionnel.

---

### 4.5 sys
**Pourquoi celle-là :**
* Gestion de l’exécution et arrêt contrôlé du programme.
* Utile pour gérer les erreurs et les fins de processus.

**Pourquoi pas une autre :**
* Bibliothèque standard suffisante pour ce besoin.

---

### 4.6 adafruit
**Pourquoi celle-là :**
* Indispensable pour communiquer avec la carte PWM intermédiaire (PCA9685) via le protocole I2C.
* Permet d'exploiter le signal PWM matériel de la carte PCA9685

**Pourquoi pas une autre :**
* **gpiozero / RPi.GPIO :** Incompatibles avec ce module spécifique, car elles sont conçues pour des signaux électriques directs sur les broches du Raspberry Pi, et non pour dialoguer avec une puce I2C.

---

## Conclusion

Le choix du Raspberry Pi 3 Model B associé à Python est parfait pour puissance, flexibilité et simplicité.
Cette combinaison permet de répondre efficacement au  projet :
- gestion en temps réel des capteurs et moteurs  
- communication réseau via SSH  
- développement rapide
- compatibilité complète avec le matériel  

---

## Sources

- https://monraspberry.com/tableau-comparatif-des-raspberry-pi/  
- https://docs.arduino.cc/hardware/uno-rev3/#tech-specs  
- https://fr.wikipedia.org/wiki/ESP32  
- https://www.nvidia.com/fr-fr/autonomous-machines/embedded-systems/jetson-nano/product-development/  
- https://www.moussasoft.com/beaglebone-black-rev-c-ti-am335x-cortex-a8-guide-complet-sur-cette-carte/  
- https://raspberrytips.fr/pourquoi-python-sur-raspberry-pi/  
- https://gpiozero.readthedocs.io/en/stable/  
- Gemini  
