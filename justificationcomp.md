# RAPPORT TECHNIQUE : DOCUMENTATION DES COMPOSANTS (US3)

Ce document explique le fonctionnement des composants qu'on a utilisés dans notre projet.

---

## 1. HC-SR04 — Capteur Ultrason

### Comment ça marche

Le HC-SR04 envoie une onde ultrasonique sur un obstacle, ca ricoche et attend qu'elle revienne vers le capteur.

ultrasonique = une brève émission d'ondes sonores à haute fréquence (supérieure à 20 kHz), inaudibles pour l'oreille humaine

Le HC-SR04 fonctionne avec 5V et le raspberry pi 3,3 V donc un diviseur de tension est necessaire.

Le diviseur de tension consiste à  mettre min 2 resistances en serie et ca va diminuer la tension.

Pas resistances en parallèles car ca va augmenter juste le courant et la tension va pas bouger donc ca va juste être pire.

Le capteur a 4 broches :

| Broche | Nom | Rôle |
| :--- | :--- | :--- |
| 1 | **VCC** | Alimentation +5V |
| 2 | **TRIG** | On envoie un pulse de 10µs pour déclencher une mesure |
| 3 | **ECHO** | Reste à HIGH le temps que l'onde fasse l'aller-retour |
| 4 | **GND** | Masse (0V) |

*Voir image schemaHCSR04.png*

Concrètement, voilà ce qui se passe à chaque mesure :
HIGH = 1
LOW = 0

1. Le RPI va envoyer une impulsion electrique de 10 micro secondes à la broche trig du capteur pour lui dire d'envoyer une onde afin de détecter un obstacle
2. Le capteur envoie 8 pulses ultrasoniques à 40 kHz et ca rebondit sur l'obstacle
3. ECHO passe à HIGH dès que l'onde part
4. ECHO repasse à LOW quand l'onde revient
5. On mesure combien de temps ECHO est resté HIGH, et ca calcule la distance 

### Calcul de la distance

La formule utilisée est :

**d = (t × 340) / 2**

- **t** = temps pendant lequel ECHO est resté à HIGH (en secondes)
- **340** = vitesse du son en m/s à température ambiante
- **/ 2** parce que l'onde fait l'aller ET le retour, donc on divise par 2 pour avoir juste la distance jusqu'à l'obstacle

Exemple : si ECHO reste HIGH pendant 0.006s → d = (0.006 × 340) / 2 = **1,02 mètre**

### Pourquoi c'est pas trop précis

Plusieurs choses peuvent fausser la mesure. La température joue sur la vitesse du son, donc si la salle est froide la mesure sera légèrement différente. Si l'obstacle est incliné, l'onde repart dans une autre direction et ne revient pas vers le capteur. Et entre deux mesures il faut attendre environ 60ms, ce qui peut poser problème si la voiture va vite.

C'est pour ca qu'il y a 3 capteurs : un devant, un à gauche, un à droite car si un donne une mauvaise valeur les deux autres compensent.


### Utilité dans notre projet ?

Dans notre projet, les 3 capteurs servent à détecter les obstacles sur le circuit (autres véhicules, parois) et à éviter les collisions. 

La détection se fait à partir de 10 cm minimum. 

L'évitement doit être réalisé en moins de 15 secondes comme demandé dans le cahier de charges.

---

## 2. Capteur Infrarouge — Suiveur de ligne

### Comment ça marche

Le capteur infrarouge est un capteur digital qui est divisé en 2 parties : l'emetteur (LED) et le recepteur (photodiode).

Il permet de détecter la présence d’un objet en mesurant la lumière infrarouge réfléchie par une surface.

Il y a 3 broches au capteur : 

| Broche | Nom | Rôle |
| :--- | :--- | :--- |
| 1 | **VCC** | Alimentation +5V |
| 2 | **OUT** | De là ca envoie données 0 ou 1 au RPI |
| 3 | **GND** | Masse (0V) |

L'emetteur envoie de la lumière infrarouge vers le sol et regarde ce qui revient. Sur une surface blanche beaucoup de lumière est réfléchie, le capteur renvoie HIGH. Sur la ligne noire d'arrivée la lumière est absorbée, le capteur renvoie LOW.

Le capteur sait si c'est blanc car ca va reflechir beaucoup de lumiere donc beaucoup de signal -> HIGH

Le capteur sait si c'est noir car ca va absorber la lumière donc moins de signal -> LOW

### Pourquoi la lumière réfléchit ou absorbe

C'est de la physique optique basique : une surface claire (blanche) réfléchit la majorité des rayons lumineux, peu importe la longueur d'onde. Une surface sombre (noire) absorbe la lumière et la convertit en chaleur au lieu de la renvoyer. Le capteur IR exploite exactement ce principe.

La réponse est **digitale** : le capteur renvoie uniquement **0 ou 1**, pas une valeur intermédiaire. C'est soit la ligne est détectée, soit elle ne l'est pas.

### Utilité dans notre projet ?

Dans notre projet, il sert uniquement à détecter la ligne d'arrivée.

Quand le capteur passe au-dessus de la ligne noire, il renvoie LOW et la voiture s'arrête.

L'arrêt doit être précis à moins de 5 cm de la ligne.

---

## 3. TCS3472 — Capteur de couleur RGB

### Comment ça marche
Le capteur mesure la lumière réfléchie par un objet. Grâce à ses photodiodes avec filtres rouge, vert et bleu, il décompose la lumière en composantes R, G et B. Ces valeurs sont ensuite converties en données numériques et envoyées au Raspberry Pi via le bus I2C. Le Raspberry Pi traite ces données pour déterminer la couleur de l'objet. 

Il y a 7 broches au capteur mais 4 sont les plus importantes : 

| Broche | Nom | Rôle |
| :--- | :--- | :--- |
| 1 | **VIN** | Alimentation +5V |
| 2 | **GND** | Masse (0V)  |
| 3 | **SCL** | Le fil qui transporte les données |
| 4 | **SDA** | Le fil qui synchronise l'échange pour que les données soient lues au bon moment (si pas bien synchro, données éronnées envoyées) |

Dans notre projet on s'en sert pour détecter le feu vert de départ. Quand la valeur verte dépasse un certain seuil qu'on définit dans le code, la voiture démarre toute seule.

C'est ce qui correspond au départ automatisé demandé dans le cahier de charges — la voiture démarre sans intervention humaine dès que le feu vert est détecté.

Le bus I2C est le bus qu'on a utilisé car : 

* Il est bidirectionnel

* Il permet de synchroniser des discussions avec plusieurs capteurs et n'utilise que 2 fils (sda pour les données et scl pour la synchronisation des données)

* Il est simple car il est facile à implémenter.

* Il est beaucoup plus utile que le bus uart car ce dernier fonctionne uniquement en point à point.

Le point négatif de l'I2C c'est le fait qu'il soit moins adapté au traffic longue distance.


Le TCS3472 envoie directement des nombres via I2C, c'est beaucoup plus simple à exploiter.

---

## 4. INA219 — Moniteur d'énergie

Le cahier de charges demande de pouvoir accéder aux logs et diagnostics à distance via SSH. L'INA219 alimente ces logs avec les données de consommation en temps réel.

### Comment ça marche

L'INA219 mesure la tension et le courant des batteries en temps réel.

Il envoie ces valeurs au Raspberry Pi via le bus I2C. Ensuite c'est le programme sur le Raspberry Pi qui peut détecter si les valeurs sont anormales et dans ce cas arrêter le système pour protéger les composants.

Lui aussi passe par le bus I2C, donc il partage les mêmes fils SDA et SCL que les autres capteurs. Pour que le Pi sache à qui il parle, chaque composant I2C a sa propre adresse sur le bus.

Il y a plusieurs broches sur le capteur mais les principales sont :

| Broche | Nom | Rôle |
| :--- | :--- | :--- |
| 1 | **VIN** | Alimentation +5V |
| 2 | **GND** | Masse (0V)  |
| 3 | **SCL** | Le fil d'horloge I2C qui synchronise la communication |
| 4 | **SDA** | Le fil de données I2C |
| 5 | **VIN +** | Entrée mesure tension côté batterie / charge |
| 6 | **VIN -** | Sortie vers la charge (mesure du courant) |

### Comment il mesure le courant physiquement

Entre VIN+ et VIN- il y a une très petite résistance appelée **résistance shunt**. Quand le courant passe à travers, ça crée une minuscule différence de tension aux deux bornes. L'INA219 mesure cette différence et applique la loi d'Ohm (**I = U / R**) pour calculer le courant exact. C'est invisible pour le reste du circuit car la résistance est tellement petite qu'elle ne perturbe rien.

### Pourquoi on en a besoin

Pendant la course les moteurs consomment beaucoup, surtout en accélération. L'INA219 nous permet de surveiller que les batteries tiennent et d'enregistrer les données dans les logs. Ces logs sont ensuite consultables à distance via SSH ce qui correspond à ce qui est demandé dans l'US6.

---

## 5. Servomoteur — Direction

### Comment ça marche

Le servomoteur c'est ce qui fait tourner les roues avant. Contrairement aux moteurs DC qui tournent en continu, lui se positionne à un angle précis et y reste. C'est ce qui permet de diriger la voiture.

Il est contrôlé par un signal PWM.

Le PWM (Pulse Width Modulation) c'est un signal électrique qui alterne entre ON (HIGH) et OFF (LOW) très rapidement. Ce qui change, c'est la durée du temps où le signal reste à HIGH.

Cette durée s'appelle le "temps d'impulsion" et elle permet de définir la position du servo :

une petite impulsion → angle vers la gauche
une impulsion moyenne → position au centre
une grande impulsion → angle vers la droite

Donc plus le signal reste longtemps à l'état HIGH, plus le servo tourne dans un sens.

En général, le servo fonctionne à une fréquence d'environ 50 Hz (20 ms par cycle), et c'est la largeur de l'impulsion (en ms) qui détermine l'angle (souvent entre ~1 ms et ~2 ms).

=> 1 ms → 0° (gauche)

   1,5 ms → 90° (centre)
   
   2 ms → 180° (droite)

Le servo est branché sur le driver PCA9685 et pas directement sur le Pi. Le PCA9685 communique en I2C avec le Pi et génère lui-même les signaux PWM. Ça évite de surcharger le Pi avec cette tâche et ça permet de gérer plusieurs servos en même temps.

---

## 6. Moteurs DC — Propulsion

### Comment ça marche

Les deux moteurs DC font avancer ou reculer la voiture. Leur vitesse se règle aussi avec un signal PWM, même principe que le servo — plus le signal est longtemps à HIGH, plus le moteur tourne vite.

Par contre ils ne sont pas branchés directement sur le Pi. Les broches GPIO du Raspberry sortent du 3,3V et quelques milliampères maximum, c'est beaucoup trop faible pour alimenter un moteur. C'est là que le driver L298N entre en jeu.

### Le pont en H

Le L298N contient ce qu'on appelle un pont en H. C'est un circuit avec 4 interrupteurs électroniques placés en forme de H autour du moteur. Selon quels interrupteurs sont activés, le courant passe dans un sens ou dans l'autre dans le moteur :

S1 + S4 fermés → courant traverse le moteur dans un sens → rotation en avant

S2 + S3 fermés → courant traverse dans l'autre sens → rotation en arrière

S1 + S3 fermés → court-circuit → frein

Tous ouverts → roue libre (le moteur tourne librement par inertie)

Attention : fermer S1 et S2 en même temps (ou S3 + S4) crée un court-circuit catastrophique → c'est ce qu'on appelle le "shoot-through".

Le Pi envoie des signaux logiques simples (IN1, IN2) pour choisir le sens, et un signal PWM sur ENA pour la vitesse. C'est le L298N qui s'occupe d'alimenter les moteurs avec les batteries, le Pi ne fait que donner les ordres.

---

## Tableau Récapitulatif

| Composant | Interface | Rôle |
| :--- | :--- | :--- |
| **HC-SR04 x3** | GPIO Digital | Détection d'obstacles (seuil 10 cm) |
| **Capteur IR** | GPIO Digital | Détection de la ligne d'arrivée |
| **TCS3472** | I2C | Détection du feu vert de départ |
| **INA219** | I2C | Surveillance batterie et logs |
| **Servomoteur** | PWM via PCA9685 (I2C) | Direction des roues avant |
| **Moteurs DC** | PWM via L298N (pont en H) | Propulsion avant et arrière |

---

## Conclusion

Ces composants correspondent bien aux contraintes du projet et sont bien documentés. Le bus I2C regroupe les capteurs qui renvoient des données complexes sur seulement deux fils, et le GPIO gère ce qui est simple comme les détections binaires. Les drivers L298N et PCA9685 protègent le Pi et lui permettent de contrôler des composants puissants avec de simples signaux logiques.


## Sources

HC-SR04

https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf 

https://www.raspberrypi.com/documentation/ 

Capteur Infrarouge

https://datasheet4u.com/datasheets/TAOS/TCS3472/911411

TCS3472

https://ams.com/documents/20143/36005/TCS3472_DS000390_3-00.pdf

INA219

https://www.ti.com/lit/ds/symlink/ina219.pdf

L298N (pont en H)

https://www.st.com/resource/en/datasheet/l298.pdf

PCA9685

https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf

I2C protocole

https://i2c.info/i2c-bus-specification
