class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.navires = []
        self.tirs = []

    def placer_navires(self, navire, position):
        self.navires.append((navire, position))

    def effectuer_tir(self, position):
        # Vérifier si un tir n'a pas déjà été effectué à cette position
        if position not in self.tirs:
            self.tirs.append(position)
            return True
        return False

    def defaite(self):
        pass