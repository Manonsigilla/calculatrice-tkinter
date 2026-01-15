# src/validateur.py
"""
Module de validation des expressions mathématiques.  
Vérifie que l'expression est valide avant de la calculer.
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
    """Valide les expressions mathématiques avant calcul"""
    
    def __init__(self):
        self.caracteres_autorises = "0123456789+-*/()., "
        self.operateurs = "+-*/"
        self.chiffres = "0123456789"
    
    def valider_expression(self, expression):
        """
        Valide une expression complète.
        
        Args:
            expression:  L'expression mathématique à valider
        
        Returns:
            tuple: (True, "") si l'expression est valide
                (False, "message d'erreur") sinon
        
        Example:
            >>> validateur = Validateur()
            >>> validateur.valider_expression("2 + 3")
            (True, "")
            >>> validateur.valider_expression("2 + a")
            (False, "Erreur :  Caractère 'a' non reconnu à la position 4")
        """
        try:
            # Test 1 : Expression vide
            if not expression or expression.strip() == "":
                raise ExpressionVideError()
            
            # Normaliser :  remplacer virgules par points pour les décimaux
            expression_norm = expression.replace(',', '.')
            
            # Test 2 : Caractères invalides
            self._valider_caracteres(expression_norm)
            
            # Test 3 : Parenthèses équilibrées
            self._valider_parentheses(expression_norm)
            
            # Test 4 : Opérateurs bien placés
            self._valider_operateurs(expression_norm)
            
            # Test 5 : Nombres bien formés
            self._valider_nombres(expression_norm)
            
            return (True, "")
        
        except Exception as e:
            return (False, str(e))
    
    def _valider_caracteres(self, expression):
        """
        Vérifie qu'aucun caractère interdit n'est présent. 
        
        Raises:
            CaractereInvalideError: Si un caractère non autorisé est trouvé
        """
        for i, char in enumerate(expression):
            if char not in self.caracteres_autorises:
                raise CaractereInvalideError(char, i)
    
    def _valider_parentheses(self, expression):
        """
        Vérifie que les parenthèses sont équilibrées. 
        
        Raises: 
            ParenthesesError: Si les parenthèses ne sont pas équilibrées
        """
        pile = []
        
        for i, char in enumerate(expression):
            if char == '(':
                pile.append(i)
            elif char == ')':
                # Parenthèse fermante sans ouvrante
                if not pile:
                    raise ParenthesesError(
                        "Parenthèse fermante ')' sans ouvrante à la position {}".format(i)
                    )
                
                position_ouvrante = pile.pop()
                
                # Vérifier parenthèses vides "()"
                # On enlève les espaces entre les parenthèses pour vérifier
                contenu = expression[position_ouvrante + 1:i]. strip()
                if not contenu:
                    raise ParenthesesError(
                        "Parenthèses vides '()' à la position {}".format(position_ouvrante)
                    )
        
        # Il reste des parenthèses ouvrantes non fermées
        if pile:
            nombre_manquantes = len(pile)
            if nombre_manquantes == 1:
                raise ParenthesesError("1 parenthèse fermante ')' manquante")
            else:
                raise ParenthesesError(
                    "{} parenthèses fermantes ')' manquantes".format(nombre_manquantes)
                )
    
    def _valider_operateurs(self, expression):
        """
        Vérifie que les opérateurs ne sont pas consécutifs ou mal placés.
        
        Raises:
            OperateurError: Si les opérateurs sont mal placés
        """
        # Enlever les espaces pour faciliter la vérification
        expr_clean = expression.replace(" ", "")
        
        if not expr_clean:
            return
        
        # Vérifier opérateur en fin d'expression
        if expr_clean[-1] in self.operateurs:
            raise OperateurError("Expression incomplète, opérateur en fin")
        
        # Parcourir et détecter opérateurs consécutifs invalides
        i = 0
        while i < len(expr_clean) - 1:
            char_actuel = expr_clean[i]
            char_suivant = expr_clean[i + 1]
            
            # Si deux opérateurs se suivent
            if char_actuel in self.operateurs and char_suivant in self.operateurs:
                # Cas autorisés : unaire après opérateur ou parenthèse
                # Exemples valides : "5 * -3", "(-2 + 3)", "(+5)"
                
                # Autoriser +/- comme unaire après un opérateur ou '('
                if char_suivant in "+-": 
                    # Vérifier si c'est au début ou après '(' ou après un opérateur
                    if i == 0 or char_actuel in "+-*/(":
                        i += 1
                        continue
                
                # Sinon, c'est une erreur
                raise OperateurError(
                    "Opérateur '{}' inattendu après '{}' à la position {}".format(
                        char_suivant, char_actuel, i + 1
                    )
                )
            
            # Vérifier opérateur juste après parenthèse ouvrante
            # (sauf +/- unaire qui est autorisé)
            if char_actuel == '(' and char_suivant in self.operateurs:
                if char_suivant not in "+-":
                    raise OperateurError(
                        "Opérateur '{}' invalide après '(' à la position {}".format(
                            char_suivant, i + 1
                        )
                    )
            
            # Vérifier opérateur juste avant parenthèse fermante
            if char_actuel in self.operateurs and char_suivant == ')':
                raise OperateurError(
                    "Opérateur '{}' invalide avant ')' à la position {}".format(
                        char_actuel, i
                    )
                )
            
            i += 1
        
        # Vérifier opérateur au début (sauf +/- unaire)
        if expr_clean[0] in "*/":
            raise OperateurError(
                "Opérateur '{}' invalide en début d'expression".format(expr_clean[0])
            )
    
    def _valider_nombres(self, expression):
        """
        Vérifie que les nombres sont bien formés (pas de 5.3.2).
        
        Raises:
            NombreInvalideError: Si un nombre est mal formé
        """
        # Enlever les espaces
        expr_clean = expression.replace(" ", "")
        
        # Séparer par opérateurs et parenthèses pour isoler les nombres
        # On garde les séparateurs pour ne pas perdre d'information
        tokens = re. split(r'([+\-*/()])', expr_clean)
        
        for token in tokens: 
            # Ignorer les tokens vides, opérateurs et parenthèses
            if not token or token in '+-*/()':
                continue
            
            # C'est potentiellement un nombre, vérifier le format
            # Compter le nombre de points
            if token.count('.') > 1:
                raise NombreInvalideError(token)
            
            # Vérifier que c'est un nombre valide
            # Formats acceptés : "123", "123.45", ".45", "123."
            patron = r'^\d+(\.\d*)?$|^\.\d+$'
            if not re.match(patron, token):
                # Si ça ne correspond pas à un nombre valide, c'est une erreur
                # (normalement déjà attrapé par _valider_caracteres, mais double vérification)
                raise NombreInvalideError(token)