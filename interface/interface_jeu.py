import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from jeu.joueur import Joueur
from jeu.plateau import Plateau
from divers.parametres import NAVIRE_ASSETS, TIR_REUSSI_ASSET, TIR_MANQUE_ASSET, EAU_ASSET

class FenetreJeu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        nom = self.obtenir_nom_joueur()
        
        # Créer les joueurs et leurs plateaux
        self.joueur = Joueur(nom)
        self.ordinateur = Joueur("Ordinateur", est_une_IA=True)
        self.plateau_joueur = Plateau()
        self.plateau_ordi = Plateau()
        
        
        self.phase_placement = True
        self.tour_joueur = True
        
        
        self.configurer_interface()
        self.pack(expand=True, fill='both')

    def obtenir_nom_joueur(self):
        nom = simpledialog.askstring("Nom du Joueur", "Entrez votre nom:")
        return nom if nom else "Joueur"

    def configurer_interface(self):
        self.cadre_joueur = tk.Frame(self)
        self.cadre_ordinateur = tk.Frame(self)
        
        self.grille_joueur = self.creer_grille_interface(self.cadre_joueur, "Vos navires", self.plateau_joueur)
        self.grille_ordi = self.creer_grille_interface(self.cadre_ordinateur, "Grille de l'Ordinateur", self.plateau_ordi)
        
        self.cadre_joueur.pack(side=tk.LEFT, padx=20, pady=20)
        self.cadre_ordinateur.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.etiquette_info = tk.Label(self, text="Placez vos navires")
        self.etiquette_info.pack()
        
        # Ajout des compteurs
        self.frame_info = tk.Frame(self)
        self.frame_info.pack(pady=10)
        
        # Info joueur
        self.label_info_joueur = tk.Label(self.frame_info, text="Vos navires: ")
        self.label_info_joueur.grid(row=0, column=0, padx=5)
        
        # Info ennemi
        self.label_info_ennemi = tk.Label(self.frame_info, text="Navires ennemis: ")
        self.label_info_ennemi.grid(row=0, column=1, padx=5)
        
        self.mettre_a_jour_compteurs()

    def creer_grille_interface(self, parent, titre, plateau):
        frame = tk.LabelFrame(parent, text=titre)
        boutons = []
        
        # Labels des colonnes (A-J)
        for i in range(10):
            tk.Label(frame, text=chr(65 + i)).grid(row=0, column=i+1)
        
        # Labels des lignes (1-10)
        for i in range(10):
            tk.Label(frame, text=str(i+1)).grid(row=i+1, column=0)
        
        # Création des cases
        for i in range(10):
            ligne = []
            for j in range(10):
                case = tk.Canvas(frame, width=30, height=30, bg=EAU_ASSET)
                case.grid(row=i+1, column=j+1)
                case.bind('<Button-1>', lambda e, x=i, y=j: self.gerer_clic(x, y, plateau))
                ligne.append(case)
            boutons.append(ligne)
            
        frame.pack()
        return boutons

    def gerer_clic(self, ligne, colonne, plateau):
        if plateau == self.plateau_joueur and self.phase_placement:
            # Phase de placement des navires du joueur
            if self.plateau_joueur.reste_navire_a_placer():
                navire = self.plateau_joueur.prochain_navire()
                if self.plateau_joueur.placer_navire(navire, ligne, colonne, True):
                    self.plateau_joueur.retirer_navire_liste()
                    self.mettre_a_jour_affichage()
                    if not self.plateau_joueur.reste_navire_a_placer():
                        self.phase_placement = False
                        self.placer_navires_ordinateur()
                        self.mettre_a_jour_affichage()
                        self.etiquette_info.config(text="À vous de jouer !")
            
        elif plateau == self.plateau_ordi and not self.phase_placement and self.tour_joueur:
            # Phase de tir du joueur
            if (ligne, colonne) not in self.plateau_ordi.tirs:
                touche = self.plateau_ordi.recevoir_tir(ligne, colonne)
                self.mettre_a_jour_affichage()
                if touche:
                    self.etiquette_info.config(text="Touché !")
                    if self.plateau_ordi.tous_navires_detruits():
                        self.fin_partie(True)
                    self.tour_joueur = False
                    self.tour_ordinateur()
                else:
                    self.etiquette_info.config(text="Manqué !")
                    self.tour_joueur = False
                    self.tour_ordinateur()

    def tour_ordinateur(self):
        # Tir aléatoire de l'ordinateur
        while True:
            ligne = random.randint(0, 9)
            colonne = random.randint(0, 9)
            if (ligne, colonne) not in self.plateau_joueur.tirs:
                break
        
        touche = self.plateau_joueur.recevoir_tir(ligne, colonne)
        self.mettre_a_jour_affichage()
        
        if touche:
            self.etiquette_info.config(text="L'ordinateur vous a touché !")
            if self.plateau_joueur.tous_navires_detruits():
                self.fin_partie(False)
            self.tour_joueur = True
        else:
            self.etiquette_info.config(text="L'ordinateur a manqué !")
            self.tour_joueur = True

    def placer_navires_ordinateur(self):
        while self.plateau_ordi.reste_navire_a_placer():
            navire = self.plateau_ordi.prochain_navire()
            place = False
            while not place:
                ligne = random.randint(0, 9)
                colonne = random.randint(0, 9)
                est_horizontal = random.choice([True, False])
                if self.plateau_ordi.placer_navire(navire, ligne, colonne, est_horizontal):
                    self.plateau_ordi.retirer_navire_liste()
                    place = True

    def mettre_a_jour_affichage(self):
        # Mise à jour grille joueur
        for i in range(10):
            for j in range(10):
                canvas = self.grille_joueur[i][j]
                if (i, j) in self.plateau_joueur.tirs:
                    if self.plateau_joueur.grille[i][j]:  # Si navire présent
                        canvas.configure(bg=TIR_REUSSI_ASSET)  # Rouge pour touché
                    else:
                        canvas.configure(bg=TIR_MANQUE_ASSET)  # Bleu pour manqué
                elif self.plateau_joueur.grille[i][j]:  # Si navire non touché
                    navire = self.plateau_joueur.grille[i][j]
                    canvas.configure(bg=NAVIRE_ASSETS[navire.nom])
                else:
                    canvas.configure(bg=EAU_ASSET)

        # Mise à jour grille ordinateur
        for i in range(10):
            for j in range(10):
                canvas = self.grille_ordi[i][j]
                if (i, j) in self.plateau_ordi.tirs:
                    if self.plateau_ordi.grille[i][j]:
                        canvas.configure(bg=TIR_REUSSI_ASSET)
                    else:
                        canvas.configure(bg=TIR_MANQUE_ASSET)
                else:
                    canvas.configure(bg=EAU_ASSET)
        
        self.mettre_a_jour_compteurs()

    def mettre_a_jour_compteurs(self):
        restants_joueur = self.plateau_joueur.compter_navires_restants()
        detruits_joueur = self.plateau_joueur.compter_navires_detruits()
        restants_ordi = self.plateau_ordi.compter_navires_restants()
        detruits_ordi = self.plateau_ordi.compter_navires_detruits()

        if self.phase_placement:
            navires_a_placer = len(self.plateau_joueur.navires_a_placer)
            self.label_info_joueur.config(text=f"Navires à placer : {navires_a_placer}")
            self.label_info_ennemi.config(text="")
            return

        if detruits_joueur < 2:
            self.label_info_joueur.config(
            text=f"Vos navires: {restants_joueur} restants | {detruits_joueur} détruit"
        )
            
        if detruits_ordi < 2:
            self.label_info_ennemi.config(
            text=f"Navires ennemis: {restants_ordi} restants | {detruits_ordi} détruit"
        )
            
        if restants_joueur < 2:
            self.label_info_joueur.config(
            text=f"Vos navires: {restants_joueur} restant | {detruits_joueur} détruits"
        )
            
        if restants_ordi < 2:
            self.label_info_ennemi.config(
            text=f"Navires ennemis: {restants_ordi} restant | {detruits_ordi} détruits"
        )
        
        self.label_info_joueur.config(
            text=f"Vos navires: {restants_joueur} restants | {detruits_joueur} détruits"
        )
        self.label_info_ennemi.config(
            text=f"Navires ennemis: {restants_ordi} restants | {detruits_ordi} détruits"
        )

    def fin_partie(self, victoire_joueur):
        gagnant = self.joueur.nom if victoire_joueur else self.ordinateur.nom
        messagebox.showinfo("Fin de partie", f"{gagnant} a gagné!")
        self.master.quit()