# src/validateur.py
"""
================================================================================
Module de validation des expressions mathématiques - VERSION 3.0
================================================================================

Ce module vérifie qu'une expression est valide AVANT de la calculer. 
Cela permet d'afficher des messages d'erreur précis et explicites. 

VALIDATIONS EFFECTUÉES :
------------------------
    1. Expression non vide
    2. Caractères autorisés uniquement
    3. Parenthèses équilibrées
    4. Opérateurs bien placés
    5. Nombres bien formés
    6. Fonctions avec syntaxe correcte

VERSION 2.0 - NOUVEAUTÉS :
--------------------------
    - Support de l'opérateur modulo (%)
    - Support des fonctions :  sqrt, abs, sin, cos, tan, min, max
    - Validation des arguments des fonctions
    
VERSION 3.0 - NOUVEAUTÉS :
--------------------------
    - Support de toutes les nouvelles fonctions (ln, log, exp, etc.)
    - Support de l'opérateur puissance ^
    - Support des constantes PI, E, ANS
    - Validation des noms de fonctions trigonométriques en degrés

================================================================================
"""

import re
from typing import Tuple
from src.exceptions import (
    CaractereInvalideError,
    ParenthesesError,
    OperateurError,
    ExpressionVideError,
    NombreInvalideError
)


class Validateur:
    """
    Valide les expressions mathématiques avant calcul.
    
    Cette classe effectue une validation syntaxique complète
    pour détecter les erreurs avant le calcul et fournir
    des messages d'erreur explicites à l'utilisateur.
    
    Attributes:
        caracteres_autorises:  Tous les caractères autorisés dans une expression
        operateurs:  Les opérateurs arithmétiques reconnus
        chiffres: Les chiffres de 0 à 9
        fonctions: Les noms de fonctions mathématiques reconnues
    
    Example:
        >>> validateur = Validateur()
        >>> valide, msg = validateur.valider_expression("2 + 3")
        >>> print(valide)
        True
        >>> valide, msg = validateur.valider_expression("2 / 0")
        >>> # Note : la division par zéro n'est pas détectée ici
        >>> # Elle sera gérée lors du calcul
    """
    
    def __init__(self):
        """
        Initialise le validateur avec les caractères et symboles autorisés.
        
        Version 2.0 :  ajout de % et des lettres pour les fonctions
        """
        # =====================================================================
        # CARACTÈRES AUTORISÉS
        # =====================================================================
        # Chiffres, opérateurs, parenthèses, point, virgule, espace
        # + lettres minuscules pour les noms de fonctions (sqrt, sin, etc.)
        # Accent circonflexe pour la puissance ^
        self.caracteres_autorises = "0123456789+-*/%^()., abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # =====================================================================
        # OPÉRATEURS RECONNUS
        # =====================================================================
        # Version 2.0 : ajout du modulo %
        # Version 3.0 : ajout de la puissance ^
        
        self.operateurs = "+-*/%^"
        #=====================================================================
        # CHIFFRES
        #=====================================================================
        self.chiffres = "0123456789"
        
        # =====================================================================
        # CONSTANTES RECONNUES (VERSION 3.0)
        # =====================================================================
        self.constantes = {'pi', 'e', 'ans'}
        
        #=====================================================================
        # FONCTIONS MATHÉMATIQUES RECONNUES
        #=====================================================================
        # Version 3.0 : nouvelles fonctions
        self.fonctions = {
            # Fonctions de base
            'sqrt', 'abs',
            # Trigonométrie radians
            'sin', 'cos', 'tan',
            # Trigonométrie degrés
            'sind', 'cosd', 'tand',
            # Logarithmes
            'ln', 'log',
            # Exponentielle
            'exp',
            # Autres
            'inv', 'sqr',
            # Min/Max
            'min', 'max'
        }
    
    def valider_expression(self, expression: str) -> Tuple[bool, str]: 
        """
        Valide une expression mathématique complète.
        
        Effectue une série de tests dans l'ordre :
            1. Vérifie que l'expression n'est pas vide
            2. Vérifie que tous les caractères sont autorisés
            3. Vérifie que les parenthèses sont équilibrées
            4. Vérifie que les opérateurs sont bien placés
            5. Vérifie que les nombres sont bien formés
            6. Vérifie que les fonctions ont une syntaxe correcte
        
        Args:
            expression: L'expression mathématique à valider
        
        Returns:
            tuple: (True, "") si l'expression est valide
                (False, "message d'erreur") sinon
        
        Examples:
            >>> validateur = Validateur()
            >>> validateur.valider_expression("2 + 3")
            (True, "")
            >>> validateur.valider_expression("")
            (False, "Erreur :  Aucune expression saisie")
            >>> validateur.valider_expression("2 + a")  # 'a' seul n'est pas une fonction
            (False, "Erreur : Caractère 'a' non reconnu à la position 4")
            >>> validateur.valider_expression("ln(E)")
            (True, "")
            >>> validateur.valider_expression("2^10")
            (True, "")
        """
        try:
            # =================================================================
            # TEST 1 : Expression vide
            # =================================================================
            if not expression or expression.strip() == "":
                raise ExpressionVideError()
            
            # =================================================================
            # NORMALISATION
            # =================================================================
            # Remplacer les virgules par des points pour les décimaux
            expression_norm = expression.replace(',', '.')
            
            # =================================================================
            # TEST 2 : Caractères invalides
            # =================================================================
            self._valider_caracteres(expression_norm)
            
            # =================================================================
            # TEST 3 : Parenthèses équilibrées
            # =================================================================
            self._valider_parentheses(expression_norm)
            
            # =================================================================
            # TEST 4 :  Opérateurs bien placés
            # =================================================================
            self._valider_operateurs(expression_norm)
            
            # =================================================================
            # TEST 5 : Nombres bien formés
            # =================================================================
            self._valider_nombres(expression_norm)
            
            # =================================================================
            # TEST 6 : Fonctions avec syntaxe correcte
            # =================================================================
            self._valider_fonctions(expression_norm)
            
            # Tout est valide ! 
            return (True, "")
        
        except Exception as e:
            # Une erreur a été détectée, on retourne le message
            return (False, str(e))
    
    def _valider_caracteres(self, expression: str) -> None:
        """
        Vérifie qu'aucun caractère interdit n'est présent. 
        
        Parcourt chaque caractère de l'expression et vérifie
        qu'il fait partie de la liste des caractères autorisés.
        
        Args:
            expression: L'expression à valider
        
        Raises: 
            CaractereInvalideError: Si un caractère non autorisé est trouvé
        """
        for i, char in enumerate(expression):
            if char not in self.caracteres_autorises:
                raise CaractereInvalideError(char, i)
    
    def _valider_parentheses(self, expression: str) -> None:
        """
        Vérifie que les parenthèses sont équilibrées.
        
        Utilise une pile pour suivre les parenthèses ouvrantes. 
        Chaque parenthèse fermante doit correspondre à une ouvrante.
        
        Cas d'erreur détectés :
            - ')' sans '(' correspondante
            - '(' sans ')' correspondante
            - Parenthèses vides "()"
        
        Args: 
            expression: L'expression à valider
        
        Raises: 
            ParenthesesError:  Si les parenthèses ne sont pas équilibrées
        """
        pile = []  # Pile pour stocker les positions des '('
        
        for i, char in enumerate(expression):
            if char == '(':
                # Empiler la position de cette parenthèse ouvrante
                pile.append(i)
                
            elif char == ')':
                # Vérifier qu'il y a une ouvrante correspondante
                if not pile:
                    raise ParenthesesError(
                        f"Parenthèse fermante ')' sans ouvrante à la position {i}"
                    )
                
                position_ouvrante = pile.pop()
                
                # Vérifier que les parenthèses ne sont pas vides
                # On extrait le contenu entre ( et ) et on vérifie qu'il n'est pas vide
                contenu = expression[position_ouvrante + 1:i].strip()
                if not contenu:
                    raise ParenthesesError(
                        f"Parenthèses vides '()' à la position {position_ouvrante}"
                    )
        
        # Vérifier qu'il ne reste pas de '(' non fermées
        if pile:
            nombre_manquantes = len(pile)
            if nombre_manquantes == 1:
                raise ParenthesesError("1 parenthèse fermante ')' manquante")
            else:
                raise ParenthesesError(
                    f"{nombre_manquantes} parenthèses fermantes ')' manquantes"
                )
    
    def _valider_operateurs(self, expression:  str) -> None:
        """
        Vérifie que les opérateurs sont correctement placés.
        
        Cas d'erreur détectés : 
            - Opérateurs consécutifs invalides (ex: "5 * / 3")
            - Opérateur en fin d'expression (ex: "5 + ")
            - Opérateur invalide après '(' (sauf +/- unaire)
            - Opérateur avant ')' (ex: "5 + )")
            - *, / ou % en début d'expression
        
        Note : +/- sont autorisés après '(' ou un opérateur (nombres unaires)
        
        Args:
            expression: L'expression à valider
        
        Raises:
            OperateurError: Si les opérateurs sont mal placés
        """
        # Enlever les espaces pour simplifier l'analyse
        expr_clean = expression.replace(" ", "")
        
        if not expr_clean:
            return
        
        # =====================================================================
        # Vérifier qu'il n'y a pas d'opérateur en fin d'expression
        # =====================================================================
        if expr_clean[-1] in self.operateurs:
            raise OperateurError("Expression incomplète, opérateur en fin")
        
        # =====================================================================
        # Parcourir l'expression pour détecter les problèmes
        # =====================================================================
        i = 0
        while i < len(expr_clean) - 1:
            char_actuel = expr_clean[i]
            char_suivant = expr_clean[i + 1]
            
            # -----------------------------------------------------------------
            # Cas 1 : Deux opérateurs consécutifs
            # -----------------------------------------------------------------
            if char_actuel in self.operateurs and char_suivant in self.operateurs:
                # Seuls + et - peuvent être unaires (après un autre opérateur)
                if char_suivant in "+-":
                    # Autorisé après un opérateur ou '('
                    if i == 0 or char_actuel in "+-*/%^(":
                        i += 1
                        continue
                
                # Sinon, c'est une erreur
                raise OperateurError(
                    f"Opérateur '{char_suivant}' inattendu après '{char_actuel}' "
                    f"à la position {i + 1}"
                )
            
            # -----------------------------------------------------------------
            # Cas 2 : Opérateur juste après '(' (sauf +/- unaire)
            # -----------------------------------------------------------------
            if char_actuel == '(' and char_suivant in self.operateurs:
                if char_suivant not in "+-": 
                    raise OperateurError(
                        f"Opérateur '{char_suivant}' invalide après '(' "
                        f"à la position {i + 1}"
                    )
            
            # -----------------------------------------------------------------
            # Cas 3 :  Opérateur juste avant ')'
            # -----------------------------------------------------------------
            if char_actuel in self.operateurs and char_suivant == ')':
                raise OperateurError(
                    f"Opérateur '{char_actuel}' invalide avant ')' "
                    f"à la position {i}"
                )
            
            i += 1
        
        # =====================================================================
        # Vérifier qu'il n'y a pas de *, /, % ou ^ au début (+ et - sont OK)
        # =====================================================================
        # On ignore les lettres au début (fonctions comme sqrt, sin, etc.)
        premier_non_lettre = 0
        while premier_non_lettre < len(expr_clean) and expr_clean[premier_non_lettre].isalpha():
            premier_non_lettre += 1
        
        if premier_non_lettre < len(expr_clean) and expr_clean[premier_non_lettre] in "*/%^":
            raise OperateurError(
                f"Opérateur '{expr_clean[premier_non_lettre]}' invalide en début d'expression"
            )
    
    def _valider_nombres(self, expression: str) -> None:
        """
        Vérifie que les nombres sont bien formés.
        
        Un nombre valide peut être :
            - Un entier :  "123"
            - Un décimal : "123.45"
            - Un décimal sans partie entière : ".45"
            - Un décimal sans partie décimale : "123."
        
        Un nombre invalide serait par exemple "5.3.2" (deux points).
        
        Args:
            expression: L'expression à valider
        
        Raises: 
            NombreInvalideError: Si un nombre est mal formé
        """
        # Enlever les espaces
        expr_clean = expression.replace(" ", "")
        
        # Séparer par opérateurs, parenthèses et virgules pour isoler les nombres
        # Le regex capture les séparateurs pour ne pas les perdre
        tokens = re.split(r'([+\-*/%^(),])', expr_clean)
        
        for token in tokens:
            # Ignorer les tokens vides, opérateurs, parenthèses, virgules
            if not token or token in '+-*/%^(),':
                continue
            
            # Ignorer les fonctions et constantes
            if token. lower() in self.fonctions or token.lower() in self.constantes:
                continue
            
            # Ignorer les noms de fonctions (mots alphabétiques)
            if token.isalpha():
                continue
            
            # Si le token contient des lettres mélangées à des chiffres,
            # ce n'est pas un nombre pur, on l'ignore (sera traité ailleurs)
            if any(c.isalpha() for c in token):
                continue
            
            # C'est potentiellement un nombre, vérifier le format
            # Compter le nombre de points décimaux
            if token.count('.') > 1:
                raise NombreInvalideError(token)
            
            # Vérifier que c'est un nombre valide
            # Formats acceptés : "123", "123.45", ".45", "123."
            patron = r'^\d+(\.\d*)?$|^\.\d+$'
            if not re.match(patron, token):
                # Si ça ne correspond pas à un nombre valide
                raise NombreInvalideError(token)
    
    def _valider_fonctions(self, expression: str) -> None:
        """
        Vérifie que les noms de fonctions sont suivis de parenthèses.
        
        Les fonctions reconnues sont : sqrt, abs, sin, cos, tan, min, max
        Chaque fonction doit être suivie immédiatement de '('. 
        
        Exemples valides :  sqrt(16), sin(3.14), min(5, 3)
        Exemples invalides :  sqrt 16, sin 3.14, sqrt
        
        Args:
            expression: L'expression à valider
        
        Raises:
            OperateurError: Si une fonction n'est pas suivie de '('
        """
        # Enlever les espaces pour simplifier
        expr_clean = expression.replace(" ", "").lower()
        
        # Chercher chaque fonction dans l'expression
        for fonction in self.fonctions:
            pos = 0
            while True:
                # Trouver la prochaine occurrence de la fonction
                pos = expr_clean.find(fonction, pos)
                if pos == -1:
                    break
                
                # Vérifier que ce n'est pas une sous-chaîne d'un mot plus long
                # (ex: "cosinus" contient "cos" mais n'est pas notre fonction)
                avant_ok = (pos == 0 or not expr_clean[pos - 1].isalpha())
                apres_pos = pos + len(fonction)
                
                if avant_ok and apres_pos < len(expr_clean):
                    char_apres = expr_clean[apres_pos]
                    
                    # Le caractère après doit être '('
                    if char_apres != '(':
                        if char_apres.isalpha():
                            # C'est peut-être un nom plus long, on continue
                            pos += 1
                            continue
                        # Sinon, c'est une erreur
                        raise OperateurError(
                            f"La fonction {fonction}() doit être suivie de parenthèses"
                        )
                
                pos += 1