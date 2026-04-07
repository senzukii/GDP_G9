class Interface:
    def afficher_etat(self, vitesse, obstacle_infrarouge, distance_cm):
        etat_obstacle = "oui" if obstacle_infrarouge else "non"
        return f"Vitesse: {vitesse} | Obstacle IR: {etat_obstacle} | Distance: {distance_cm} cm"
