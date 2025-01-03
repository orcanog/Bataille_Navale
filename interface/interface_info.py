import tkinter as tk

class InterfaceInfo:
    def __init__(self, parent, gestionnaire):
        self.parent = parent
        self.gestionnaire = gestionnaire
        self.orientation_verticale = False
        # Navire sélectionné par défaut lors du démarrage de la phase de placement des navires
        self.navire_selectionne = "Porte-avions"

    # Méthode pour créer l'interface d'informations
    def creer_interface(self):
        self.creer_frame_info()
        self.mettre_a_jour_compteurs()

    # Méthodes pour créer l'interface d'informations
    def creer_frame_info(self):
        self.frame_info = tk.Frame(self.parent)
        self.frame_info.pack(side=tk.TOP, fill='x', pady=20)
        self.creer_labels_info()
        self.creer_controles_placement()

    def creer_labels_info(self):
        self.etiquette_info = tk.Label(self.frame_info, 
                                     text="Placez vos navires", 
                                     font=("Arial", 12, "bold"))
        self.etiquette_info.pack(pady=5)
        
        self.label_placement = tk.Label(self.frame_info, 
                                      text="", 
                                      font=("Arial", 10))
        self.label_placement.pack(pady=5)

    # Méthodes pour créer les contrôles de placement des navires
    def creer_controles_placement(self):
        self.frame_controles = tk.LabelFrame(self.frame_info, 
                                           text="Contrôles de placement",
                                           pady=10, padx=10)
        self.frame_controles.pack(pady=5)
        
        # Ajout du bouton de placement aléatoire
        self.btn_aleatoire = tk.Button(self.frame_controles,
                                      text="Placement aléatoire",
                                      command=self.placer_navires_aleatoirement)
        self.btn_aleatoire.pack(pady=5)
        
        self.creer_boutons_navires()
        self.creer_boutons_orientation()

    # Méthodes pour créer les boutons de selection des navires et d'orientation
    def creer_boutons_navires(self):
        self.frame_navires = tk.Frame(self.frame_controles)
        self.frame_navires.pack(side=tk.LEFT, padx=20)
        self.boutons_navires = {}
        
        for nom, quantite in self.gestionnaire.TYPES_NAVIRES.items():
            frame = tk.Frame(self.frame_navires)
            frame.pack(fill='x', pady=2)
            
            btn = tk.Button(frame, text=nom, 
                           command=lambda n=nom: self.selectionner_navire(n))
            btn.pack(side=tk.LEFT)
            
            label = tk.Label(frame, text=f"x{quantite}")
            label.pack(side=tk.LEFT, padx=5)
            
            self.boutons_navires[nom] = (btn, label)

    def creer_boutons_orientation(self):
        self.frame_orientation = tk.Frame(self.frame_controles)
        self.frame_orientation.pack(side=tk.LEFT, padx=20)
        
        self.btn_horizontal = tk.Button(self.frame_orientation, 
                                      text="Horizontal",
                                      command=lambda: self.changer_orientation(False))
        self.btn_horizontal.pack(side=tk.LEFT, padx=5)
        
        self.btn_vertical = tk.Button(self.frame_orientation, 
                                    text="Vertical",
                                    command=lambda: self.changer_orientation(True))
        self.btn_vertical.pack(side=tk.LEFT, padx=5)

        # État initial: horizontal sélectionné
        self.orientation_verticale = False

    # Méthodes pour gérer les interactions avec l'interface
    def selectionner_navire(self, nom):
        if self.gestionnaire.compter_navires_disponibles(nom) > 0:
            self.navire_selectionne = nom
            self.mettre_a_jour_style_boutons()

    def changer_orientation(self, verticale):
        self.orientation_verticale = verticale
        self.mettre_a_jour_style_boutons()

    # Changer le style du bouton lorsqu'on appuie dessus
    def mettre_a_jour_style_boutons(self):
        for nom, (btn, _) in self.boutons_navires.items():
            if nom == self.navire_selectionne:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')
        
        self.btn_horizontal.config(relief=tk.SUNKEN if not self.orientation_verticale else tk.RAISED)
        self.btn_vertical.config(relief=tk.SUNKEN if self.orientation_verticale else tk.RAISED)

    # Méthode pour mettre à jour les compteurs d'informations
    def mettre_a_jour_compteurs(self):
        if self.gestionnaire.phase_placement:
            navires_a_placer = len(self.gestionnaire.plateau_joueur.navires_a_placer)
            txt_navires = "navire" if navires_a_placer < 2 else "navires"
            self.label_placement.config(text=f"{navires_a_placer} {txt_navires} à placer")
            self.mettre_a_jour_boutons_navires()
            return
        
        # Mise à jour des compteurs de navires
        restants_joueur = self.gestionnaire.plateau_joueur.compter_navires_restants()
        detruits_joueur = self.gestionnaire.plateau_joueur.compter_navires_detruits()
        restants_ordi = self.gestionnaire.plateau_ordi.compter_navires_restants()
        detruits_ordi = self.gestionnaire.plateau_ordi.compter_navires_detruits()
        
        # Gestion du singulier/pluriel
        txt_restant_j = "restant" if restants_joueur < 2 else "restants"
        txt_detruit_j = "détruit" if detruits_joueur < 2 else "détruits"
        
        txt_restant_o = "restant" if restants_ordi < 2 else "restants"
        txt_detruit_o = "détruit" if detruits_ordi < 2 else "détruits"
        
        # Mise à jour de l'information
        self.label_info_joueur.config(
            text=f"Vos navires: {restants_joueur} {txt_restant_j} | {detruits_joueur} {txt_detruit_j}"
        )
        self.label_info_ennemi.config(
            text=f"Navires ennemis: {restants_ordi} {txt_restant_o} | {detruits_ordi} {txt_detruit_o}"
        )

    # Méthode pour mettre à jour les informations affichées
    def mettre_a_jour_message(self, message):
        self.etiquette_info.config(text=message)
        self.mettre_a_jour_compteurs()

    # Méthode pour enlever les informations et boutons de placement des navires
    def nettoyer_interface_placement(self):
        if hasattr(self, 'frame_controles'):
            self.frame_controles.destroy()
        if hasattr(self, 'label_placement'):
            self.label_placement.destroy()

    # Méthode pour mettre à jour les boutons des navires selon leur quantité restante
    def mettre_a_jour_boutons_navires(self):
        if not self.gestionnaire.phase_placement:
            return
        
        for nom in self.gestionnaire.TYPES_NAVIRES:
            navires_restants = self.gestionnaire.compter_navires_disponibles(nom)
            btn, label = self.boutons_navires[nom]
            
            # Mise à jour du compteur
            label.config(text=f"x{navires_restants}")
            
            # Mise à jour de l'état du bouton
            if navires_restants == 0:
                btn.config(state=tk.DISABLED)
                if nom == self.navire_selectionne:
                    self.navire_selectionne = None
                    self.mettre_a_jour_style_boutons()
            else:
                btn.config(state=tk.NORMAL)

    # Méthode pour placer les navires du joueur aléatoirement
    def placer_navires_aleatoirement(self):
        self.gestionnaire.placer_navires_aleatoirement(self.gestionnaire.plateau_joueur)
        self.mettre_a_jour_compteurs()
        if not self.gestionnaire.plateau_joueur.reste_navire_a_placer():
            self.parent.fin_phase_placement()