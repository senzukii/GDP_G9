# RAPPORT TECHNIQUE : DOCUMENTATION DES CAPTEURS (US3)

Ce document détaille le fonctionnement et la justification de chaque capteur utilisé dans le projet de module mobile.

---

## 1. HC-SR04 — Capteur Ultrason (x3)

### Fonctionnement

Le HC-SR04 envoie une onde sonore ultrasonique et mesure le temps qu’il met pour revenir après avoir touché un obstacle.

Il possède **4 broches** :

| Broche | Nom | Rôle |
| :--- | :--- | :--- |
| 1 | **VCC** | Alimentation +5V |
| 2 | **TRIG** | Déclencheur : le Pi envoie un pulse de 10µs pour lancer la mesure |
| 3 | **ECHO** | Réponse : reste HIGH pendant toute la durée du trajet de l'onde |
| 4 | **GND** | Masse (0V) |

### Séquence de mesure

1. Le Pi met **TRIG à HIGH** pendant **10 microsecondes** puis le remet à LOW
2. Le capteur envoie **8 pulses ultrasoniques** à 40 kHz
3. **ECHO passe à HIGH** dès que l'onde part
4. **ECHO repasse à LOW** dès que l'onde revient
5. On mesure le temps pendant lequel ECHO était HIGH

### Formule de calcul
d = (t × v_son) / 2

- **t** = durée pendant laquelle ECHO était HIGH (en secondes)
- **v_son** = 34 300 cm/s (vitesse du son à température ambiante)
- **/ 2** car l'onde fait l'aller ET le retour

**Exemple :** si ECHO reste HIGH pendant 0.00058s :
d = (0.00058 × 34300) / 2 = 9.94 cm → obstacle à ~10 cm

### Pourquoi pas très précis ?

Plusieurs facteurs perturbent la mesure :

- **La température** modifie la vitesse du son
- **L'angle** de l'obstacle : si la surface est inclinée, l'onde repart ailleurs et ne revient pas
- **Les surfaces molles** absorbent une partie de l'onde
- **Temps de réponse** : ~60ms minimum entre deux mesures

C'est pour ça qu'on utilise **3 capteurs** (gauche, droite, devant) pour compenser ces imprécisions.

### Pourquoi ce capteur ?

- Excellent rapport qualité/prix pour de la robotique de base
- Suffisant pour détecter un obstacle à 10 cm minimum comme exigé
- Interfaçage simple via GPIO sans protocole complexe

---

## 2. Capteur Infrarouge — Suiveur de ligne

### Fonctionnement

Le capteur IR émet une lumière infrarouge vers le sol et mesure ce qui est réfléchi :

- **Surface blanche** → réfléchit beaucoup → signal **HIGH**
- **Surface noire** (ligne d'arrivée) → absorbe la lumière → signal **LOW**

Il retourne un signal **binaire** (0 ou 1). Pas de calcul, pas de formule.

### Pourquoi ce capteur ?

- **Réactif** : la détection est quasi instantanée
- **Simple** : une seule broche GPIO en entrée suffit
- **Fiable** pour distinguer noir/blanc sur un circuit

### Pourquoi pas une caméra ?

Une caméra avec OpenCV demanderait trop de puissance de calcul au Raspberry Pi, ce qui ralentirait la boucle de contrôle principale des moteurs.

---

## 3. TCS3472 — Capteur de couleur RGB

### Fonctionnement

Le TCS3472 mesure l'intensité des composantes **Rouge, Vert, Bleu** de la lumière qu'il reçoit. Il communique via le protocole **I2C** avec seulement 2 fils :

| Fil | Rôle |
| :--- | :--- |
| **SDA** | Données (Serial Data) |
| **SCL** | Horloge de synchronisation (Serial Clock) |

Il retourne 4 valeurs numériques : R, G, B et Clear (luminosité globale).

### Utilisation dans le projet

Détecter le **feu vert de départ** : quand la valeur G (vert) dépasse un seuil défini, la voiture démarre automatiquement sans intervention humaine.

### Pourquoi pas le TCS3200 ?

Le TCS3200 produit une fréquence proportionnelle à l'intensité lumineuse, plus complexe à traiter. Le TCS3472 envoie directement des valeurs numériques via I2C.

---

## 4. INA219 — Moniteur d'énergie

### Fonctionnement

L'INA219 mesure en temps réel :
- La **tension** des batteries (en Volts)
- Le **courant** consommé (en Ampères)

Il communique via **I2C** (mêmes fils SDA/SCL que le TCS3472, avec une adresse différente sur le bus).

SDA c'est le fil qui transporte les données.

SCL c'est le fil qui synchronise l'envoi des données pour que le Pi et le capteur se comprennent et lisent les données au bon moment.

Pour vérifier qu'il est bien détecté :
```bash
i2cdetect -y 1
```

### Utilisation dans le projet

- Surveiller l'état des batteries 18650 pendant la course
- Alimenter le **système de logs** : si la tension chute lors d'une accélération, c'est enregistré et consultable à distance via SSH

### Pourquoi pas l'ACS712 ?

L'ACS712 produit une sortie **analogique**. Le Raspberry Pi n'a pas d'entrées analogiques natives, il faudrait un convertisseur supplémentaire. L'INA219 en I2C s'intègre directement sans composant extra.

---

## Tableau Récapitulatif

| Capteur | Interface | Broches | Rôle |
| :--- | :--- | :--- | :--- |
| **HC-SR04 x3** | GPIO Digital | TRIG + ECHO + VCC + GND | Évitement d'obstacles (seuil 10 cm) |
| **Capteur IR** | GPIO Digital | Signal + VCC + GND | Détection ligne d'arrivée |
| **TCS3472** | I2C | SDA + SCL + VCC + GND | Détection feu vert de départ |
| **INA219** | I2C | SDA + SCL + VCC + GND | Surveillance batterie + logs |

---

## Conclusion

Le choix de ces capteurs repose sur un équilibre entre **fiabilité** et **simplicité d'intégration**. Le protocole I2C est utilisé pour les capteurs renvoyant des données complexes (couleur, énergie), tandis que le GPIO direct suffit pour les détections binaires simples (ligne, obstacle). Cette configuration permet de valider tous les critères d'acceptation du cahier de charges, notamment l'évitement d'obstacles à 10 cm minimum et l'arrêt précis sur la ligne d'arrivée.
