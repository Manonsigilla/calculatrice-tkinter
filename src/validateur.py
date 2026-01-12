# src/validateur.py
"""
Module de validation des expressions mathématiques. 
Vérifie que l'expression est valide avant de la calculer.
"""

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
    
    def valider_expression(self, expression:  str) -> tuple[bool, str]:
        """
        Valide une expression complète.
        
        Args:
            expression: L'expression mathématique à valider
        
        Returns:
            tuple:  (True, "") si l'expression est valide
            (False, "message d'erreur") sinon
        
        Example:
            >>> validateur = Validateur()
            >>> validateur.valider_expression("2 + 3")
            (True, "")
            >>> validateur.valider_expression("2 + a")
            (False, "Erreur : Caractère 'a' non reconnu à la position 4")
        """
        try:
            # Test 1 : Expression vide
            if not expression or expression.strip() == "":
                raise ExpressionVideError()
            
            # Test 2 :  Caractères invalides
            self._valider_caracteres(expression)
            
            # Test 3 :  Parenthèses équilibrées
            self._valider_parentheses(expression)
            
            # Test 4 : Opérateurs bien placés
            self._valider_operateurs(expression)
            
            # Test 5 :  Nombres bien formés
            self._valider_nombres(expression)
            
            return (True, "")
        
        except Exception as e:
            return (False, str(e))
    
    def _valider_caracteres(self, expression: str):
        """
        Vérifie qu'aucun caractère interdit n'est présent. 
        
        Raises:
            CaractereInvalideError: Si un caractère non autorisé est trouvé
        """
        for i, char in enumerate(expression):
            if char not in self.caracteres_autorises:
                raise CaractereInvalideError(char, i)
    
    def _valider_parentheses(self, expression: str):
        """
        Vérifie que les parenthèses sont équilibrées.
        
        Raises:
            ParenthesesError:  Si les parenthèses ne sont pas équilibrées
        """
        # TODO: À compléter par Personne 2
        # Compter les ( et les )
        # Vérifier qu'on ne ferme jamais avant d'ouvrir
        pass
    
    def _valider_operateurs(self, expression: str):
        """
        Vérifie que les opérateurs ne sont pas consécutifs ou mal placés.
        
        Raises:
            OperateurError: Si les opérateurs sont mal placés
        """
        # TODO: À compléter par Personne 2
        # Vérifier pas de ++ ou +* etc.
        # Vérifier pas d'opérateur en fin
        pass
    
    def _valider_nombres(self, expression: str):
        """
        Vérifie que les nombres sont bien formés (pas de 5.3.2).
        
        Raises:
            NombreInvalideError: Si un nombre est mal formé
        """
        # TODO: À compléter par Personne 2
        # Vérifier pas de nombres avec plusieurs points
        pass