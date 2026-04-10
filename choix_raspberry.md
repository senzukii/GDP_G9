# Choix techniques pour le projet voiture (US2)

## 1. Comparaison des plateformes

On a fait un tableau pour voir ce qui existe :

| Plateforme | Multitâche (OS) | Mémoire RAM | Connectivité | Broches GPIO | Prix |
|------------|-----------------|-------------|--------------|--------------|------|
| **Raspberry Pi 3** | **Oui (Linux / 4 cœurs)** | **1 GB** | **Wi-Fi + Bluetooth + 4x USB** | **40** | **~40€** |
| Arduino Uno R3 | Non | 2 KB | Rien | 20 | ~25€ |
| BeagleBone Black | Oui (Linux / 1 cœur) | 512 MB | Ethernet + 1x USB | 65 | ~60€ |
| Orange Pi PC | Oui (Linux / 4 cœurs) | 1 GB | Ethernet + 3x USB | 40 | ~30€ |

## 2. Pourquoi on a choisi le Raspberry Pi 3

Les raisons principales, et pour la nécessité du projet sont : le multi tâches, le WiFi, le nombres de GPiO disponibles ainsi que la RAM.

### Le multitâche, c'est super important

Déjà, avec une voiture on peut pas se permettre d'attendre.
Si le programme est en train de lire un capteur ultrason, les moteurs doivent continuer à tourner quand même.
Avec l'Arduino c'est impossible parce qu'il fait les tâches les unes après les autres.

Le Raspberry Pi par contre, avec son Linux et ses 4 cœurs, il peut gérer plein de trucs en même temps. Genre analyser la vidéo de la caméra, lire les capteurs ET contrôler les roues, tout ça en parallèle.

### Le WiFi c'est indispensable

Bon logiquement une voiture elle bouge, donc on peut pas la brancher avec un câble Ethernet...
Du coup le WiFi et Bluetooth qui sont déjà intégrés dans le Raspberry Pi 3, c'est carrément parfait. 
Avec l'Orange Pi ou le BeagleBone on aurait dû rajouter des clés USB en plus, et ça prend de la place et ça ainsi que  de la batterie pour rien.

### La RAM et les GPIO

Avec 1 GB de RAM on est tranquille pour faire tourner nos scripts Python et traiter les images de la caméra. 
Le BeagleBone avec juste 512 MB aurait peut-être galéré un peu.

Et puis les 40 broches GPIO c'est nickel pour brancher les contrôleurs de moteurs (le pont en H L298N), les servos et tous les capteurs qu'on veut.

## 3. Pourquoi Python

Pour le langage de programmation on a pris Python et voilà pourquoi :

- C'est le langage recommandé par Raspberry Pi Foundation donc la documentation est bien présente
- C'est facile à lire et rapide à coder, ça tombe bien vu qu'on a pas des masses de temps avec le Scrum, est le nombres d'user story
- Il y a plein de bibliothèques toutes faites pour gérer le matériel
- La communauté est énorme donc quand on bloque on trouve vite de l'aide

On aurait pu prendre le C/C++ mais bon c'est beaucoup plus compliqué à coder et on a pas le temps pour ça. 
Le Java c'est pas vraiment fait pour contrôler du matos directement sur Raspberry Pi.

## 4. Les bibliothèques qu'on utilise

### gpiozero

C'est une bibliothèque moderne pour contrôler les GPIO. 
Elle a des objets tout prêts genre AngularServo pour les servomoteurs ou DistanceSensor pour les capteurs ultrason. 
Ça rend le code beaucoup plus simple.

On aurait pu utiliser RPi.GPIO mais c'est plus vieux et moins pratique, le code est plus lourd avec.

### time

Pour gérer les délais et calculer les durées. 
On s'en sert notamment pour calculer les distances avec les capteurs ultrason. 
C'est une bibliothèque de base Python donc rien à installer.

### threading

Ça permet de faire tourner plusieurs tâches en même temps. 
Super important pour gérer les capteurs et les moteurs en parallèle. 
On aurait pu utiliser multiprocessing mais c'est trop lourd pour ce qu'on fait.

### logging

Pour mettre en place des logs structurés. 
C'est pratique pour débugger à distance via SSH. 
Si on avait juste fait des print() ce serait beaucoup moins pro et moins facile à suivre.

### sys

Pour gérer l'exécution du programme et arrêter proprement quand y'a des erreurs. 
Bibliothèque standard Python.

### adafruit

Celle-là elle est obligatoire pour parler avec la carte PWM (PCA9685) en I2C. 
On peut pas utiliser gpiozero ou RPi.GPIO pour ça parce qu'elles sont faites pour contrôler directement les broches du Raspberry, pas pour dialoguer avec une puce I2C.

## Conclusion

Le Raspberry Pi 3 avec Python c'est le meilleur choix pour notre projet. 
On a la puissance qu'il faut, c'est flexible, et surtout c'est simple à utiliser.

Ça nous permet de :
- Gérer en temps réel les capteurs et moteurs
- Communiquer par WiFi et SSH
- Développer vite
- Avoir un matos compatible

## Sources

- https://monraspberry.com/tableau-comparatif-des-raspberry-pi/
- https://docs.arduino.cc/hardware/uno-rev3/#tech-specs
- https://www.nvidia.com/fr-fr/autonomous-machines/embedded-systems/jetson-nano/product-development/
- https://www.moussasoft.com/beaglebone-black-rev-c-ti-am335x-cortex-a8-guide-complet-sur-cette-carte/
- https://raspberrytips.fr/pourquoi-python-sur-raspberry-pi/
- https://gpiozero.readthedocs.io/en/stable/
- Gemini
