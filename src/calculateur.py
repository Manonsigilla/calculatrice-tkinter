# src/calculateur.py
"""
Module de calcul des expressions mathématiques.
Implémente l'algorithme Shunting Yard pour respecter les priorités opératoires.
"""

from src.exceptions import DivisionParZeroError, ExpressionInvalideError


def calculer(expression: str) -> float:
    """
    Calcule le résultat d'une expression mathématique.
    
    Args:
        expression: Expression mathématique (ex: "3 + 5 * 2")
    
    Returns:
        float: Le résultat du calcul
    
    Raises:
        DivisionParZeroError: Si une division par zéro est tentée
        ExpressionInvalideError: Si l'expression ne peut pas être évaluée
    
    Example:
        >>> calculer("2 + 3")
        5.0
        >>> calculer("2 + 3 * 4")
        14.0
        >>> calculer("(2 + 3) * 4")
        20.0
    """
    # ÉTAPE 1 : Tokenization
    tokens = tokenize(expression)
    
    # ÉTAPE 2 :  Conversion en notation polonaise inversée (RPN)
    rpn = infix_to_rpn(tokens)
    
    # ÉTAPE 3 : Évaluation
    resultat = evaluer_rpn(rpn)
    
    return resultat


def tokenize(expression: str) -> list:
    """
    Découpe l'expression en tokens (nombres, opérateurs, parenthèses).
    
    Args:
        expression: Expression à découper (ex: "3 + 5 * 2")
    
    Returns:
        list: Liste de tokens (ex: ['3', '+', '5', '*', '2'])
    
    Example:
        >>> tokenize("3 + 5 * 2")
        ['3', '+', '5', '*', '2']
        >>> tokenize("3. 14 * (2 + 1)")
        ['3.14', '*', '(', '2', '+', '1', ')']
    """
    # TODO: À compléter par Personne 1
    # Parcourir l'expression caractère par caractère
    # Regrouper les chiffres ensemble (ex: "123" → un seul token)
    # Gérer les nombres décimaux (ex: "3.14" → un seul token)
    # Séparer les opérateurs et parenthèses
    
    tokens = []
    # Votre code ici... 
    
    return tokens


def infix_to_rpn(tokens: list) -> list:
    """
    Convertit une expression infixe en notation polonaise inversée (RPN).
    Utilise l'algorithme Shunting Yard de Dijkstra.
    
    Args:
        tokens: Liste de tokens en notation infixe
    
    Returns:
        list: Liste de tokens en notation RPN
    
    Example:
        >>> infix_to_rpn(['3', '+', '5', '*', '2'])
        ['3', '5', '2', '*', '+']
        >>> infix_to_rpn(['(', '2', '+', '3', ')', '*', '4'])
        ['2', '3', '+', '4', '*']
    """
    # Priorités des opérateurs
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/':  2,
        '^': 3  # Optionnel : puissance
    }
    
    # TODO: À compléter par Personne 1
    # Implémenter l'algorithme Shunting Yard
    # Utiliser une pile pour les opérateurs
    # Utiliser une liste pour la sortie
    
    output = []
    stack = []
    
    # Votre code ici...
    
    return output


def evaluer_rpn(rpn: list) -> float:
    """
    Évalue une expression en notation polonaise inversée (RPN).
    
    Args:
        rpn: Liste de tokens en notation RPN
    
    Returns:
        float:  Résultat du calcul
    
    Raises:
        DivisionParZeroError: Si une division par zéro est tentée
    
    Example:
        >>> evaluer_rpn(['3', '5', '2', '*', '+'])
        13.0
        >>> evaluer_rpn(['2', '3', '+', '4', '*'])
        20.0
    """
    # TODO: À compléter par Personne 1
    # Utiliser une pile
    # Pour chaque token : 
    #   - Si c'est un nombre :  empiler
    #   - Si c'est un opérateur : dépiler 2 nombres, calculer, empiler le résultat
    
    stack = []
    
    for token in rpn:
        if est_nombre(token):
            stack.append(float(token))
        else:
            # Dépiler les deux derniers nombres
            b = stack. pop()
            a = stack. pop()
            
            # Appliquer l'opération
            if token == '+':
                resultat = a + b
            elif token == '-':
                resultat = a - b
            elif token == '*':
                resultat = a * b
            elif token == '/':
                if b == 0:
                    raise DivisionParZeroError()
                resultat = a / b
            # Ajouter d'autres opérateurs si besoin
            
            stack.append(resultat)
    
    return stack[0]


def est_nombre(token: str) -> bool:
    """
    Vérifie si un token est un nombre.
    
    Args:
        token: Le token à vérifier
    
    Returns:
        bool: True si c'est un nombre, False sinon
    
    Example:
        >>> est_nombre("3")
        True
        >>> est_nombre("3.14")
        True
        >>> est_nombre("+")
        False
    """
    try:
        float(token)
        return True
    except ValueError: 
        return False