# src/exceptions.py
"""
================================================================================
Module des exceptions personnalisées pour la calculatrice.
================================================================================
Définit tous les types d'erreurs que l'application peut rencontrer. 
Chaque exception hérite de CalculatriceError pour une gestion unifiée. 

Version 2.0 - Ajout des exceptions pour les nouvelles fonctionnalités : 
    - RacineNegativeError :  pour sqrt de nombres négatifs
    - ArgumentFonctionError : pour les arguments invalides des fonctions
    - TangenteDomainError : pour tan(90°) et valeurs similaires
    - ModuloParZeroError : pour les divisions modulo par zéro
================================================================================
"""


class CalculatriceError(Exception):
    """
    Classe de base pour toutes les erreurs de la calculatrice.
    
    Toutes les exceptions personnalisées héritent de cette classe,
    ce qui permet de les attraper toutes avec un seul except.
    
    Exemple: 
        try:
            resultat = calculer(expression)
        except CalculatriceError as e:
            print(f"Erreur de calcul : {e}")
    """
    pass


class DivisionParZeroError(CalculatriceError):
    """
    Levée quand une division par zéro est tentée.
    
    Cette erreur est fatale et empêche le calcul de continuer.
    Le message est clair pour l'utilisateur.
    """
    def __init__(self):
        super().__init__("Erreur :  Division par zéro impossible")


class ModuloParZeroError(CalculatriceError):
    """
    Levée quand un modulo par zéro est tenté (ex: 5 % 0).
    
    Le modulo par zéro est mathématiquement indéfini.
    """
    def __init__(self):
        super().__init__("Erreur : Modulo par zéro impossible")


class CaractereInvalideError(CalculatriceError):
    """
    Levée quand un caractère non autorisé est détecté dans l'expression.
    
    Attributes:
        caractere: Le caractère invalide trouvé
        position: Sa position dans l'expression (index 0-based)
    """
    def __init__(self, caractere, position):
        message = f"Erreur : Caractère '{caractere}' non reconnu à la position {position}"
        super().__init__(message)
        self.caractere = caractere
        self.position = position


class ParenthesesError(CalculatriceError):
    """
    Levée quand les parenthèses sont déséquilibrées ou mal placées.
    
    Cas gérés :
        - Parenthèse fermante sans ouvrante correspondante
        - Parenthèse ouvrante sans fermante correspondante
        - Parenthèses vides ()
    """
    def __init__(self, message):
        super().__init__(f"Erreur : {message}")


class OperateurError(CalculatriceError):
    """
    Levée quand les opérateurs sont mal placés dans l'expression.
    
    Cas gérés :
        - Opérateurs consécutifs invalides (ex: "5 * / 3")
        - Opérateur en fin d'expression (ex: "5 + ")
        - Opérateur invalide après parenthèse ouvrante
    """
    def __init__(self, message):
        super().__init__(f"Erreur : {message}")


class ExpressionVideError(CalculatriceError):
    """
    Levée quand l'expression est vide ou ne contient que des espaces.
    """
    def __init__(self):
        super().__init__("Erreur :  Aucune expression saisie")


class NombreInvalideError(CalculatriceError):
    """
    Levée quand un nombre est mal formé.
    
    Exemples de nombres invalides :
        - "5.3.2" (plusieurs points décimaux)
        - ".." (pas de chiffres)
    """
    def __init__(self, nombre):
        super().__init__(f"Erreur : Format de nombre invalide ({nombre})")


class ExpressionInvalideError(CalculatriceError):
    """
    Levée quand l'expression est syntaxiquement incorrecte.
    
    Cette exception est générique pour les erreurs de syntaxe
    qui ne rentrent pas dans les autres catégories.
    """
    def __init__(self, message):
        super().__init__(f"Erreur : {message}")


class RacineNegativeError(CalculatriceError):
    """
    Levée quand on tente de calculer la racine carrée d'un nombre négatif.
    
    La racine carrée d'un nombre négatif n'est pas définie dans les réels.
    On pourrait supporter les nombres complexes dans une version future.
    """
    def __init__(self, nombre):
        super().__init__(f"Erreur :  Racine carrée d'un nombre négatif ({nombre}) impossible")


class ArgumentFonctionError(CalculatriceError):
    """
    Levée quand une fonction reçoit un argument invalide.
    
    Exemples :
        - min() ou max() sans arguments
        - Fonction avec syntaxe incorrecte
    """
    def __init__(self, fonction, message):
        super().__init__(f"Erreur :  Fonction {fonction}() - {message}")


class TangenteDomainError(CalculatriceError):
    """
    Levée quand tan() est appelée sur une valeur où elle n'est pas définie. 
    
    tan(x) n'est pas définie quand cos(x) = 0, c'est-à-dire pour
    x = π/2 + n*π (90°, 270°, etc.)
    """
    def __init__(self, angle):
        super().__init__(f"Erreur :  Tangente non définie pour l'angle {angle} (cos = 0)")