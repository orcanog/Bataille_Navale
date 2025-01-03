from jeu.navire import Navire

class Plateau:
    def __init__(self):
        self.taille = 10
        self.grille = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        self.navires = []
        self.tirs = set()
        self.navires_a_placer = self.initialiser_navires()

    def initialiser_navires(self):
        return [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4),
            Navire("Destroyeur", 3),
            Navire("Destroyeur", 3),
            Navire("Sous-marin", 2),
            Navire("Sous-marin", 2)
        ]

    def prochain_navire(self):
        return self.navires_a_placer[0] if self.navires_a_placer else None

    def retirer_navire_liste(self):
        if self.navires_a_placer:
            return self.navires_a_placer.pop(0)
        return None

    def placer_navire(self, navire, ligne, colonne, est_horizontal):
        if self.peut_placer_navire(navire, ligne, colonne, est_horizontal):
            positions = []
            for i in range(navire.taille):
                if est_horizontal:
                    self.grille[ligne][colonne + i] = navire
                    positions.append((ligne, colonne + i))
                else:
                    self.grille[ligne + i][colonne] = navire
                    positions.append((ligne + i, colonne))
            navire.positions = positions
            navire.est_horizontal = est_horizontal
            self.navires.append(navire)
            return True
        return False

    def peut_placer_navire(self, navire, ligne, colonne, est_horizontal):
        if est_horizontal and colonne + navire.taille > self.taille:
            return False
        if not est_horizontal and ligne + navire.taille > self.taille:
            return False

        # Vérifier si les cases sont libres
        for i in range(navire.taille):
            if est_horizontal:
                if self.grille[ligne][colonne + i] is not None:
                    return False
            else:
                if self.grille[ligne + i][colonne] is not None:
                    return False
        return True

    def reste_navire_a_placer(self):
        return len(self.navires_a_placer) > 0

    def recevoir_tir(self, ligne, colonne):
        if (ligne, colonne) in self.tirs:
            return False
        
        self.tirs.add((ligne, colonne))
        presence_navire = self.grille[ligne][colonne]
        
        if presence_navire:
            navire = presence_navire
            navire.degats.append((ligne, colonne))
            if len(navire.degats) == navire.taille:
                navire.etat = "detruit"
            return True
        return False

    def tous_navires_detruits(self):
        return all(navire.etat == "detruit" for navire in self.navires)
    
    def compter_navires_restants(self):
        return len([navire for navire in self.navires if navire.etat != "detruit"])

    def compter_navires_detruits(self):
        return len([navire for navire in self.navires if navire.etat == "detruit"])