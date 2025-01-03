import tkinter as tk
from divers.parametres import NAVIRE_ASSETS, TIR_REUSSI_ASSET, TIR_MANQUE_ASSET, EAU_ASSET
from interface.gestionnaire_joueurs import GestionnaireJoueurs
from interface.interface_info import InterfaceInfo

class InterfaceJeu(tk.Frame):
    # Constantes de délai
    DELAI_MESSAGE = 1000  # 1 seconde
    DELAI_TIR = 1500     # 1.5 secondes

    def __init__(self, master, nom_joueur):
        super().__init__(master)
        self.master = master
        self.nom_joueur = nom_joueur
        self.initialiser_partie()
        self.pack(expand=True, fill='both')

    # Méthode pour initialiser la partie
    def initialiser_partie(self):
        self.gestionnaire = GestionnaireJoueurs(self.nom_joueur)
        self.interface = InterfaceInfo(self, self.gestionnaire)
        self.liaison_evenements()
        self.creer_interface()

    # Méthode pour créer l'interface de jeu
    def creer_interface(self):
        self.interface.creer_interface()
        self.creer_frame_grilles()
        self.interface.mettre_a_jour_compteurs()

    # Méthode pour créer une grille de jeu
    def creer_grille_interface(self, parent, titre, plateau):
        frame = tk.LabelFrame(parent, text=titre)
        boutons = []
        TAILLE_CASE = 30
        BORDURE = 1
        
        for i in range(10):
            tk.Label(frame, text=chr(65 + i)).grid(row=0, column=i+1)
        
        for i in range(10):
            tk.Label(frame, text=str(i+1)).grid(row=i+1, column=0)
            ligne = []
            for j in range(10):
                case = tk.Canvas(frame, 
                               width=TAILLE_CASE, 
                               height=TAILLE_CASE, 
                               bg=EAU_ASSET,
                               highlightthickness=BORDURE,
                               highlightbackground='black')
                case.grid(row=i+1, column=j+1, padx=0, pady=0)
                case.bind('<Button-1>', 
                         lambda e, x=i, y=j, p=plateau: self.gerer_clic_joueur(x, y))
                ligne.append(case)
            boutons.append(ligne)
        
        frame.pack()
        return boutons

    # Méthode pour créer le conteneur des grilles de jeu
    def creer_frame_grilles(self):
        self.frame_grilles = tk.Frame(self)
        self.frame_grilles.pack(expand=True, fill='both')
        
        for i in range(5):
            self.frame_grilles.grid_columnconfigure(i, weight=1)
        
        self.creer_grille_joueur()
        self.creer_grille_ordinateur()

    # Méthode pour créer la grille du joueur
    def creer_grille_joueur(self):
        self.cadre_joueur = tk.Frame(self.frame_grilles)
        self.interface.label_info_joueur = tk.Label(self.cadre_joueur, text="", font=("Arial", 10))
        self.interface.label_info_joueur.pack(pady=(0, 10))
        self.grille_joueur = self.creer_grille_interface(self.cadre_joueur, 
                                                        "Vos navires", 
                                                        self.gestionnaire.plateau_joueur)
        self.cadre_joueur.grid(row=0, column=1)

    # Méthode pour créer la grille de l'ordinateur
    def creer_grille_ordinateur(self):
        self.cadre_ordinateur = tk.Frame(self.frame_grilles)
        self.interface.label_info_ennemi = tk.Label(self.cadre_ordinateur, text="", font=("Arial", 10))
        self.interface.label_info_ennemi.pack(pady=(0, 10))
        self.grille_ordi = self.creer_grille_interface(self.cadre_ordinateur,
                                                      "Grille de l'IA",
                                                      self.gestionnaire.plateau_ordi)
        self.cadre_ordinateur.grid(row=0, column=3)
        self.cadre_ordinateur.grid_remove()

    # Méthode pour mettre à jour l'affichage des cases des grilles
    def mettre_a_jour_case(self, canvas, position, plateau, montrer_navires=True):
        i, j = position
        if (i, j) in plateau.tirs:
            if plateau.grille[i][j]:
                canvas.configure(bg=TIR_REUSSI_ASSET)
            else:
                canvas.configure(bg=TIR_MANQUE_ASSET)
        elif plateau.grille[i][j] and montrer_navires:
            navire = plateau.grille[i][j]
            canvas.configure(bg=NAVIRE_ASSETS[navire.nom])
        else:
            canvas.configure(bg=EAU_ASSET)

    # Méthode pour mettre à jour l'affichage des grilles
    def mettre_a_jour_affichage(self):
        for i in range(10):
            for j in range(10):
                self.mettre_a_jour_case(self.grille_joueur[i][j], 
                                      (i,j), 
                                      self.gestionnaire.plateau_joueur)
                self.mettre_a_jour_case(self.grille_ordi[i][j], 
                                      (i,j), 
                                      self.gestionnaire.plateau_ordi, 
                                      False)

    # Méthode pour lier les événements de clics sur les grilles à des fonctions
    def liaison_evenements(self):
        self.interface.grille_joueur_callback = self.gerer_clic_joueur
        self.interface.grille_ordi_callback = self.gerer_clic_joueur

    # Méthode pour gérer les clics du joueur sur les grilles
    def gerer_clic_joueur(self, ligne, colonne):

        # Phase de placement pour le joueur, clics sur sa grille
        if self.gestionnaire.phase_placement:
            if not self.interface.navire_selectionne:
                self.interface.mettre_a_jour_message("Sélectionnez un navire à placer")
                return

            navire_a_placer = None
            for navire in self.gestionnaire.plateau_joueur.navires_a_placer:
                if navire.nom == self.interface.navire_selectionne:
                    navire_a_placer = navire
                    break
            
            if not navire_a_placer:
                return
                
            if self.gestionnaire.placer_navire(ligne, colonne, navire_a_placer, 
                                             not self.interface.orientation_verticale):
                for i, navire in enumerate(self.gestionnaire.plateau_joueur.navires_a_placer):
                    if navire is navire_a_placer:
                        self.gestionnaire.plateau_joueur.navires_a_placer.pop(i)
                        break
                        
                self.interface.mettre_a_jour_affichage()
                self.interface.mettre_a_jour_compteurs()
                
                if not self.gestionnaire.compter_navires_disponibles(self.interface.navire_selectionne):
                    self.interface.navire_selectionne = None
                    self.interface.mettre_a_jour_style_boutons()
                
                if not self.gestionnaire.plateau_joueur.reste_navire_a_placer():
                    self.fin_phase_placement()
                    
        # Phase de jeu pour le joueur, clics sur la grille de l'ordinateur
        elif not self.gestionnaire.phase_placement and self.gestionnaire.tour_joueur:
            if (ligne, colonne) in self.gestionnaire.plateau_ordi.tirs:
                self.interface.mettre_a_jour_message("Cette case a déjà été ciblée !")
                return
                
            touche, partie_finie = self.gestionnaire.gerer_tir_joueur(ligne, colonne)
            self.mettre_a_jour_affichage()
            
            message = "Touché !" if touche else "Manqué !"
            self.interface.mettre_a_jour_message(message)
            
            if partie_finie:
                self.master.after(self.DELAI_MESSAGE, lambda: self.fin_partie(True))
            else:
                self.gestionnaire.tour_joueur = False
                self.master.after(self.DELAI_MESSAGE, self.tour_ordinateur)

    # Méthode pour terminer la phase de placement
    def fin_phase_placement(self):
        self.gestionnaire.phase_placement = False
        self.interface.nettoyer_interface_placement()
        self.gestionnaire.placer_navires_ordinateur()
        # On affiche la grille de l'ordinateur qui était cachée lors de la phase de placement
        self.cadre_ordinateur.grid()
        self.mettre_a_jour_affichage()
        self.interface.mettre_a_jour_message("À vous de jouer !")

    # Méthode pour gérer le tour de l'ordinateur
    def tour_ordinateur(self):
        self.interface.mettre_a_jour_message("Tour de l'ordinateur...")
        self.master.after(self.DELAI_MESSAGE, self.executer_tir_ordi)

    # Méthode pour exécuter le tir de l'ordinateur
    def executer_tir_ordi(self):
        ligne, colonne, touche, partie_finie = self.gestionnaire.gerer_tir_ordinateur()
        self.mettre_a_jour_affichage()
        
        message = "L'ordinateur vous a touché!" if touche else "L'ordinateur a manqué!"
        self.interface.mettre_a_jour_message(message)
        
        if partie_finie:
            self.master.after(self.DELAI_TIR, lambda: self.fin_partie(False))
        else:
            self.master.after(self.DELAI_TIR, self.fin_tour_ordi)

    # Méthode pour gérer la fin du tour de l'ordinateur
    def fin_tour_ordi(self):
        self.gestionnaire.tour_joueur = True
        self.interface.mettre_a_jour_message("À vous de jouer!")

    # Méthode pour gérer la fin de la partie
    def fin_partie(self, victoire):
        message = "Victoire !" if victoire else "Défaite !"
        self.interface.mettre_a_jour_message(message)
        self.ajouter_boutons_fin_partie()

    # Méthode pour ajouter des boutons pour recommencer ou quitter la partie
    def ajouter_boutons_fin_partie(self):
        self.frame_fin = tk.Frame(self.interface.frame_info)
        self.frame_fin.pack(pady=10)
        
        tk.Button(self.frame_fin, text="Nouvelle partie",
                 command=self.nouvelle_partie).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_fin, text="Quitter",
                 command=self.master.quit).pack(side=tk.LEFT, padx=10)

    # Méthode pour recommencer une nouvelle partie
    def nouvelle_partie(self):
        self.destroy()
        self.__init__(self.master, self.nom_joueur)