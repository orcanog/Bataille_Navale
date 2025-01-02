class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.degats = []

    def est_detruit(self):
        return len(self.degats) == self.taille

    def touche(self):
        self.degats.append(1)

    def get_position(self):
        return self.positions

    def get_taille(self):
        return self.taille