"""
================================================================================
Module de l'interface graphique de la calculatrice - VERSION 3.1
================================================================================
Utilise CustomTkinter pour un design moderne.  

NOUVEAUTÉS V2.0 :
- Boutons fonctions scientifiques (sqrt, abs, sin, cos, tan)
- Boutons min, max pour comparer deux nombres
- Bouton % pour le modulo
- Support des nombres négatifs avec le signe -

VERSION 3.0 - FONCTIONNALITÉS COMPLÈTES : 
-----------------------------------------
    - Raccourcis clavier complets
    - Bouton ANS (dernier résultat)
    - Copier le résultat dans le presse-papier
    - Nouvelles fonctions :  ln, log, exp, inv, sqr
    - Constantes :  PI, E
    - Opérateur puissance ^
    - Mode degrés/radians pour la trigonométrie
    - Affichage en fractions
    - Export historique (CSV/TXT)
    - Recherche dans l'historique
    - Graphiques de fonctions
    - Calcul de pourcentage intelligent
    
AMÉLIORATIONS V3.1 :
--------------------
    - Fenêtre redimensionnable (responsive)
    - ScrollableFrame pour les petits écrans
    - Couleurs améliorées pour meilleure lisibilité
    - Contraste optimisé
================================================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sys

from src.calculateur import calculer, obtenir_dernier_resultat
from src.validateur import Validateur
from src.historique import Historique
from src.exceptions import CalculatriceError
from src.fractions import decimal_vers_fraction_str

class CalculatriceGUI:  
    """
    Interface graphique de la calculatrice scientifique
    
    Gère l'affichage, les interactions utilisateur et toutes les fonctionnalités
    avancées (raccourcis clavier, export, graphiques, etc.).
    """
    
    def __init__(self):
        """Initialise l'interface graphique"""
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # =====================================================================
        # FENÊTRE PRINCIPALE 
        # =====================================================================
        self.fenetre = ctk.CTk()
        self.fenetre.title("Calculatrice Scientifique v3.1")
        self.fenetre.geometry("550x880")
        self.fenetre.resizable(False, False)
        
        # ✅ CHANGEMENT :  Rendre la fenêtre redimensionnable
        self.fenetre.resizable(True, True)  # Largeur et hauteur ajustables
        
        # Taille minimale pour éviter que la fenêtre soit trop petite
        self.fenetre.minsize(500, 600)
        
        # Modules
        self.validateur = Validateur()
        self.historique = Historique()
        
        # Variables
        self.expression_courante = ""
        self.mode_degres = False  # False = radians, True = degrés
        self.afficher_fractions = False  # False = décimal, True = fractions
        
        # Raccourci clavier
        self._configurer_raccourcis_clavier()
        
        # Créer l'interface
        self.creer_interface()
    
    def _configurer_raccourcis_clavier(self):
        """
        Configure tous les raccourcis clavier pour faciliter l'utilisation.
        
        L'utilisateur peut taper directement au clavier au lieu de cliquer. 
        """
        # =====================================================================
        # TOUCHES SPÉCIALES
        # =====================================================================
        # Entrée = calculer
        self.fenetre.bind('<Return>', lambda e: self.calculer_expression())
        self.fenetre.bind('<KP_Enter>', lambda e: self.calculer_expression())
        
        # Échap = effacer tout
        self.fenetre.bind('<Escape>', lambda e: self.effacer())
        
        # Backspace = effacer dernier caractère
        self.fenetre.bind('<BackSpace>', lambda e: self.effacer_dernier())
        
        # =====================================================================
        # CHIFFRES (clavier principal et pavé numérique)
        # =====================================================================
        for i in range(10):
            # Clavier principal
            self.fenetre.bind(str(i), lambda e, c=str(i): self.ajouter_caractere(c))
            # Pavé numérique
            self.fenetre.bind(f'<KP_{i}>', lambda e, c=str(i): self.ajouter_caractere(c))
        
        # =====================================================================
        # OPÉRATEURS
        # =====================================================================
        self.fenetre.bind('+', lambda e: self.ajouter_caractere('+'))
        self.fenetre.bind('<KP_Add>', lambda e: self.ajouter_caractere('+'))
        
        self.fenetre.bind('-', lambda e: self.ajouter_caractere('-'))
        self.fenetre.bind('<KP_Subtract>', lambda e:  self.ajouter_caractere('-'))
        
        self.fenetre.bind('*', lambda e: self.ajouter_caractere('*'))
        self.fenetre.bind('<KP_Multiply>', lambda e: self.ajouter_caractere('*'))
        
        self.fenetre.bind('/', lambda e: self.ajouter_caractere('/'))
        self.fenetre.bind('<KP_Divide>', lambda e: self.ajouter_caractere('/'))
        
        self.fenetre.bind('%', lambda e: self.ajouter_caractere('%'))
        self.fenetre.bind('^', lambda e: self.ajouter_caractere('^'))
        
        # =====================================================================
        # AUTRES CARACTÈRES
        # =====================================================================
        self.fenetre.bind('.', lambda e: self.ajouter_caractere('.'))
        self.fenetre.bind('<KP_Decimal>', lambda e: self.ajouter_caractere('.'))
        
        self.fenetre.bind(',', lambda e: self.ajouter_caractere(','))
        self.fenetre.bind('(', lambda e: self.ajouter_caractere('('))
        self.fenetre.bind(')', lambda e: self.ajouter_caractere(')'))
        
    def creer_interface(self):
        """Crée tous les éléments de l'interface"""
        
        # =====================================================================
        # FRAME SCROLLABLE PRINCIPAL
        # =====================================================================
        # Cela permet de faire défiler si l'écran est trop petit
        self.frame_principal = ctk.CTkScrollableFrame(
            self.fenetre,
            fg_color="transparent"
        )
        self.frame_principal.pack(fill="both", expand=True, padx=5, pady=5)
        
        # =====================================================================
        # BARRE DE MENU SUPÉRIEURE
        # =====================================================================
        frame_menu = ctk.CTkFrame(self.frame_principal, height=40)
        frame_menu.pack(pady=5, padx=10, fill="x")
        
        # Bouton mode Deg/Rad
        self.btn_mode_angle = ctk.CTkButton(
            frame_menu,
            text="RAD",
            width=60,
            height=30,
            font=("Arial", 12, "bold"),
            fg_color="#E63946",
            hover_color="#C62828",
            command=self.basculer_mode_angle
        )
        self.btn_mode_angle.pack(side="left", padx=5)
        
        # Bouton mode Fraction/Décimal
        self.btn_mode_fraction = ctk.CTkButton(
            frame_menu,
            text="DEC",
            width=60,
            height=30,
            font=("Arial", 12, "bold"),
            fg_color="#2A9D8F",
            hover_color="#1B7A6E",
            command=self.basculer_mode_fraction
        )
        self.btn_mode_fraction.pack(side="left", padx=5)
        
        # Bouton Graphique
        btn_graphique = ctk.CTkButton(
            frame_menu,
            text="Graph",
            width=80,
            height=30,
            font=("Arial", 12),
            command=self.ouvrir_graphique
        )
        btn_graphique.pack(side="left", padx=5)
        
        # Bouton Aide
        btn_aide = ctk.CTkButton(
            frame_menu,
            text="Aide",
            width=40,
            height=30,
            font=("Arial", 12),
            command=self.afficher_aide
        )
        btn_aide.pack(side="right", padx=5)
        
        # =====================================================================
        # ÉCRAN D'AFFICHAGE
        # =====================================================================
        self.ecran = ctk.CTkEntry(
            self.frame_principal,
            font=("Arial", 24),
            height=60,
            justify="right"
        )
        self.ecran.pack(pady=15, padx=20, fill="x")
        
        # Label pour le résultat (en vert)
        self.label_resultat = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 18),
            text_color="#00C853"
        )
        self.label_resultat.pack(pady=5)
        
        # Label pour les erreurs (en rouge)
        self.label_erreur = ctk.CTkLabel(
            self.frame_principal,
            text="",
            font=("Arial", 12),
            text_color="#FF5252"
        )
        self.label_erreur.pack(pady=5)
        
        # =====================================================================
        # FRAME CONSTANTES (PI, E, ANS)
        # =====================================================================
        frame_constantes = ctk.CTkFrame(self.frame_principal)
        frame_constantes.pack(pady=5, padx=20)
        
        boutons_constantes = [
            ('π', 'PI', '#E63946', "white"),
            ('e', 'E', '#2A9D8F', "white"),
            ('ANS', 'ANS', '#457B9D', "white")
        ]
        
        for texte_affiche, valeur, couleur, couleur_texte in boutons_constantes:
            btn = ctk.CTkButton(
                frame_constantes,
                text=texte_affiche,
                width=70,
                height=35,
                font=("Arial", 14, "bold"),
                fg_color=couleur,
                hover_color=self._assombrir_couleur(couleur),
                text_color=couleur_texte,
                command=lambda v=valeur: self.ajouter_caractere(v)
            )
            btn.pack(side="left", padx=5)
        
        # Bouton copier résultat
        btn_copier = ctk.CTkButton(
            frame_constantes,
            text="Copier",
            width=90,
            height=35,
            font=("Arial", 12),
            fg_color="#F77F00",
            hover_color="#D66D00",
            text_color="white",
            command=self.copier_resultat
        )
        btn_copier.pack(side="left", padx=5)
        
        # =====================================================================
        # FRAME FONCTIONS AVANCÉES (ln, log, exp, etc.)
        # =====================================================================
        frame_fonctions_avancees = ctk.CTkFrame(self.frame_principal)
        frame_fonctions_avancees.pack(pady=5, padx=20)
        
        boutons_avances_ligne1 = ['ln', 'log', 'exp', '^', 'inv']
        for texte in boutons_avances_ligne1:
            if texte == '^':
                btn = ctk.CTkButton(
                    frame_fonctions_avancees,
                    text=texte,
                    width=90,
                    height=35,
                    font=("Arial", 14),
                    fg_color="#06A77D",
                    hover_color="#048A67",
                    text_color="white",
                    command=lambda t=texte: self.ajouter_caractere(t)
                )
            else:
                btn = ctk.CTkButton(
                    frame_fonctions_avancees,
                    text=texte,
                    width=90,
                    height=35,
                    font=("Arial", 14),
                    fg_color="#06A77D",
                    hover_color="#048A67",
                    command=lambda t=texte: self.ajouter_fonction(t)
                )
            btn.grid(row=0, column=boutons_avances_ligne1.index(texte), padx=3, pady=3)
        
        # =====================================================================
        # FRAME POUR LES BOUTONS SCIENTIFIQUES
        # =====================================================================
        frame_scientifique = ctk.CTkFrame(self.frame_principal)
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
        frame_boutons = ctk.CTkFrame(self.frame_principal)
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
        # BOUTONS D'HISTORIQUE
        # =====================================================================
        frame_historique = ctk.CTkFrame(self.frame_principal)
        frame_historique.pack(pady=15)
        
        btn_voir_hist = ctk.CTkButton(
            frame_historique,
            text="📊 Voir",
            width=100,
            command=self.afficher_historique
        )
        btn_voir_hist.pack(side="left", padx=5)
        
        btn_rechercher_hist = ctk.CTkButton(
            frame_historique,
            text="🔍 Rechercher",
            width=120,
            command=self.rechercher_historique
        )
        btn_rechercher_hist.pack(side="left", padx=5)
        
        btn_exporter_hist = ctk.CTkButton(
            frame_historique,
            text="💾 Export",
            width=100,
            command=self.exporter_historique
        )
        btn_exporter_hist.pack(side="left", padx=5)
        
        btn_effacer_hist = ctk.CTkButton(
            frame_historique,
            text="🗑️ Effacer",
            width=100,
            fg_color="#8B0000",
            hover_color="#5C0000",
            command=self.effacer_historique
        )
        btn_effacer_hist.pack(side="left", padx=5)
    
    # =========================================================================
    # MÉTHODES D'INTERACTION
    # =========================================================================
    
    def ajouter_fonction(self, fonction):
        """
        Ajoute une fonction mathématique à l'expression. 
        
        Args:
            fonction:  Le nom de la fonction (ex: "sin", "sqrt", "ln")
        """
        self.expression_courante += f"{fonction}("
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
        self.label_erreur.configure(text="")
    
    def ajouter_caractere(self, caractere):
        """
        Ajoute un caractère à l'expression courante.
        
        Args:
            caractere: Le caractère à ajouter (chiffre, opérateur, constante)
        """
        self.expression_courante += str(caractere)
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
        self.label_erreur.configure(text="")
    
    def calculer_expression(self):
        """
        Calcule l'expression saisie.
        
        Cette méthode : 
        1. Récupère l'expression
        2. La valide
        3. La calcule
        4. Affiche le résultat (décimal ou fraction selon le mode)
        5. Gère le calcul de pourcentage intelligent
        6. Ajoute à l'historique
        """
        expression = self.ecran.get()
        
        # Effacer les messages précédents
        self.label_erreur.configure(text="")
        self.label_resultat.configure(text="")
        
        # =====================================================================
        # GESTION INTELLIGENTE DU POURCENTAGE
        # =====================================================================
        # Si l'expression se termine par "%", c'est un calcul de pourcentage
        # Exemples : 
        #   "100 + 20%" → 100 + (100 * 20 / 100) = 120 (TVA)
        #   "200 - 15%" → 200 - (200 * 15 / 100) = 170 (réduction)
        if '%' in expression and ('+' in expression or '-' in expression):
            expression = self._traiter_pourcentage(expression)
        
        # =====================================================================
        # VALIDATION
        # =====================================================================
        valide, message_erreur = self.validateur.valider_expression(expression)
        if not valide:
            self.label_erreur.configure(text=message_erreur)
            return
        
        # =====================================================================
        # CALCUL
        # =====================================================================
        try:
            # Calculer avec le bon mode (degrés ou radians)
            resultat = calculer(expression, utiliser_degres=self.mode_degres)
            
            # Formater le résultat
            if self.afficher_fractions:
                # Mode fraction
                resultat_affiche = decimal_vers_fraction_str(resultat)
                self.label_resultat.configure(text=f"= {resultat_affiche}")
            else:
                # Mode décimal
                if resultat == int(resultat):
                    resultat_affiche = int(resultat)
                else: 
                    resultat_affiche = round(resultat, 10)
                self.label_resultat.configure(text=f"= {resultat_affiche}")
            
            # Ajouter à l'historique
            self.historique.ajouter(expression, resultat)
            
        except CalculatriceError as e: 
            self.label_erreur.configure(text=str(e))
        except Exception as e:
            self.label_erreur.configure(text=f"Erreur inattendue :  {str(e)}")
    
    def _traiter_pourcentage(self, expression:  str) -> str:
        """
        Traite les calculs de pourcentage intelligents. 
        
        Convertit "100 + 20%" en "100 + (100 * 20 / 100)"
        
        Args:
            expression: L'expression contenant un %
        
        Returns:
            str: L'expression transformée
        """
        # Trouver l'opérateur (+ ou -)
        if '+' in expression:
            operateur = '+'
        elif '-' in expression:
            operateur = '-'
        else: 
            return expression  # Pas de traitement spécial
        
        # Séparer base et pourcentage
        parties = expression.split(operateur)
        if len(parties) == 2:
            base = parties[0].strip()
            pourcentage_str = parties[1].strip().replace('%', '')
            
            # Construire la nouvelle expression
            nouvelle_expr = f"{base} {operateur} ({base} * {pourcentage_str} / 100)"
            return nouvelle_expr
        
        return expression
    
    def effacer(self):
        """Efface tout (bouton C - Clear)."""
        self.expression_courante = ""
        self.ecran.delete(0, "end")
        self.label_erreur.configure(text="")
        self.label_resultat.configure(text="")
    
    def effacer_dernier(self):
        """Efface le dernier caractère (bouton CE - Clear Entry)."""
        self.expression_courante = self.expression_courante[:-1]
        self.ecran.delete(0, "end")
        self.ecran.insert(0, self.expression_courante)
    
    # =========================================================================
    # MÉTHODES POUR LES MODES
    # =========================================================================
    
    def basculer_mode_angle(self):
        """
        Bascule entre radians et degrés pour les fonctions trigonométriques. 
        
        RAD → DEG → RAD ... 
        """
        self.mode_degres = not self.mode_degres
        
        if self.mode_degres:
            self.btn_mode_angle.configure(text="DEG", fg_color="#4CAF50")
        else:
            self.btn_mode_angle.configure(text="RAD", fg_color="#FF6B6B")
    
    def basculer_mode_fraction(self):
        """
        Bascule entre affichage décimal et fractionnel.
        
        DEC → FRAC → DEC ...
        """
        self.afficher_fractions = not self.afficher_fractions
        
        if self.afficher_fractions:
            self.btn_mode_fraction.configure(text="FRAC", fg_color="#FF9800")
        else:
            self.btn_mode_fraction.configure(text="DEC", fg_color="#4ECDC4")
    
    # =========================================================================
    # MÉTHODES POUR COPIER/COLLER
    # =========================================================================
    
    def copier_resultat(self):
        """
        Copie le dernier résultat dans le presse-papier.
        
        Utilise le module tkinter pour accéder au clipboard.
        """
        dernier = obtenir_dernier_resultat()
        
        if dernier is not None:
            # Copier dans le presse-papier
            self.fenetre.clipboard_clear()
            self.fenetre.clipboard_append(str(dernier))
            self.fenetre.update()  # Nécessaire pour que le clipboard soit mis à jour
            
            # Afficher une confirmation
            self.label_resultat.configure(
                text=f"✓ {dernier} copié ! ",
                text_color="#4CAF50"
            )
        else:
            self.label_erreur.configure(text="Aucun résultat à copier")
    
    # =========================================================================
    # MÉTHODES POUR L'HISTORIQUE
    # =========================================================================
    
    def afficher_historique(self):
        """Affiche une fenêtre popup avec l'historique complet."""
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Historique des calculs")
        popup.geometry("600x500")
        
        titre = ctk.CTkLabel(
            popup,
            text="📊 Historique des calculs",
            font=("Arial", 20, "bold")
        )
        titre.pack(pady=10)
        
        frame_scroll = ctk.CTkScrollableFrame(popup, width=550, height=350)
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
                
                # Formater le timestamp
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp_format = dt.strftime("%d/%m/%Y %H:%M:%S")
                except:
                    timestamp_format = timestamp
                
                label_info = ctk.CTkLabel(
                    frame_calcul,
                    text=f"#{i} - {timestamp_format}",
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
    
    def rechercher_historique(self):
        """Ouvre une fenêtre de recherche dans l'historique."""
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Rechercher dans l'historique")
        popup.geometry("500x400")
        
        titre = ctk.CTkLabel(
            popup,
            text="🔍 Rechercher dans l'historique",
            font=("Arial", 18, "bold")
        )
        titre.pack(pady=10)
        
        # Champ de recherche
        frame_recherche = ctk.CTkFrame(popup)
        frame_recherche.pack(pady=10, padx=20, fill="x")
        
        entry_recherche = ctk.CTkEntry(
            frame_recherche,
            placeholder_text="Tapez un terme à rechercher...",
            font=("Arial", 14),
            width=350
        )
        entry_recherche.pack(side="left", padx=5)
        
        # Zone de résultats
        frame_resultats = ctk.CTkScrollableFrame(popup, width=450, height=250)
        frame_resultats.pack(pady=10, padx=20, fill="both", expand=True)
        
        label_info = ctk.CTkLabel(
            frame_resultats,
            text="Tapez un terme et appuyez sur Entrée",
            font=("Arial", 12),
            text_color="gray"
        )
        label_info.pack(pady=20)
        
        def effectuer_recherche(event=None):
            """Effectue la recherche et affiche les résultats."""
            terme = entry_recherche.get()
            
            # Effacer les résultats précédents
            for widget in frame_resultats.winfo_children():
                widget.destroy()
            
            if not terme:
                label_vide = ctk.CTkLabel(
                    frame_resultats,
                    text="Tapez un terme à rechercher",
                    font=("Arial", 12),
                    text_color="gray"
                )
                label_vide.pack(pady=20)
                return
            
            # Rechercher
            resultats = self.historique.rechercher(terme)
            
            if not resultats:
                label_vide = ctk.CTkLabel(
                    frame_resultats,
                    text=f"Aucun résultat pour '{terme}'",
                    font=("Arial", 12),
                    text_color="orange"
                )
                label_vide.pack(pady=20)
            else:
                for i, op in enumerate(resultats, 1):
                    frame_res = ctk.CTkFrame(frame_resultats)
                    frame_res.pack(pady=3, padx=5, fill="x")
                    
                    label_res = ctk.CTkLabel(
                        frame_res,
                        text=f"{op['expression']} = {op['resultat']}",
                        font=("Arial", 12)
                    )
                    label_res.pack(padx=10, pady=5)
        
        # Bouton rechercher
        btn_rechercher = ctk.CTkButton(
            frame_recherche,
            text="🔍",
            width=50,
            command=effectuer_recherche
        )
        btn_rechercher.pack(side="left", padx=5)
        
        # Lier la touche Entrée
        entry_recherche.bind('<Return>', effectuer_recherche)
        
        btn_fermer = ctk.CTkButton(popup, text="Fermer", command=popup.destroy, width=120)
        btn_fermer.pack(pady=10)
    
    def exporter_historique(self):
        """Exporte l'historique en CSV ou TXT."""
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Exporter l'historique")
        popup.geometry("400x200")
        
        titre = ctk.CTkLabel(
            popup,
            text="💾 Exporter l'historique",
            font=("Arial", 18, "bold")
        )
        titre.pack(pady=20)
        
        label_info = ctk.CTkLabel(
            popup,
            text="Choisissez le format d'export :",
            font=("Arial", 14)
        )
        label_info.pack(pady=10)
        
        frame_boutons = ctk.CTkFrame(popup)
        frame_boutons.pack(pady=20)
        
        def exporter_csv():
            """Exporte en CSV."""
            succes = self.historique.exporter_csv()
            if succes:
                messagebox.showinfo("Succès", "Historique exporté en CSV !")
                popup.destroy()
        
        def exporter_txt():
            """Exporte en TXT."""
            succes = self.historique.exporter_texte()
            if succes: 
                messagebox.showinfo("Succès", "Historique exporté en TXT !")
                popup.destroy()
        
        btn_csv = ctk.CTkButton(
            frame_boutons,
            text="📄 CSV",
            width=120,
            command=exporter_csv
        )
        btn_csv.pack(side="left", padx=10)
        
        btn_txt = ctk.CTkButton(
            frame_boutons,
            text="📝 TXT",
            width=120,
            command=exporter_txt
        )
        btn_txt.pack(side="left", padx=10)
    
    def effacer_historique(self):
        """Efface tout l'historique après confirmation."""
        reponse = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment effacer tout l'historique ?"
        )
        if reponse: 
            self.historique.effacer()
            messagebox.showinfo("Succès", "Historique effacé !")
    
    # =========================================================================
    # MÉTHODES POUR LES GRAPHIQUES
    # =========================================================================
    
    def ouvrir_graphique(self):
        """Ouvre la fenêtre de graphique de fonctions."""
        try:
            from src.graphique import FenetreGraphique
            FenetreGraphique(self.fenetre)
        except ImportError: 
            messagebox.showerror(
                "Erreur",
                "Le module graphique n'est pas disponible"
            )
    
    # =========================================================================
    # MÉTHODE D'AIDE
    # =========================================================================
    
    def afficher_aide(self):
        """Affiche une fenêtre d'aide avec les raccourcis et fonctions."""
        popup = ctk.CTkToplevel(self.fenetre)
        popup.title("Aide - Calculatrice v3.0")
        popup.geometry("700x600")
        
        titre = ctk.CTkLabel(
            popup,
            text="❓ Aide - Calculatrice Scientifique",
            font=("Arial", 20, "bold")
        )
        titre.pack(pady=10)
        
        frame_scroll = ctk.CTkScrollableFrame(popup, width=650, height=480)
        frame_scroll.pack(pady=10, padx=20, fill="both", expand=True)
        
        aide_texte = """
🎯 RACCOURCIS CLAVIER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Entrée : Calculer
• Échap : Effacer tout
• Backspace : Effacer le dernier caractère
• 0-9 : Chiffres
• + - * / % ^ :  Opérateurs
• ( ) : Parenthèses
• .  , :  Séparateurs

📐 FONCTIONS MATHÉMATIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• sqrt(x) : Racine carrée
• sqr(x) : Carré (x²)
• abs(x) : Valeur absolue
• inv(x) : Inverse (1/x)
• ln(x) : Logarithme népérien
• log(x) : Logarithme base 10
• exp(x) : Exponentielle (e^x)

📊 TRIGONOMÉTRIE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━���━━━━━
• sin(x), cos(x), tan(x) : En radians
• sind(x), cosd(x), tand(x) : En degrés
• Mode RAD/DEG : Basculer le mode

🔢 CONSTANTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• PI : 3.14159... 
• E : 2.71828...
• ANS :  Dernier résultat

💡 FONCTIONS SPÉCIALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• min(a,b) : Minimum
• max(a,b) : Maximum
• a^b : Puissance
• a%b : Modulo

💰 CALCUL DE POURCENTAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 100 + 20% → 120 (TVA)
• 200 - 15% → 170 (réduction)

🎨 MODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• DEC/FRAC : Affichage décimal ou fraction
• RAD/DEG : Trigonométrie en radians ou degrés

📚 HISTORIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Voir :  Afficher tout l'historique
• Rechercher : Chercher un terme
• Export : Sauvegarder en CSV ou TXT
• Effacer : Vider l'historique

📈 GRAPHIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Bouton Graph : Dessiner des fonctions
• Exemples : sin(x), x^2, ln(x)
        """
        
        label_aide = ctk.CTkLabel(
            frame_scroll,
            text=aide_texte,
            font=("Courier", 11),
            justify="left"
        )
        label_aide.pack(padx=20, pady=10)
        
        btn_fermer = ctk.CTkButton(popup, text="Fermer", command=popup.destroy, width=120)
        btn_fermer.pack(pady=10)
    
    # =========================================================================
    # MÉTHODES UTILITAIRES
    # =========================================================================
    
    def _assombrir_couleur(self, couleur_hex:  str) -> str:
        """
        Assombrit une couleur hexadécimale de 20%. 
        
        Args:
            couleur_hex: Couleur au format "#RRGGBB"
        
        Returns:
            str: Couleur assombrie
        """
        # Retirer le #
        couleur = couleur_hex.lstrip('#')
        
        # Convertir en RGB
        r = int(couleur[0:2], 16)
        g = int(couleur[2:4], 16)
        b = int(couleur[4:6], 16)
        
        # Assombrir de 20%
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        
        # Reconvertir en hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def run(self):
        """Lance l'application et démarre la boucle principale."""
        self.fenetre.mainloop()