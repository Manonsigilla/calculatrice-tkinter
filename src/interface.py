"""
================================================================================
Module de l'interface graphique de la calculatrice - VERSION 2.0
================================================================================
Utilise CustomTkinter pour un design moderne.  

NOUVEAUTÉS V2.0 :
- Boutons fonctions scientifiques (sqrt, abs, sin, cos, tan)
- Boutons min, max pour comparer deux nombres
- Bouton % pour le modulo
- Support des nombres négatifs avec le signe -
================================================================================
"""

import customtkinter as ctk
from tkinter import messagebox

from src.calculateur import calculer
from src.validateur import Validateur
from src.historique import Historique
from src.exceptions import CalculatriceError


class CalculatriceGUI:  
    """Interface graphique de la calculatrice scientifique"""
    
    def __init__(self):
        """Initialise l'interface graphique"""
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # =====================================================================
        # FENÊTRE PRINCIPALE - HAUTEUR AUGMENTÉE POUR VOIR LES BOUTONS HISTORIQUE
        # =====================================================================
        self.fenetre = ctk.CTk()
        self.fenetre.title("Calculatrice Scientifique v2.0")
        self.fenetre.geometry("450x780")  # Hauteur augmentée (était 700)
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
        
        # =====================================================================
        # ÉCRAN D'AFFICHAGE
        # =====================================================================
        self.ecran = ctk.CTkEntry(
            self.fenetre,
            font=("Arial", 24),
            height=60,
            justify="right"
        )
        self.ecran.pack(pady=15, padx=20, fill="x")
        
        # Label pour le résultat (en vert)
        self.label_resultat = ctk.CTkLabel(
            self.fenetre,
            text="",
            font=("Arial", 18),
            text_color="green"
        )
        self.label_resultat.pack(pady=5)
        
        # Label pour les erreurs (en rouge)
        self.label_erreur = ctk.CTkLabel(
            self.fenetre,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.label_erreur.pack(pady=5)
        
        # =====================================================================
        # FRAME POUR LES BOUTONS SCIENTIFIQUES
        # =====================================================================
        frame_scientifique = ctk.CTkFrame(self.fenetre)
        frame_scientifique.pack(pady=10, padx=20)
        
        # Première ligne :  sin, cos, tan, sqrt
        boutons_scientifiques_ligne1 = ['sin', 'cos', 'tan', 'sqrt']
        for j, texte in enumerate(boutons_scientifiques_ligne1):
            btn = ctk.CTkButton(
                frame_scientifique,
                text=texte,
                width=95,
                height=40,
                font=("Arial", 14),
                fg_color="#6B5B95",
                hover_color="#5A4A84",
                command=lambda t=texte: self.ajouter_fonction(t)
            )
            btn.grid(row=0, column=j, padx=3, pady=3)
        
        # Deuxième ligne : abs, min, max, (vide ou autre)
        # MODIFICATION : Retrait du bouton ± qui n'était pas clair
        boutons_scientifiques_ligne2 = ['abs', 'min', 'max']
        for j, texte in enumerate(boutons_scientifiques_ligne2):
            btn = ctk.CTkButton(
                frame_scientifique,
                text=texte,
                width=95,
                height=40,
                font=("Arial", 14),
                fg_color="#6B5B95",
                hover_color="#5A4A84",
                command=lambda t=texte: self.ajouter_fonction(t)
            )
            btn.grid(row=1, column=j, padx=3, pady=3)
        
        # =====================================================================
        # FRAME POUR LES BOUTONS PRINCIPAUX
        # =====================================================================
        frame_boutons = ctk.CTkFrame(self.fenetre)
        frame_boutons.pack(pady=10, padx=20)
        
        # Définition des boutons
        boutons = [
            ['C', 'CE', '(', ')'],
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['%', ',', '', '']  # Modulo et virgule (pour min/max)
        ]
        
        # Créer et positionner les boutons
        for i, ligne in enumerate(boutons):
            for j, texte in enumerate(ligne):
                # Ignorer les cases vides
                if texte == '':
                    continue
                    
                if texte == '=':
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
                elif texte == '%':
                    btn = ctk.CTkButton(
                        frame_boutons,
                        text=texte,
                        width=70,
                        height=50,
                        font=("Arial", 18),
                        fg_color="#2E86AB",
                        hover_color="#1E5F7A",
                        command=lambda t=texte: self.ajouter_caractere(t)
                    )
                else:
                    btn = ctk.CTkButton(
                        frame_boutons,
                        text=texte,
                        width=70,
                        height=50,
                        font=("Arial", 18),
                        command=lambda t=texte: self.ajouter_caractere(t)
                    )
                
                btn.grid(row=i, column=j, padx=5, pady=5)
        
        # =====================================================================
        # BOUTONS D'HISTORIQUE - Maintenant visibles ! 
        # =====================================================================
        frame_historique = ctk.CTkFrame(self.fenetre)
        frame_historique.pack(pady=15)
        
        btn_voir_hist = ctk.CTkButton(
            frame_historique,
            text="📊 Voir historique",
            width=150,
            command=self.afficher_historique
        )
        btn_voir_hist.pack(side="left", padx=10)
        
        btn_effacer_hist = ctk.CTkButton(
            frame_historique,
            text="🗑️ Effacer historique",
            width=150,
            fg_color="#8B0000",
            hover_color="#5C0000",
            command=self.effacer_historique
        )
        btn_effacer_hist.pack(side="left", padx=10)
    
    def ajouter_fonction(self, fonction):
        """
        Ajoute une fonction mathématique à l'expression. 
        Ajoute "fonction(" à l'expression courante.
        
        Args:
            fonction: Le nom de la fonction (sin, cos, sqrt, min, max, etc.)
        """
        self.expression_courante += f"{fonction}("
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
        self.label_erreur.configure(text="")
    
    def ajouter_caractere(self, caractere):
        """
        Ajoute un caractère à l'expression courante.
        
        Args:
            caractere: Le caractère à ajouter
        """
        self.expression_courante += str(caractere)
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
        self.label_erreur.configure(text="")
    
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
            
            # Formater le résultat
            if resultat == int(resultat):
                resultat_affiche = int(resultat)
            else:
                resultat_affiche = round(resultat, 10)
            
            self.label_resultat.configure(text=f"= {resultat_affiche}")
            self.historique.ajouter(expression, resultat_affiche)
            
        except CalculatriceError as e:
            self.label_erreur.configure(text=str(e))
        except Exception as e:
            self.label_erreur.configure(text=f"Erreur inattendue : {str(e)}")
    
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
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Historique des calculs")
        popup.geometry("500x400")
        
        titre = ctk.CTkLabel(
            popup,
            text="📊 Historique des calculs",
            font=("Arial", 20, "bold")
        )
        titre.pack(pady=10)
        
        frame_scroll = ctk.CTkScrollableFrame(popup, width=450, height=280)
        frame_scroll.pack(pady=10, padx=20, fill="both", expand=True)
        
        operations = self.historique.obtenir_historique()
        
        if not operations:
            label_vide = ctk.CTkLabel(
                frame_scroll,
                text="Aucun calcul dans l'historique",
                font=("Arial", 14),
                text_color="gray"
            )
            label_vide.pack(pady=20)
        else:
            for i, (expression, resultat, timestamp) in enumerate(operations, 1):
                frame_calcul = ctk.CTkFrame(frame_scroll)
                frame_calcul.pack(pady=5, padx=10, fill="x")
                
                label_info = ctk.CTkLabel(
                    frame_calcul,
                    text=f"#{i} - {timestamp}",
                    font=("Arial", 10),
                    text_color="gray"
                )
                label_info.pack(anchor="w", padx=10, pady=2)
                
                label_calcul = ctk.CTkLabel(
                    frame_calcul,
                    text=f"{expression} = {resultat}",
                    font=("Arial", 14, "bold")
                )
                label_calcul.pack(anchor="w", padx=10, pady=5)
        
        btn_fermer = ctk.CTkButton(popup, text="Fermer", command=popup.destroy, width=120)
        btn_fermer.pack(pady=10)
    
    def effacer_historique(self):
        """Efface l'historique"""
        reponse = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment effacer tout l'historique ?"
        )
        if reponse:
            self.historique.effacer()
            messagebox.showinfo("Succès", "Historique effacé !")
    
    def run(self):
        """Lance l'application"""
        self.fenetre.mainloop()