# src/exceptions.py
"""
Exceptions personnalisées pour la calculatrice. 
Définit tous les types d'erreurs que l'application peut rencontrer. 
"""


class CalculatriceError(Exception):
    """Classe de base pour toutes les erreurs de la calculatrice"""
    pass


class DivisionParZeroError(CalculatriceError):
    """Levée quand une division par zéro est tentée"""
    def __init__(self):
        super().__init__("Erreur : Division par zéro impossible")


class CaractereInvalideError(CalculatriceError):
    """Levée quand un caractère non autorisé est détecté"""
    def __init__(self, caractere, position):
        message = f"Erreur : Caractère '{caractere}' non reconnu à la position {position}"
        super().__init__(message)
        self.caractere = caractere
        self.position = position


class ParenthesesError(CalculatriceError):
    """Levée quand les parenthèses sont déséquilibrées"""
    def __init__(self, message):
        super().__init__(f"Erreur : {message}")


class OperateurError(CalculatriceError):
    """Levée quand les opérateurs sont mal placés"""
    def __init__(self, message):
        super().__init__(f"Erreur : {message}")


class ExpressionVideError(CalculatriceError):
    """Levée quand l'expression est vide"""
    def __init__(self):
        super().__init__("Erreur : Aucune expression saisie")


class NombreInvalideError(CalculatriceError):
    """Levée quand un nombre est mal formé (ex: 5.3.2)"""
    def __init__(self, nombre):
        super().__init__(f"Erreur : Format de nombre invalide ({nombre})")


class ExpressionInvalideError(CalculatriceError):
    """Levée quand l'expression est syntaxiquement incorrecte"""
    def __init__(self, message):
        super().__init__(f"Erreur : {message}")