import random
from jeu.joueur import Joueur
from jeu.plateau import Plateau

class GestionnaireJoueurs:
    TYPES_NAVIRES = {
        "Porte-avions": 1,
        "Croiseur": 1,
        "Destroyeur": 2,
        "Sous-marin": 2
    }

    def __init__(self, nom_joueur):
        self.initialiser_joueurs(nom_joueur)
        self.initialiser_etat_jeu()

    def initialiser_joueurs(self, nom_joueur):
        self.joueur = Joueur(nom_joueur)
        self.ordinateur = Joueur("Ordinateur", est_une_IA=True)
        self.plateau_joueur = Plateau()
        self.plateau_ordi = Plateau()

    def initialiser_etat_jeu(self):
        self.phase_placement = True
        self.tour_joueur = True

    # Méthode pour compter les navires placés d'un type spécifique
    def compter_navires_places(self, type_navire):
        return sum(1 for navire in self.plateau_joueur.navires if navire.nom == type_navire)

    # Méthode pour vérifier si un type de navire est encore disponible
    def est_navire_disponible(self, type_navire):
        navires_places = self.compter_navires_places(type_navire)
        return navires_places < self.TYPES_NAVIRES[type_navire]

    # Méthode pour compter les navires restants à placer d'un type spécifique
    def compter_navires_disponibles(self, type_navire):
        return sum(1 for navire in self.plateau_joueur.navires_a_placer 
              if navire.nom == type_navire)

    # Méthode pour placer un navire spécifique sur le plateau
    def placer_navire(self, ligne, colonne, navire, est_horizontal):
        return self.plateau_joueur.placer_navire(navire, ligne, colonne, est_horizontal)

    # Méthode pour placer tous les navires aléatoirement sur le plateau
    def placer_navires_aleatoirement(self, plateau):
        while plateau.reste_navire_a_placer():
            navire = plateau.prochain_navire()
            self.placer_navire_aleatoire(navire, plateau)

    # Méthode pour placer un navire aléatoirement sur le plateau
    def placer_navire_aleatoire(self, navire, plateau):
        while True:
            ligne = random.randint(0, 9)
            colonne = random.randint(0, 9)
            est_horizontal = random.choice([True, False])
            if plateau.placer_navire(navire, ligne, colonne, est_horizontal):
                plateau.retirer_navire_liste()
                break

    # Méthode pour placer les navires de l'ordinateur aléatoirement
    def placer_navires_ordinateur(self):
        self.placer_navires_aleatoirement(self.plateau_ordi)

    # Méthode pour gérer un tir du joueur
    def gerer_tir_joueur(self, ligne, colonne):
        if (ligne, colonne) in self.plateau_ordi.tirs:
            return False, False
        touche = self.plateau_ordi.recevoir_tir(ligne, colonne)
        partie_finie = touche and self.plateau_ordi.tous_navires_detruits()
        return touche, partie_finie

    # Méthode pour gérer un tir de l'ordinateur
    def gerer_tir_ordinateur(self):
        while True:
            ligne = random.randint(0, 9)
            colonne = random.randint(0, 9)
            if (ligne, colonne) not in self.plateau_joueur.tirs:
                touche = self.plateau_joueur.recevoir_tir(ligne, colonne)
                partie_finie = touche and self.plateau_joueur.tous_navires_detruits()
                return ligne, colonne, touche, partie_finie