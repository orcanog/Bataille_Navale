import tkinter as tk
from tkinter import messagebox
from interface.interface_jeu import InterfaceJeu

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bataille Navale")
        self.geometry("1280x800")
        self.entry_nom = None  # Initialize entry widget variable
        
        # Frame principale pour contenir menu et jeu
        self.frame_principale = tk.Frame(self)
        self.frame_principale.pack(expand=True, fill='both')
        
        self.frame_active = None
        self.afficher_menu()

    def afficher_menu(self):
        # Nettoyer l'interface précédente
        if self.frame_active:
            self.frame_active.destroy()

        # Créer nouvelle frame menu
        self.frame_menu = tk.Frame(self.frame_principale)
        self.frame_active = self.frame_menu
        self.frame_menu.pack(expand=True, fill='both')
        
        # Titre
        titre = tk.Label(self.frame_menu, text="Bataille Navale", font=("Arial", 24, "bold"))
        titre.pack(pady=20)

        # Frame pour le nom
        frame_nom = tk.Frame(self.frame_menu)
        frame_nom.pack(pady=10)
        
        # Label et Entry pour le nom
        tk.Label(frame_nom, text="Nom du joueur:").pack(side=tk.LEFT)
        self.entry_nom = tk.Entry(frame_nom)  # Store as instance variable
        self.entry_nom.pack(side=tk.LEFT, padx=5)
        self.entry_nom.insert(0, "Joueur")

        # Boutons
        tk.Button(self.frame_menu, text="Règles du jeu", command=self.afficher_regles).pack(pady=5)
        tk.Button(self.frame_menu, text="Commencer la partie", command=self.demarrer_partie).pack(pady=5)
        tk.Button(self.frame_menu, text="Quitter", command=self.quit).pack(pady=5)

    def afficher_regles(self):
        regles = """Règles de la Bataille Navale:

1. Chaque joueur dispose d'une flotte de 6 navires:
   - 1 Porte-avions (5 cases)
   - 1 Croiseur (4 cases)
   - 2 Destroyeurs (3 cases)
   - 2 Sous-marins (2 cases)

2. Phase de placement:
   - Placez vos navires sur votre grille
   - Les navires peuvent être placés horizontalement ou verticalement
   - Les navires ne peuvent pas se chevaucher

3. Phase de jeu:
   - À tour de rôle, tirez sur la grille adverse
   - Un tir réussi est marqué en rouge
   - Un tir manqué est marqué en bleu

4. Victoire:
   - Le premier joueur qui détruit tous les navires adverses gagne"""
        
        messagebox.showinfo("Règles du jeu", regles)

    def demarrer_partie(self):
        try:
            nom = self.entry_nom.get() if self.entry_nom else "Joueur"
            if self.frame_active:
                self.frame_active.destroy()
            
            self.frame_jeu = InterfaceJeu(self.frame_principale, nom)
            self.frame_active = self.frame_jeu
            self.frame_jeu.pack(expand=True, fill='both')
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de démarrer la partie: {str(e)}")

    def retour_menu(self):
        self.afficher_menu()