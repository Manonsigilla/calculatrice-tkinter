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
    # Enlever tous les espaces
    expression = expression.replace(" ", "").replace(",", ".")
    
    tokens = []
    nombre_courant = ""
    for char in expression:
        if char.isdigit() or char == '.':
            # c'est une chiffre ou un point donc on construit le nombre
            nombre_courant += char
        else:
            # c'est un opérateur ou une parenthèse
            if nombre_courant:
                tokens.append(nombre_courant) # ajouter le nombre construit
                nombre_courant = "" # réinitialiser pour le prochain nombre
            tokens.append(char) # ajouter l'opérateur ou la parenthèse
    if nombre_courant:
        tokens.append(nombre_courant) # ajouter le dernier nombre s'il existe
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
        '^': 3  
    }
    
    output = [] # Liste de sortie (RPN, résultat final)
    stack = [] # Pile pour les opérateurs et parenthèses
    
    for token in tokens:
        if est_nombre(token):
            output.append(token) # Ajouter les nombres si c'est des nombres directement dans output
        
        elif token == '(':
            stack.append(token) # Empiler les parenthèses ouvrantes
            
        elif token == ')':
            # Dépiler jusqu'à la parenthèse ouvrante
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop() # Retirer la parenthèse ouvrante de la pile
                
        elif token in precedence:
            # Dépiler les opérateurs de la pile selon la priorité
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token) # Empiler l'opérateur courant
    
    # Vider la pile restante
    while stack:
        output.append(stack.pop())
        
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
    from src.exceptions import DivisionParZeroError
    
    stack = []
    
    for token in rpn:
        if est_nombre(token):
            stack.append(float(token))
        else:
            # Si c'est un opérateur -> dépiler deux nombres, calculer, et empiler le résultat
            if len(stack) < 2:
                raise ExpressionInvalideError("Expression RPN invalide")
            
            # Dépiler les deux derniers nombres
            b = stack.pop() # Deuxième opérande
            a = stack.pop() # Premier opérande
            
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
            elif token == '^':
                resultat = a ** b
            else:
                raise ExpressionInvalideError(f"Opérateur inconnu '{token}'")
            
            stack.append(resultat)
    if len(stack) != 1:
        raise ExpressionInvalideError("Expression RPN invalide")
    
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