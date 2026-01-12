# src/interface.py
"""
Module de l'interface graphique de la calculatrice.
Utilise CustomTkinter pour un design moderne. 
"""

import customtkinter as ctk
from tkinter import messagebox

from src.calculateur import calculer
from src.validateur import Validateur
from src.historique import Historique
from src.exceptions import CalculatriceError


class CalculatriceGUI: 
    """Interface graphique de la calculatrice"""
    
    def __init__(self):
        """Initialise l'interface graphique"""
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")  # "light" ou "dark"
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.fenetre = ctk.CTk()
        self.fenetre.title("Calculatrice")
        self.fenetre.geometry("400x600")
        self.fenetre.resizable(False, False)
        
        # Modules
        self.validateur = Validateur()
        self.historique = Historique()
        
        # Variables
        self.expression_courante = ""
        
        # Créer l'interface
        self.creer_interface()
    
    def creer_interface(self):
        """Crée tous les éléments de l'interface"""
        # TODO: À compléter par Personne 3
        
        # Écran d'affichage
        self.ecran = ctk.CTkEntry(
            self.fenetre,
            font=("Arial", 24),
            height=60,
            justify="right"
        )
        self.ecran.pack(pady=20, padx=20, fill="x")
        
        # Label pour le résultat
        self.label_resultat = ctk.CTkLabel(
            self.fenetre,
            text="",
            font=("Arial", 18),
            text_color="green"
        )
        self.label_resultat.pack(pady=5)
        
        # Label pour les erreurs
        self.label_erreur = ctk.CTkLabel(
            self.fenetre,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.label_erreur.pack(pady=5)
        
        # Frame pour les boutons
        frame_boutons = ctk.CTkFrame(self.fenetre)
        frame_boutons.pack(pady=20, padx=20)
        
        # TODO:  Créer les boutons (0-9, opérateurs, =, C, CE, parenthèses)
        # Utiliser frame_boutons.grid() pour les positionner
        
        # Boutons d'historique
        frame_historique = ctk.CTkFrame(self.fenetre)
        frame_historique.pack(pady=10)
        
        btn_voir_hist = ctk.CTkButton(
            frame_historique,
            text="Voir historique",
            command=self.afficher_historique
        )
        btn_voir_hist.pack(side="left", padx=5)
        
        btn_effacer_hist = ctk.CTkButton(
            frame_historique,
            text="Effacer historique",
            command=self.effacer_historique
        )
        btn_effacer_hist.pack(side="left", padx=5)
    
    def ajouter_caractere(self, caractere):
        """
        Ajoute un caractère à l'expression courante. 
        
        Args:
            caractere: Le caractère à ajouter
        """
        self.expression_courante += str(caractere)
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
        self.label_erreur.configure(text="")  # Effacer les erreurs
    
    def calculer_expression(self):
        """
        Calcule l'expression saisie.
        Appelé quand l'utilisateur clique sur =
        """
        expression = self.ecran.get()
        
        # Effacer les messages précédents
        self.label_erreur.configure(text="")
        self.label_resultat.configure(text="")
        
        # Validation
        valide, message_erreur = self.validateur.valider_expression(expression)
        if not valide:
            self.label_erreur.configure(text=message_erreur)
            return
        
        # Calcul
        try:
            resultat = calculer(expression)
            self.label_resultat.configure(text=f"= {resultat}")
            self.historique.ajouter(expression, resultat)
        except CalculatriceError as e: 
            self.label_erreur.configure(text=str(e))
        except Exception as e: 
            self.label_erreur.configure(text=f"Erreur inattendue :  {str(e)}")
    
    def effacer(self):
        """Efface tout l'écran (bouton C)"""
        self.expression_courante = ""
        self.ecran.delete(0, "end")
        self.label_erreur.configure(text="")
        self.label_resultat.configure(text="")
    
    def effacer_dernier(self):
        """Efface le dernier caractère (bouton CE)"""
        self.expression_courante = self.expression_courante[:-1]
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
    
    def afficher_historique(self):
        """Affiche la fenêtre d'historique"""
        # TODO: À compléter par Personne 3
        # Créer une fenêtre popup avec la liste des calculs
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Historique des calculs")
        popup.geometry("500x400")
        
        # Ajouter un scrollable frame
        # Afficher toutes les opérations
        # Bouton pour fermer
        pass
    
    def effacer_historique(self):
        """Efface l'historique"""
        reponse = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment effacer tout l'historique ?"
        )
        if reponse:
            self.historique.effacer()
            messagebox.showinfo("Succès", "Historique effacé")
    
    def run(self):
        """Lance l'application"""
        self.fenetre.mainloop()