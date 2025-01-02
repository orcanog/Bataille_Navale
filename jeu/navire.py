class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.degats = []
        self.est_horizontal = True
        self.etat = "sain"

    def est_detruit(self):
        return self.etat == "detruit"