Gestion Projet G9 2025/2026

## Description

Projet combinant programmation et électronique embarquée.

Le véhicule est capable de :

- Réaliser des trajectoires complexes (demi-tour, 8)
- Détecter une ligne d’arrivée avec précision
- Être testé avec des tests unitaires et scripts. 

---

## Architecture du Projet

Le projet repose sur une **architecture modulaire** séparant la logique, le matériel et l'interface.

```text
GDP_G9/
├── .gitignore              # Ignore les fichiers temporaires
├── README.md               # Documentation principale
├── LICENSE                 # Licence du projet
├── logger.py               # Utilitaires de logs
├── run_tests.py            # Lanceur de tests
├── diagramme_uml.puml      # Source PlantUML
├── schemaHCSR04.png        # Schéma capteur ultrason
├── caslimites.md           # Analyse des cas critiques
├── choix_raspberry.md      # Justification plateforme
├── justificationcomp.md    # Notes complémentaires
│
├── app/                    # Code applicatif principal
│   ├── controller/         # Logique d'orchestration
│   │   └── controleur.py
│   ├── model/              # Couche matérielle
│   │   ├── actionneurs/    # Moteur, Servomoteur
│   │   └── capteurs/       # IR, RGB, Ultrason
│   └── view/               # Interface utilisateur
│       └── interface.py
│
├── service/                # Scripts d'exécution terrain
│   ├── manoeuvres.py       # Algorithmes de déplacement
│   ├── routine.py          # Script principal
│   └── routine.service     # Service systemd (auto-start)
│
├── tests/                  # Suite de tests unitaires
│   ├── controller/
│   ├── model/
│   └── view/
│
└── reports/                # Rapports et logs générés
    ├── report_*.txt
    └── routine.log
```
---

## Composants

### Capteurs
- Ultrason HC-SR04  
- Capteur IR  
- TCS34725  

### Actionneurs
- Moteur DC (L298N)  
- Servomoteur (PCA9685)  

### Énergie
- INA219  

### Execution
- Course.py  
- routine.py 
- manoeuvres.py 

---

## Tests

Tests unitaires :
- Capteurs  
- Actionneurs  
- Modèle  

---

## Difficultés rencontrées

- Problèmes de câblage  
- Bugs GPIO / I2C  
- Debug après tests réels
- Durée de vie des batteries PiJuice  

---

## Scrum

- User stories  
- Backlog  
- Daily scrum
- Sprint review
- Sprint Retrospective

---

## Équipe

Groupe 9 - 2025/2026
Maxime CLOS, Daniel HERMAN, Théo LAYEUX, Amadou OUSMANOU, Noah
SCHOLLAERT

---

Dernière mise à jour : 13 avril 2026
