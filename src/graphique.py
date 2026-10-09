# src/graphique.py
"""
================================================================================
Module de dessin de graphiques de fonctions - VERSION 3.0
================================================================================

Permet de dessiner des graphiques de fonctions mathématiques sur un Canvas tkinter. 

FONCTIONNALITÉS : 
-----------------
    - Dessiner n'importe quelle fonction (sin, cos, x^2, ln, etc.)
    - Zoom et navigation
    - Grille et axes
    - Affichage des valeurs
    - Export en image (optionnel)

SANS utiliser matplotlib (on dessine directement sur un Canvas tkinter).

================================================================================
"""

import re
import customtkinter as ctk
from tkinter import Canvas, messagebox
from src.calculateur import (
    calculer,
    obtenir_dernier_resultat,
    definir_dernier_resultat,
)
from src.exceptions import CalculatriceError


class FenetreGraphique:
    """
    Fenêtre pour dessiner des graphiques de fonctions mathématiques.
    
    L'utilisateur entre une fonction de x (ex: sin(x), x^2, ln(x))
    et le graphique est dessiné sur un Canvas.
    """
    
    def __init__(self, parent):
        """
        Initialise la fenêtre de graphique. 
        
        Args:
            parent: La fenêtre parent (pour la rendre modale)
        """
        # =====================================================================
        # CRÉER LA FENÊTRE TOPLEVEL
        # =====================================================================
        self.fenetre = ctk.CTkToplevel(parent)
        self.fenetre.title("Graphique de fonctions")
        self.fenetre.geometry("900x700")
        
        # =====================================================================
        # PARAMÈTRES DU GRAPHIQUE
        # =====================================================================
        self.x_min = -10.0  # Limite gauche de l'axe X
        self.x_max = 10.0   # Limite droite de l'axe X
        self.y_min = -10.0  # Limite basse de l'axe Y
        self.y_max = 10.0   # Limite haute de l'axe Y
        
        self.largeur_canvas = 800  # Largeur du canvas en pixels
        self.hauteur_canvas = 600  # Hauteur du canvas en pixels

        # Dernière fonction tracée (None si aucune) : permet de la redessiner
        # automatiquement après un zoom.
        self.fonction_courante = None

        # =====================================================================
        # CRÉER L'INTERFACE
        # =====================================================================
        self._creer_interface()
    
    def _creer_interface(self):
        """Crée tous les éléments de l'interface graphique."""
        # =====================================================================
        # FRAME SUPÉRIEUR :  SAISIE DE LA FONCTION
        # =====================================================================
        frame_haut = ctk.CTkFrame(self.fenetre)
        frame_haut.pack(pady=10, padx=20, fill="x")
        
        label_titre = ctk.CTkLabel(
            frame_haut,
            text="📈 Graphique de fonctions",
            font=("Arial", 18, "bold")
        )
        label_titre.pack(pady=5)
        
        label_info = ctk.CTkLabel(
            frame_haut,
            text="Entrez une fonction de x (ex: sin(x), x^2, ln(x), 2*x+3)",
            font=("Arial", 12)
        )
        label_info.pack(pady=5)
        
        # Frame pour la saisie
        frame_saisie = ctk.CTkFrame(frame_haut)
        frame_saisie.pack(pady=10)
        
        label_fonction = ctk.CTkLabel(
            frame_saisie,
            text="f(x) =",
            font=("Arial", 14, "bold")
        )
        label_fonction.pack(side="left", padx=5)
        
        self.entry_fonction = ctk.CTkEntry(
            frame_saisie,
            width=400,
            font=("Arial", 14),
            placeholder_text="sin(x)"
        )
        self.entry_fonction.pack(side="left", padx=5)
        
        btn_dessiner = ctk.CTkButton(
            frame_saisie,
            text="🎨 Dessiner",
            width=120,
            font=("Arial", 14, "bold"),
            fg_color="green",
            hover_color="darkgreen",
            command=self.dessiner_fonction
        )
        btn_dessiner.pack(side="left", padx=5)
        
        # Lier la touche Entrée
        self.entry_fonction.bind('<Return>', lambda e: self.dessiner_fonction())
        
        # =====================================================================
        # FRAME MILIEU : CANVAS POUR LE GRAPHIQUE
        # =====================================================================
        frame_canvas = ctk.CTkFrame(self.fenetre)
        frame_canvas.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas tkinter classique (CustomTkinter n'a pas de Canvas)
        self.canvas = Canvas(
            frame_canvas,
            width=self.largeur_canvas,
            height=self.hauteur_canvas,
            bg="#1e1e1e",  # Fond sombre
            highlightthickness=1,
            highlightbackground="#444444"
        )
        self.canvas.pack()
        
        # =====================================================================
        # FRAME BAS : BOUTONS DE CONTRÔLE
        # =====================================================================
        frame_bas = ctk.CTkFrame(self.fenetre)
        frame_bas.pack(pady=10, padx=20, fill="x")
        
        # Boutons de zoom
        btn_zoom_plus = ctk.CTkButton(
            frame_bas,
            text="🔍 Zoom +",
            width=100,
            command=self.zoom_plus
        )
        btn_zoom_plus.pack(side="left", padx=5)
        
        btn_zoom_moins = ctk.CTkButton(
            frame_bas,
            text="🔍 Zoom -",
            width=100,
            command=self.zoom_moins
        )
        btn_zoom_moins.pack(side="left", padx=5)
        
        btn_reinitialiser = ctk.CTkButton(
            frame_bas,
            text="🔄 Réinitialiser",
            width=120,
            command=self.reinitialiser_zoom
        )
        btn_reinitialiser.pack(side="left", padx=5)
        
        btn_effacer = ctk.CTkButton(
            frame_bas,
            text="🗑️ Effacer",
            width=100,
            fg_color="red",
            hover_color="darkred",
            command=self.effacer_canvas
        )
        btn_effacer.pack(side="left", padx=5)
        
        # Label d'info
        self.label_info_bas = ctk.CTkLabel(
            frame_bas,
            text="Prêt à dessiner",
            font=("Arial", 11)
        )
        self.label_info_bas.pack(side="right", padx=10)
        
        # =====================================================================
        # DESSINER LA GRILLE ET LES AXES PAR DÉFAUT
        # =====================================================================
        self.dessiner_grille()
    
    # =========================================================================
    # MÉTHODES DE DESSIN
    # =========================================================================
    
    def dessiner_grille(self):
        """
        Dessine la grille, les axes X et Y et les graduations.
        """
        # Effacer le canvas
        self.canvas.delete("all")
        
        # =====================================================================
        # DESSINER LA GRILLE
        # =====================================================================
        # Lignes verticales
        pas_x = (self.x_max - self.x_min) / 20  # 20 lignes verticales
        for i in range(21):
            x_math = self.x_min + i * pas_x
            x_pixel = self._math_vers_pixel_x(x_math)
            
            self.canvas.create_line(
                x_pixel, 0,
                x_pixel, self.hauteur_canvas,
                fill="#333333",
                width=1
            )
        
        # Lignes horizontales
        pas_y = (self.y_max - self.y_min) / 20  # 20 lignes horizontales
        for i in range(21):
            y_math = self.y_min + i * pas_y
            y_pixel = self._math_vers_pixel_y(y_math)
            
            self.canvas.create_line(
                0, y_pixel,
                self.largeur_canvas, y_pixel,
                fill="#333333",
                width=1
            )
        
        # =====================================================================
        # DESSINER LES AXES
        # =====================================================================
        # Axe X (y = 0)
        if self.y_min <= 0 <= self.y_max:
            y_pixel = self._math_vers_pixel_y(0)
            self.canvas.create_line(
                0, y_pixel,
                self.largeur_canvas, y_pixel,
                fill="white",
                width=2
            )
            # Label de l'axe X
            self.canvas.create_text(
                self.largeur_canvas - 20, y_pixel - 15,
                text="X",
                fill="white",
                font=("Arial", 12, "bold")
            )
        
        # Axe Y (x = 0)
        if self.x_min <= 0 <= self.x_max:
            x_pixel = self._math_vers_pixel_x(0)
            self.canvas.create_line(
                x_pixel, 0,
                x_pixel, self.hauteur_canvas,
                fill="white",
                width=2
            )
            # Label de l'axe Y
            self.canvas.create_text(
                x_pixel + 15, 20,
                text="Y",
                fill="white",
                font=("Arial", 12, "bold")
            )
        
        # =====================================================================
        # DESSINER LES GRADUATIONS
        # =====================================================================
        # Graduations sur l'axe X
        if self.y_min <= 0 <= self.y_max:
            y_pixel_axe = self._math_vers_pixel_y(0)
            pas_graduation = max(1, int((self.x_max - self.x_min) / 10))
            
            x_grad = int(self.x_min)
            while x_grad <= self.x_max:
                if x_grad != 0:  # Ne pas afficher 0 deux fois
                    x_pixel = self._math_vers_pixel_x(x_grad)
                    # Petit trait
                    self.canvas.create_line(
                        x_pixel, y_pixel_axe - 5,
                        x_pixel, y_pixel_axe + 5,
                        fill="white",
                        width=2
                    )
                    # Texte
                    self.canvas.create_text(
                        x_pixel, y_pixel_axe + 15,
                        text=str(x_grad),
                        fill="white",
                        font=("Arial", 9)
                    )
                x_grad += pas_graduation
        
        # Graduations sur l'axe Y
        if self.x_min <= 0 <= self.x_max:
            x_pixel_axe = self._math_vers_pixel_x(0)
            pas_graduation = max(1, int((self.y_max - self.y_min) / 10))
            
            y_grad = int(self.y_min)
            while y_grad <= self.y_max:
                if y_grad != 0:
                    y_pixel = self._math_vers_pixel_y(y_grad)
                    # Petit trait
                    self.canvas.create_line(
                        x_pixel_axe - 5, y_pixel,
                        x_pixel_axe + 5, y_pixel,
                        fill="white",
                        width=2
                    )
                    # Texte
                    self.canvas.create_text(
                        x_pixel_axe - 20, y_pixel,
                        text=str(y_grad),
                        fill="white",
                        font=("Arial", 9)
                    )
                y_grad += pas_graduation
        
        # Origine (0, 0)
        if self.x_min <= 0 <= self.x_max and self.y_min <= 0 <= self.y_max:
            x_pixel = self._math_vers_pixel_x(0)
            y_pixel = self._math_vers_pixel_y(0)
            self.canvas.create_text(
                x_pixel + 15, y_pixel + 15,
                text="0",
                fill="white",
                font=("Arial", 10, "bold")
            )
    
    def dessiner_fonction(self):
        """
        Dessine la courbe de la fonction saisie par l'utilisateur.
        """
        # Récupérer la fonction
        fonction_str = self.entry_fonction.get().strip()

        if not fonction_str:
            messagebox.showwarning("Attention", "Veuillez entrer une fonction !")
            return

        # Mémoriser la fonction affichée pour pouvoir la redessiner après un
        # zoom (sinon la courbe disparaissait au premier zoom).
        self.fonction_courante = fonction_str
        self._tracer(fonction_str, silencieux=False)

    def _tracer(self, fonction_str, silencieux=False):
        """
        Trace la courbe d'une fonction sur la grille.

        Args:
            fonction_str: La fonction de x à tracer
            silencieux: Si True, ne pas afficher de boîte de dialogue en cas
                d'échec (utilisé lors d'un zoom automatique)
        """
        # Redessiner la grille
        self.dessiner_grille()

        # =====================================================================
        # CALCULER LES POINTS DE LA COURBE
        # =====================================================================
        points = []
        nb_points = 1000  # Nombre de points à calculer (plus = plus lisse)

        pas = (self.x_max - self.x_min) / nb_points

        erreurs = 0  # Compter les erreurs

        # Le calcul met à jour le dernier résultat global (utilisé par ANS).
        # On le sauvegarde pour le restaurer à la fin : dessiner une courbe ne
        # doit pas remplacer le résultat courant de la calculatrice.
        resultat_avant_dessin = obtenir_dernier_resultat()

        for i in range(nb_points + 1):
            x_math = self.x_min + i * pas

            # Remplacer la variable 'x' par la valeur actuelle. On utilise un
            # motif à limites de mot : un simple .replace('x', ...) corrompait
            # les noms de fonctions contenant un x (« exp(x) » devenait
            # « e(-2.0)p((-2.0)) », « max(x,0) » devenait « ma(-2.0)((-2.0),0) »).
            expression = re.sub(
                r'(?<![A-Za-z])x(?![A-Za-z])', f'({x_math})', fonction_str
            )

            try:
                # Calculer y = f(x)
                y_math = calculer(expression)

                # Vérifier que y est dans les limites (éviter les infinis)
                if abs(y_math) < 1e6:
                    x_pixel = self._math_vers_pixel_x(x_math)
                    y_pixel = self._math_vers_pixel_y(y_math)
                    points.append((x_pixel, y_pixel))
                else:
                    # Valeur trop grande, on ignore ce point
                    points.append(None)

            except CalculatriceError:
                # Erreur de calcul (ex: ln(-5), division par 0)
                erreurs += 1
                points.append(None)

            except Exception:
                # Autre erreur
                erreurs += 1
                points.append(None)

        # Restaurer le dernier résultat d'avant le tracé
        definir_dernier_resultat(resultat_avant_dessin)

        # =====================================================================
        # DESSINER LA COURBE
        # =====================================================================
        if not any(p is not None for p in points):
            if not silencieux:
                messagebox.showerror(
                    "Erreur",
                    "Impossible de calculer la fonction.\n"
                    "Vérifiez la syntaxe (ex: sin(x), x^2, ln(x))"
                )
            self.label_info_bas.configure(text="Erreur de calcul")
            return

        # Dessiner les segments entre les points consécutifs
        for i in range(len(points) - 1):
            if points[i] is not None and points[i + 1] is not None:
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Vérifier que les points sont dans le canvas
                if (0 <= x1 <= self.largeur_canvas and 
                    0 <= y1 <= self.hauteur_canvas and
                    0 <= x2 <= self.largeur_canvas and 
                    0 <= y2 <= self.hauteur_canvas):
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#00FF00",  # Vert vif
                        width=2,
                        smooth=True
                    )
        
        # Afficher les infos
        if erreurs > 0:
            self.label_info_bas.configure(
                text=f"✓ Fonction dessinée ({erreurs} points non calculables)"
            )
        else:
            self.label_info_bas.configure(text=f"✓ Fonction f(x) = {fonction_str} dessinée")
    
    # =========================================================================
    # MÉTHODES DE CONVERSION COORDONNÉES
    # =========================================================================
    
    def _math_vers_pixel_x(self, x_math:  float) -> float:
        """
        Convertit une coordonnée mathématique X en coordonnée pixel.
        
        Args:
            x_math: Coordonnée X mathématique
        
        Returns:
            float: Coordonnée X en pixels sur le canvas
        """
        # Proportion de x dans l'intervalle [x_min, x_max]
        proportion = (x_math - self.x_min) / (self.x_max - self.x_min)
        # Convertir en pixels
        return proportion * self.largeur_canvas
    
    def _math_vers_pixel_y(self, y_math: float) -> float:
        """
        Convertit une coordonnée mathématique Y en coordonnée pixel.
        
        ATTENTION :  Les Y sont inversés (0 en haut du canvas, hauteur en bas)
        
        Args: 
            y_math: Coordonnée Y mathématique
        
        Returns:
            float:  Coordonnée Y en pixels sur le canvas
        """
        # Proportion de y dans l'intervalle [y_min, y_max]
        proportion = (y_math - self.y_min) / (self.y_max - self.y_min)
        # Convertir en pixels (inverser car Y=0 est en haut)
        return self.hauteur_canvas - (proportion * self.hauteur_canvas)
    
    # =========================================================================
    # MÉTHODES DE ZOOM ET NAVIGATION
    # =========================================================================
    
    def zoom_plus(self):
        """
        Zoom avant (réduire l'intervalle de 50%).
        """
        # Calculer le centre actuel
        centre_x = (self.x_min + self.x_max) / 2
        centre_y = (self.y_min + self.y_max) / 2
        
        # Réduire l'intervalle de moitié
        largeur_x = (self.x_max - self.x_min) / 2
        hauteur_y = (self.y_max - self.y_min) / 2
        
        self.x_min = centre_x - largeur_x / 2
        self.x_max = centre_x + largeur_x / 2
        self.y_min = centre_y - hauteur_y / 2
        self.y_max = centre_y + hauteur_y / 2

        # Redessiner (grille + courbe si une fonction est affichée)
        self._redessiner()
        self.label_info_bas.configure(text="🔍 Zoom avant appliqué")
    
    def zoom_moins(self):
        """
        Zoom arrière (augmenter l'intervalle de 100%).
        """
        # Calculer le centre actuel
        centre_x = (self.x_min + self.x_max) / 2
        centre_y = (self.y_min + self.y_max) / 2
        
        # Doubler l'intervalle
        largeur_x = (self.x_max - self.x_min)
        hauteur_y = (self.y_max - self.y_min)
        
        self.x_min = centre_x - largeur_x
        self.x_max = centre_x + largeur_x
        self.y_min = centre_y - hauteur_y
        self.y_max = centre_y + hauteur_y

        # Redessiner (grille + courbe si une fonction est affichée)
        self._redessiner()
        self.label_info_bas.configure(text="🔍 Zoom arrière appliqué")

    def reinitialiser_zoom(self):
        """
        Réinitialise le zoom aux valeurs par défaut (-10 à 10).
        """
        self.x_min = -10.0
        self.x_max = 10.0
        self.y_min = -10.0
        self.y_max = 10.0

        self._redessiner()
        self.label_info_bas.configure(text="🔄 Zoom réinitialisé")

    def effacer_canvas(self):
        """
        Efface tout le canvas et redessine juste la grille.
        """
        # Oublier la fonction : elle ne doit pas réapparaître au prochain zoom.
        self.fonction_courante = None
        self.dessiner_grille()
        self.label_info_bas.configure(text="🗑️ Canvas effacé")

    def _redessiner(self):
        """
        Redessine la grille, puis la courbe de la fonction affichée si elle
        existe (utilisé après un changement de zoom).
        """
        if self.fonction_courante:
            self._tracer(self.fonction_courante, silencieux=True)
        else:
            self.dessiner_grille()