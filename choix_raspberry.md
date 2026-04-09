# RAPPORT TECHNIQUE : DOCUMENTATION DES CHOIX TECHNIQUES (US2)

Document complet et justificatif du choix de Raspberry Pi ainsi que l'utilisation de Python.

---

## 1. Comparaison des plateformes embarquées

| CRITÈRE | RASPBERRY PI 3 B | ARDUINO UNO | ESP32 | NVIDIA JETSON NANO | BEAGLEBONE BLACK |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Prix** | ~35-40€ | ~20-25€ | ~10-15€ | ~100-150€ | ~50-60€ |
| **Processeur** | Quad-core 1.2 GHz | 16 MHz | Dual-core 240 MHz | Quad-core 1.43 GHz | 1 GHz ARM |
| **RAM** | 1 GB | 2 KB | 520 KB | 2-4 GB | 512 MB |
| **GPIO** | 40 pins | 14 digital, 6 analog | 36 pins | 40 pins | 65 pins |
| **Langages** | Python, C++, Java | C/C++ | C/C++, Python | Python, C++ | Python, C++ |
| **Système d'exploitation** | Raspbian (Linux) | Aucun | FreeRTOS | Ubuntu | Debian |
| **Consommation** | ~2.5W | ~0.5W | ~0.5W | ~10W | ~2W |
| **Multitâche** | Oui | Non | Oui | Oui | Oui |

---

## 2. Raspberry Pi 3 Model B

### Pourquoi celui-là :
* **Compatibilité logicielle :** Support natif de Python avec accès direct aux bibliothèques GPIO nécessaires au projet.
* **Puissance de calcul :** Parfaite pour exécuter des algorithmes de navigation, de détection et de gestion en temps réel.
* **Connectivité intégrée :** WiFi embarqué permettant une connexion SSH.
* **Multitâche :** Système Linux permettant l’exécution simultanée de plusieurs processus (capteurs, moteurs, logs, réseau).
* **Connectique :** 40 GPIO parfait pour connecter tous les composants.

### Pourquoi pas un autre :
* **Arduino Uno :** Trop limité (absence de système d’exploitation, pas de multitâche,...).
* **ESP32 :** Intéressant mais moins adapté à une architecture Linux complète avec gestion avancée (logs, SSH).
* **Jetson Nano :** Trop puissant et énergivore pour ce type de projet.
* **BeagleBone Black :** Alternative viable mais moins accessible en termes de documentation et d’écosystème que Raspberry Pi.

---

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

### 4.5 adafruit
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