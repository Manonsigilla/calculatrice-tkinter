# src/calculateur.py
"""
================================================================================
Module de calcul des expressions mathématiques - VERSION 2.0 (CORRIGÉ)
================================================================================

CORRECTIONS : 
- min(a,b) et max(a,b) fonctionnent maintenant correctement
- Les nombres négatifs sont correctement gérés :  (-6+2) = -4
- La virgule est bien interprétée comme séparateur d'arguments

================================================================================
"""

from src.exceptions import (
    DivisionParZeroError, 
    ExpressionInvalideError,
    RacineNegativeError,
    ArgumentFonctionError,
    TangenteDomainError,
    ModuloParZeroError
)


# =============================================================================
# CONSTANTES
# =============================================================================
PI = 3.141592653589793


# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def calculer(expression:  str) -> float:
    """
    Calcule le résultat d'une expression mathématique.
    
    Args:
        expression: Expression mathématique (ex: "3 + 5 * 2", "min(3,7)")
    
    Returns:
        float:  Le résultat du calcul
    """
    # ÉTAPE 1 : Tokenization
    tokens = tokenize(expression)
    
    # ÉTAPE 2 :  Conversion en notation polonaise inversée (RPN)
    rpn = infix_to_rpn(tokens)
    
    # ÉTAPE 3 : Évaluation
    resultat = evaluer_rpn(rpn)
    
    return resultat


# =============================================================================
# TOKENIZATION - CORRIGÉE
# =============================================================================

def tokenize(expression: str) -> list:
    """
    Découpe l'expression en tokens. 
    
    CORRECTIONS V2.0 :
    - La virgule est maintenant un token séparateur pour min/max
    - Le signe moins est correctement identifié comme unaire ou binaire
    
    Args:
        expression: Expression à découper
    
    Returns: 
        list: Liste de tokens
    """
    # Nettoyage :  enlever espaces
    expression = expression.replace(" ", "")
    # NE PAS remplacer la virgule par un point !  La virgule sert de séparateur
    # pour les fonctions comme min(a,b) et max(a,b)
    
    tokens = []
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        # =====================================================================
        # CAS 1 :  CHIFFRE OU POINT -> NOMBRE
        # =====================================================================
        if char.isdigit() or char == '.':
            nombre = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                nombre += expression[i]
                i += 1
            tokens.append(nombre)
            continue
        
        # =====================================================================
        # CAS 2 : LETTRE -> NOM DE FONCTION
        # =====================================================================
        elif char.isalpha():
            fonction = ""
            while i < len(expression) and expression[i].isalpha():
                fonction += expression[i]
                i += 1
            tokens.append(fonction.lower())
            continue
        
        # =====================================================================
        # CAS 3 : SIGNE MOINS -> UNAIRE OU SOUSTRACTION ? 
        # =====================================================================
        elif char == '-':
            # Le moins est UNAIRE si : 
            # - C'est le premier token
            # - Le token précédent est un opérateur (+, -, *, /, %)
            # - Le token précédent est une parenthèse ouvrante (
            # - Le token précédent est une virgule ,
            
            est_unaire = (
                len(tokens) == 0 or
                tokens[-1] in ['+', '-', '*', '/', '%', '(', ',']
            )
            
            if est_unaire:
                # C'est un moins unaire -> on l'ajoute comme token spécial
                tokens.append('UNARY_MINUS')
            else:
                # C'est une soustraction
                tokens.append('-')
            i += 1
        
        # =====================================================================
        # CAS 4 :  SIGNE PLUS UNAIRE (ignoré)
        # =====================================================================
        elif char == '+': 
            est_unaire = (
                len(tokens) == 0 or
                tokens[-1] in ['+', '-', '*', '/', '%', '(', ',']
            )
            
            if not est_unaire:
                # C'est une addition
                tokens.append('+')
            # Si c'est unaire (+5), on l'ignore car +5 = 5
            i += 1
        
        # =====================================================================
        # CAS 5 : VIRGULE -> SÉPARATEUR D'ARGUMENTS (pour min, max)
        # =====================================================================
        elif char == ',':
            tokens.append(',')
            i += 1
        
        # =====================================================================
        # CAS 6 : AUTRES OPÉRATEURS ET PARENTHÈSES
        # =====================================================================
        elif char in '*/()%':
            tokens.append(char)
            i += 1
        
        # =====================================================================
        # CAS 7 : CARACTÈRE INCONNU
        # =====================================================================
        else:
            tokens.append(char)
            i += 1
    
    return tokens


# =============================================================================
# ALGORITHME SHUNTING YARD - CORRIGÉ
# =============================================================================

def infix_to_rpn(tokens: list) -> list:
    """
    Convertit une expression infixe en notation polonaise inversée (RPN).
    
    CORRECTIONS V2.0 : 
    - Gestion correcte de la virgule comme séparateur
    - UNARY_MINUS a la plus haute priorité
    
    Args:
        tokens: Liste de tokens en notation infixe
    
    Returns:
        list: Liste de tokens en notation RPN
    """
    # Priorités des opérateurs
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/':  2,
        '%': 2,
        '^': 3,
        'UNARY_MINUS': 4  # Priorité la plus haute pour le moins unaire
    }
    
    # Liste des fonctions reconnues
    fonctions = {'sqrt', 'abs', 'sin', 'cos', 'tan', 'min', 'max'}
    
    output = []
    stack = []
    
    for token in tokens:
        # =====================================================================
        # NOMBRE -> directement dans output
        # =====================================================================
        if est_nombre(token):
            output.append(token)
        
        # =====================================================================
        # FONCTION -> sur la pile
        # =====================================================================
        elif token in fonctions:
            stack.append(token)
        
        # =====================================================================
        # MOINS UNAIRE -> sur la pile (haute priorité)
        # =====================================================================
        elif token == 'UNARY_MINUS': 
            stack.append(token)
        
        # =====================================================================
        # VIRGULE -> dépiler jusqu'à la parenthèse ouvrante
        # =====================================================================
        elif token == ',': 
            while stack and stack[-1] != '(':
                output.append(stack.pop())
        
        # =====================================================================
        # PARENTHÈSE OUVRANTE -> sur la pile
        # =====================================================================
        elif token == '(': 
            stack.append(token)
        
        # =====================================================================
        # PARENTHÈSE FERMANTE -> dépiler jusqu'à l'ouvrante
        # =====================================================================
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            
            # Retirer la parenthèse ouvrante
            if stack: 
                stack.pop()
            
            # Si une fonction précède, la dépiler
            if stack and stack[-1] in fonctions: 
                output.append(stack.pop())
        
        # =====================================================================
        # OPÉRATEUR -> gérer les priorités
        # =====================================================================
        elif token in precedence: 
            while (stack and stack[-1] != '(' and stack[-1] in precedence and precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
    
    # Vider la pile
    while stack: 
        output.append(stack.pop())
    
    return output


# =============================================================================
# ÉVALUATION RPN - CORRIGÉE
# =============================================================================

def evaluer_rpn(rpn: list) -> float:
    """
    Évalue une expression en notation polonaise inversée (RPN).
    
    Args:
        rpn: Liste de tokens en notation RPN
    
    Returns:
        float:  Résultat du calcul
    """
    stack = []
    
    operateurs_binaires = {'+', '-', '*', '/', '%', '^'}
    fonctions_unaires = {'sqrt', 'abs', 'sin', 'cos', 'tan', 'UNARY_MINUS'}
    fonctions_binaires = {'min', 'max'}
    
    for token in rpn:
        # =====================================================================
        # NOMBRE -> empiler
        # =====================================================================
        if est_nombre(token):
            stack.append(float(token))
        
        # =====================================================================
        # OPÉRATEUR BINAIRE
        # =====================================================================
        elif token in operateurs_binaires: 
            if len(stack) < 2:
                raise ExpressionInvalideError("Expression incomplète")
            
            b = stack.pop()
            a = stack.pop()
            
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
            elif token == '%': 
                if b == 0:
                    raise ModuloParZeroError()
                resultat = modulo(a, b)
            elif token == '^':
                resultat = puissance(a, b)
            
            stack.append(resultat)
        
        # =====================================================================
        # FONCTION UNAIRE
        # =====================================================================
        elif token in fonctions_unaires:
            if len(stack) < 1:
                raise ExpressionInvalideError(f"Fonction {token}() sans argument")
            
            arg = stack.pop()
            
            if token == 'sqrt': 
                resultat = racine_carree(arg)
            elif token == 'abs': 
                resultat = valeur_absolue(arg)
            elif token == 'sin': 
                resultat = sinus(arg)
            elif token == 'cos':
                resultat = cosinus(arg)
            elif token == 'tan':
                resultat = tangente(arg)
            elif token == 'UNARY_MINUS':
                resultat = -arg
            
            stack.append(resultat)
        
        # =====================================================================
        # FONCTION BINAIRE (min, max)
        # =====================================================================
        elif token in fonctions_binaires:
            if len(stack) < 2:
                raise ArgumentFonctionError(token, "nécessite 2 arguments séparés par une virgule")
            
            b = stack.pop()
            a = stack.pop()
            
            if token == 'min': 
                resultat = minimum(a, b)
            elif token == 'max':
                resultat = maximum(a, b)
            
            stack.append(resultat)
        
        else:
            raise ExpressionInvalideError(f"Token inconnu :  '{token}'")
    
    if len(stack) != 1:
        raise ExpressionInvalideError("Expression invalide")
    
    return stack[0]


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def est_nombre(token: str) -> bool:
    """Vérifie si un token est un nombre."""
    try:
        float(token)
        return True
    except ValueError:
        return False


# =============================================================================
# FONCTIONS MATHÉMATIQUES (sans module math)
# =============================================================================

def racine_carree(x:  float) -> float:
    """Calcule la racine carrée avec la méthode de Newton-Raphson."""
    if x == 0:
        return 0.0
    if x < 0:
        raise RacineNegativeError(x)
    
    estimation = x / 2.0
    precision = 1e-10
    
    while True:
        nouvelle_estimation = (estimation + x / estimation) / 2.0
        if valeur_absolue(nouvelle_estimation - estimation) < precision:
            return nouvelle_estimation
        estimation = nouvelle_estimation


def valeur_absolue(x: float) -> float:
    """Retourne la valeur absolue de x."""
    if x < 0:
        return -x
    return float(x)


def modulo(a: float, b:  float) -> float:
    """Calcule a % b (reste de la division)."""
    quotient = a / b
    if quotient >= 0:
        quotient_floor = int(quotient)
    else:
        quotient_floor = int(quotient) - (1 if quotient != int(quotient) else 0)
    return a - b * quotient_floor


def minimum(a: float, b: float) -> float:
    """Retourne le minimum entre a et b."""
    if a < b:
        return float(a)
    return float(b)


def maximum(a: float, b: float) -> float:
    """Retourne le maximum entre a et b."""
    if a > b:
        return float(a)
    return float(b)


def puissance(base: float, exposant: float) -> float:
    """Calcule base^exposant."""
    if exposant == 0:
        return 1.0
    if base == 0:
        return 0.0
    if exposant == 1:
        return float(base)
    
    if exposant < 0:
        return 1.0 / puissance(base, -exposant)
    
    if exposant == int(exposant):
        resultat = 1.0
        for _ in range(int(exposant)):
            resultat *= base
        return resultat
    
    return base ** exposant


# =============================================================================
# FONCTIONS TRIGONOMÉTRIQUES (séries de Taylor)
# =============================================================================

def sinus(x: float) -> float:
    """Calcule sin(x) avec x en radians."""
    x = _normaliser_angle(x)
    resultat = 0.0
    terme = x
    
    for n in range(25):
        resultat += terme
        terme *= -x * x / ((2 * n + 2) * (2 * n + 3))
    
    return resultat


def cosinus(x: float) -> float:
    """Calcule cos(x) avec x en radians."""
    x = _normaliser_angle(x)
    resultat = 0.0
    terme = 1.0
    
    for n in range(25):
        resultat += terme
        terme *= -x * x / ((2 * n + 1) * (2 * n + 2))
    
    return resultat


def tangente(x: float) -> float:
    """Calcule tan(x) avec x en radians."""
    cos_x = cosinus(x)
    if valeur_absolue(cos_x) < 1e-10:
        raise TangenteDomainError(x)
    return sinus(x) / cos_x


def _normaliser_angle(x: float) -> float:
    """Normalise un angle dans [-π, π]."""
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    return x