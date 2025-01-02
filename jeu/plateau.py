class Plateau:
    def __init__(self):
        self.taille = 10
        self.grille = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        self.navires = []
        self.tirs = set()