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


#com
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
        
        # Définition des boutons
        boutons = [
            ['C', 'CE', '(', ')'],
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        
        # Créer et positionner les boutons
        for i, ligne in enumerate(boutons):
            for j, texte in enumerate(ligne):
                if texte == '=':
                    # Bouton égal en vert
                    btn = ctk.CTkButton(
                        frame_boutons,
                        text=texte,
                        width=70,
                        height=50,
                        font=("Arial", 18, "bold"),
                        fg_color="green",
                        hover_color="darkgreen",
                        command=self.calculer_expression
                    )
                elif texte == 'C':
                    # Bouton effacer en rouge
                    btn = ctk.CTkButton(
                        frame_boutons,
                        text=texte,
                        width=70,
                        height=50,
                        font=("Arial", 18, "bold"),
                        fg_color="red",
                        hover_color="darkred",
                        command=self.effacer
                    )
                elif texte == 'CE':
                    # Bouton effacer dernier en orange
                    btn = ctk.CTkButton(
                        frame_boutons,
                        text=texte,
                        width=70,
                        height=50,
                        font=("Arial", 18, "bold"),
                        fg_color="orange",
                        hover_color="darkorange",
                        command=self.effacer_dernier
                    )
                else:
                    # Boutons normaux (chiffres et opérateurs)
                    btn = ctk.CTkButton(
                        frame_boutons,
                        text=texte,
                        width=70,
                        height=50,
                        font=("Arial", 18),
                        command=lambda t=texte: self.ajouter_caractere(t)
                    )
                
                btn.grid(row=i, column=j, padx=5, pady=5)
        
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
        # Créer une fenêtre popup
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Historique des calculs")
        popup.geometry("500x400")
        
        # Titre
        titre = ctk.CTkLabel(
            popup,
            text="📊 Historique des calculs",
            font=("Arial", 20, "bold")
        )
        titre.pack(pady=10)
        
        # Frame scrollable pour l'historique
        frame_scroll = ctk.CTkScrollableFrame(
            popup,
            width=450,
            height=280
        )
        frame_scroll.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Récupérer l'historique
        operations = self.historique.obtenir_historique()
        
        if not operations:
            # Aucun calcul dans l'historique
            label_vide = ctk.CTkLabel(
                frame_scroll,
                text="Aucun calcul dans l'historique",
                font=("Arial", 14),
                text_color="gray"
            )
            label_vide.pack(pady=20)
        else:
            # Afficher chaque opération
            for i, (expression, resultat, timestamp) in enumerate(operations, 1):
                # Frame pour chaque calcul
                frame_calcul = ctk.CTkFrame(frame_scroll)
                frame_calcul.pack(pady=5, padx=10, fill="x")
                
                # Numéro et timestamp
                label_info = ctk.CTkLabel(
                    frame_calcul,
                    text=f"#{i} - {timestamp}",
                    font=("Arial", 10),
                    text_color="gray"
                )
                label_info.pack(anchor="w", padx=10, pady=2)
                
                # Expression et résultat
                label_calcul = ctk.CTkLabel(
                    frame_calcul,
                    text=f"{expression} = {resultat}",
                    font=("Arial", 14, "bold")
                )
                label_calcul.pack(anchor="w", padx=10, pady=5)
        
        # Bouton fermer
        btn_fermer = ctk.CTkButton(
            popup,
            text="Fermer",
            command=popup.destroy,
            width=120
        )
        btn_fermer.pack(pady=10)
    
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