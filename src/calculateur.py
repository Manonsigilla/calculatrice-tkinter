# src/calculateur.py
"""
================================================================================
Module de calcul des expressions mathématiques - VERSION 2.0
================================================================================

VERSION 2.0 - CORRECTIONS ET NOUVELLES FONCTIONNALITÉS : 
- min(a,b) et max(a,b) fonctionnent maintenant correctement
- Les nombres négatifs sont correctement gérés :  (-6+2) = -4
- La virgule est bien interprétée comme séparateur d'arguments

VERSION 3.0 - NOUVELLES FONCTIONNALITÉS :
-----------------------------------------
- Logarithme népérien :  ln(x)
- Logarithme base 10 : log(x)
- Exponentielle : exp(x) ou e^x
- Puissance visible : ^ (2^3 = 8)
- Inverse : inv(x) = 1/x
- Carré : sqr(x) = x²
- Constantes :  PI et E
- Trigonométrie en degrés :  sind(), cosd(), tand()
- Support de ANS (dernier résultat)

================================================================================
"""

from src.exceptions import (
    DivisionParZeroError, 
    ExpressionInvalideError,
    RacineNegativeError,
    ArgumentFonctionError,
    TangenteDomainError,
    ModuloParZeroError,
    LogarithmeError
)


#=============================================================================
# CONSTANTES
#=============================================================================
PI = 3.141592653589793 # Valeur de π
E = 2.718281828459045 # Valeur de e, nombre d'Euler (base des logarithmes népériens)


#=============================================================================
# VARIABLE GLOBALE POUR ANS (dernier résultat)
#=============================================================================
_dernier_resultat = 0.0


def obtenir_dernier_resultat():
    """
    Retourne le dernier résultat calculé (pour ANS).
    
    Returns:
        float: Le dernier résultat
    """
    return _dernier_resultat


def definir_dernier_resultat(valeur):
    """
    Définit le dernier résultat (appelé après chaque calcul).
    
    Args:
        valeur:  Le nouveau résultat à stocker
    """
    global _dernier_resultat
    _dernier_resultat = valeur

#=============================================================================
# FONCTION PRINCIPALE
#=============================================================================

def calculer(expression:  str, utiliser_degres=False) -> float:
    """
    Calcule le résultat d'une expression mathématique.
    
    Args:
        expression: Expression mathématique (ex: "3 + 5 * 2", "min(3,7)")
        utiliser_degres: Si True, les fonctions trigo utilisent des degrés
                        Si False (défaut), elles utilisent des radians
    
    Returns:
        float:  Le résultat du calcul
    
    Examples:
        resultat = calculer("3 + 5 * 2")
        calculer("ln(E)")  # Retourne 1.0
        calculer("2^3 + sqr(4)")  # Retourne 24.0
    """
    # ÉTAPE 1 : Tokenization
    tokens = tokenize(expression)
    
    # ÉTAPE 2 :  Conversion en notation polonaise inversée (RPN)
    rpn = infix_to_rpn(tokens)
    
    # ÉTAPE 3 : Évaluation
    resultat = evaluer_rpn(rpn, utiliser_degres)
    
    # Mettre à jour le dernier résultat pour ANS
    definir_dernier_resultat(resultat)
    
    return resultat


#=============================================================================
# TOKENIZATION
#=============================================================================

def tokenize(expression: str) -> list:
    """
    Découpe l'expression en tokens. 
    
    GÈRE : 
    ------
        - Nombres entiers et décimaux
        - Opérateurs :  +, -, *, /, %, ^
        - Parenthèses : (, )
        - Virgule : , (séparateur d'arguments)
        - Fonctions : sqrt, abs, sin, cos, tan, ln, log, exp, inv, sqr, etc.
        - Constantes :  PI, E, ANS
        - Nombres négatifs (unaires)
    
    Args:
        expression: Expression à tokenizer
    
    Returns:
        list: Liste de tokens
    
    Examples:
        >>> tokenize("2 * PI")
        ['2', '*', 'PI']
        >>> tokenize("ln(E)")
        ['ln', '(', 'E', ')']
    """
    # Nettoyage :  enlever espaces
    expression = expression.replace(" ", "")
    # NE PAS remplacer la virgule par un point !  La virgule sert de séparateur
    # pour les fonctions comme min(a,b) et max(a,b)
    
    tokens = []
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        #=====================================================================
        # CAS 1 :  CHIFFRE OU POINT -> NOMBRE
        #=====================================================================
        if char.isdigit() or char == '.':
            nombre = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                nombre += expression[i]
                i += 1
            tokens.append(nombre)
            continue
        
        #=====================================================================
        # CAS 2 : LETTRE -> NOM DE FONCTION OU CONSTANTE
        #=====================================================================
        elif char.isalpha():
            mot = ""
            while i < len(expression) and expression[i].isalpha():
                mot += expression[i]
                i += 1
            # convertir en minuscules (insensible à la casse)
            mot_lower = mot.lower()
            
            # Vérifier si c'est une constante reconnue
            if mot_lower == 'pi':
                tokens.append('PI') # garder en majuscules pour la constante
            elif mot_lower == 'e' and (i >= len(expression) or not expression[i] != 'x'):
                tokens.append('E') # garder en majuscules pour la constante
            elif mot_lower == 'ans':
                tokens.append('ANS') # garder en majuscules pour la constante
            else:
                # C'est une fonction
                tokens.append(mot_lower)
            continue
        
        #=====================================================================
        # CAS 3 : SIGNE MOINS -> UNAIRE OU SOUSTRACTION ? 
        #=====================================================================
        elif char == '-':
            # Le moins est UNAIRE si : 
            # - C'est le premier token
            # - Le token précédent est un opérateur (+, -, *, /, %)
            # - Le token précédent est une parenthèse ouvrante (
            # - Le token précédent est une virgule ,
            
            est_unaire = (
                len(tokens) == 0 or
                tokens[-1] in ['+', '-', '*', '/', '%', '^', '(', ',']
            )
            
            if est_unaire:
                # C'est un moins unaire -> on l'ajoute comme token spécial
                tokens.append('UNARY_MINUS')
            else:
                # C'est une soustraction
                tokens.append('-')
            i += 1
        
        #=====================================================================
        # CAS 4 :  SIGNE PLUS UNAIRE (ignoré)
        #=====================================================================
        elif char == '+': 
            est_unaire = (
                len(tokens) == 0 or
                tokens[-1] in ['+', '-', '*', '/', '%', '^', '(', ',']
            )
            
            if not est_unaire:
                # C'est une addition
                tokens.append('+')
            # Si c'est unaire (+5), on l'ignore car +5 = 5
            i += 1
        
        #=====================================================================
        # CAS 5 : VIRGULE -> SÉPARATEUR D'ARGUMENTS (pour min, max)
        #=====================================================================
        elif char == ',':
            tokens.append(',')
            i += 1
        
        #=====================================================================
        # CAS 6 : PUISSANCE ^
        #=====================================================================
        elif char == '^':
            tokens.append('^')
            i += 1
            
        #=====================================================================
        # CAS 7 : AUTRES OPÉRATEURS ET PARENTHÈSES
        #=====================================================================
        elif char in '*/()%':
            tokens.append(char)
            i += 1
        
        #=====================================================================
        # CAS 8 : CARACTÈRE INCONNU
        #=====================================================================
        else:
            tokens.append(char)
            i += 1
    
    return tokens


#=============================================================================
# ALGORITHME SHUNTING YARD
#=============================================================================

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
        
    Examples:
        >>> infix_to_rpn(['3', '+', '5', '*', '2'])
        ['3', '5', '2', '*', '+']
        >>> infix_to_rpn(['2', '^', '3'])
        ['2', '3', '^']
    """
    #=========================================================================
    # TABLE DES PRIORITÉS DES OPÉRATEURS
    #=========================================================================
    # Plus le nombre est élevé, plus l'opérateur est prioritaire
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/':  2,
        '%': 2,
        '^': 3,
        'UNARY_MINUS': 4  # Priorité la plus haute pour le moins unaire
    }
    
    #=========================================================================
    # ASSOCIATIVITÉ DES OPÉRATEURS
    #=========================================================================
    # La puissance est associative à droite :  2^3^2 = 2^(3^2) = 2^9 = 512
    # Les autres opérateurs sont associatifs à gauche
    associativite_droite = {'^'}
    
    #=========================================================================
    # LISTE DES FONCTIONS RECONNUES
    #=========================================================================
    fonctions = {
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
    
    output = []
    stack = []
    
    for token in tokens:
        #=====================================================================
        # NOMBRE -> directement dans output
        #=====================================================================
        if est_nombre(token):
            output.append(token)
        
        #=====================================================================
        # CONSTANTE (PI, E, ANS) -> directement dans output
        #=====================================================================
        elif token in ['PI', 'E', 'ANS']: 
            output.append(token)
            
        #=====================================================================
        # FONCTION -> sur la pile
        #=====================================================================
        elif token in fonctions:
            stack.append(token)
        
        #=====================================================================
        # MOINS UNAIRE -> sur la pile (haute priorité)
        #=====================================================================
        elif token == 'UNARY_MINUS': 
            stack.append(token)
        
        #=====================================================================
        # VIRGULE -> dépiler jusqu'à la parenthèse ouvrante
        #=====================================================================
        elif token == ',': 
            while stack and stack[-1] != '(':
                output.append(stack.pop())
        
        #=====================================================================
        # PARENTHÈSE OUVRANTE -> sur la pile
        #=====================================================================
        elif token == '(': 
            stack.append(token)
        
        #=====================================================================
        # PARENTHÈSE FERMANTE -> dépiler jusqu'à l'ouvrante
        #=====================================================================
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            
            # Retirer la parenthèse ouvrante
            if stack: 
                stack.pop()
            
            # Si une fonction précède, la dépiler
            if stack and stack[-1] in fonctions: 
                output.append(stack.pop())
        
        #=====================================================================
        # OPÉRATEUR -> gérer les priorités
        #=====================================================================
        elif token in precedence:
            # Dépiler les opérateurs de la pile selon la priorité
            while stack and stack[-1] != '(' and stack[-1] in precedence: 
                # Pour les opérateurs associatifs à droite (^), on dépile
                # seulement si la priorité en haut de pile est STRICTEMENT > 
                if token in associativite_droite: 
                    if precedence[stack[-1]] > precedence[token]:
                        output.append(stack.pop())
                    else:
                        break
                else:
                    # Pour les autres, on dépile si priorité >=
                    if precedence[stack[-1]] >= precedence[token]:
                        output.append(stack.pop())
                    else:
                        break
                    
            stack.append(token)
    
    # Vider la pile
    while stack: 
        output.append(stack.pop())
    
    return output


#=============================================================================
# ÉVALUATION RPN
#=============================================================================

def evaluer_rpn(rpn: list, utiliser_degres=False) -> float:
    """
    Évalue une expression en notation polonaise inversée (RPN).
    
    Args:
        rpn: Liste de tokens en notation RPN
        utiliser_degres: Si True, les fonctions trigo utilisent des degrés
    
    Returns:
        float:  Résultat du calcul
    
    Raises:
        Diverses exceptions selon les erreurs rencontrées
    """
    stack = []
    
    # Listes des différents types de tokens
    operateurs_binaires = {'+', '-', '*', '/', '%', '^'}
    fonctions_unaires = {'sqrt', 'abs', 'sin', 'cos', 'tan', 'sind', 'cosd', 'tand', 'ln', 'log', 'exp', 'inv', 'sqr', 'UNARY_MINUS'}
    fonctions_binaires = {'min', 'max'}
    
    for token in rpn:
        #=====================================================================
        # NOMBRE -> empiler
        #=====================================================================
        if est_nombre(token):
            stack.append(float(token))
        
        # =====================================================================
        # CONSTANTE PI -> empiler sa valeur
        # =====================================================================
        elif token == 'PI':
            stack.append(PI)
        
        #=====================================================================
        # CONSTANTE E -> empiler sa valeur
        #=====================================================================
        elif token == 'E':
            stack.append(E)
        
        #=====================================================================
        # ANS (dernier résultat) -> empiler sa valeur
        #=====================================================================
        elif token == 'ANS':
            stack.append(obtenir_dernier_resultat())
        
        #=====================================================================
        # OPÉRATEUR BINAIRE
        #=====================================================================
        elif token in operateurs_binaires: 
            if len(stack) < 2:
                raise ExpressionInvalideError("Expression incomplète - opérandes manquants")
            
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
        
        #=====================================================================
        # FONCTION UNAIRE
        #=====================================================================
        elif token in fonctions_unaires:
            if len(stack) < 1:
                raise ExpressionInvalideError(f"Fonction {token}() sans argument")
            
            arg = stack.pop()
            
            # Fonctions de base
            if token == 'sqrt':
                resultat = racine_carree(arg)
            elif token == 'abs':
                resultat = valeur_absolue(arg)
            
            # Trigonométrie radians
            elif token == 'sin':
                resultat = sinus(arg)
            elif token == 'cos':
                resultat = cosinus(arg)
            elif token == 'tan': 
                resultat = tangente(arg)
            
            # Trigonométrie degrés
            elif token == 'sind': 
                resultat = sinus_degres(arg)
            elif token == 'cosd':
                resultat = cosinus_degres(arg)
            elif token == 'tand':
                resultat = tangente_degres(arg)
            
            # Logarithmes
            elif token == 'ln':
                resultat = logarithme_neperien(arg)
            elif token == 'log':
                resultat = logarithme_base10(arg)
            
            # Exponentielle
            elif token == 'exp': 
                resultat = exponentielle(arg)
            
            # Autres
            elif token == 'inv':
                resultat = inverse(arg)
            elif token == 'sqr': 
                resultat = carre(arg)
            
            # Moins unaire
            elif token == 'UNARY_MINUS': 
                resultat = -arg
            
            stack.append(resultat)
        
        #=====================================================================
        # FONCTION BINAIRE (min, max)
        #=====================================================================
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
        raise ExpressionInvalideError("Expression invalide - vérifiez la syntaxe")
    
    return stack[0]


#=============================================================================
# FONCTIONS UTILITAIRES
#=============================================================================

def est_nombre(token: str) -> bool:
    """Vérifie si un token est un nombre."""
    try:
        float(token)
        return True
    except ValueError:
        return False


#=============================================================================
# FONCTIONS MATHÉMATIQUES - BASE
#=============================================================================

def racine_carree(x:  float) -> float:
    """
    Calcule la racine carrée avec la méthode de Newton-Raphson.
    
    Args:
        x: Nombre dont on veut la racine (doit être >= 0)
    
    Returns:
        float: sqrt(x)
    
    Raises:
        RacineNegativeError: Si x < 0
    """
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
    """
    Calcule base^exposant.
    
    Args:
        base: La base
        exposant: L'exposant
    
    Returns:
        float: base^exposant
    """
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
    
    # Pour les exposants non-entiers, utiliser ** de Python
    # (ce n'est pas math.pow, donc autorisé)
    return base ** exposant

def inverse(x: float) -> float:
    """
    Calcule 1/x (l'inverse de x).
    
    Args:
        x:  Nombre à inverser
    
    Returns:
        float: 1/x
    
    Raises:
        DivisionParZeroError: Si x = 0
    """
    if x == 0:
        raise DivisionParZeroError()
    return 1.0 / x


def carre(x:  float) -> float:
    """
    Calcule x² (x au carré).
    
    Args:
        x: Nombre à élever au carré
    
    Returns:
        float: x²
    """
    return x * x

#=============================================================================
# FONCTIONS TRIGONOMÉTRIQUES (radians) -  séries de Taylor
#=============================================================================

def sinus(x: float) -> float:
    """
    Calcule sin(x) avec x en radians.
    Utilise la série de Taylor. 
    
    Args:
        x: Angle en radians
    
    Returns:
        float: sin(x)
    """
    x = _normaliser_angle(x)
    resultat = 0.0
    terme = x
    
    for n in range(25):
        resultat += terme
        terme *= -x * x / ((2 * n + 2) * (2 * n + 3))
    
    return resultat


def cosinus(x: float) -> float:
    """
    Calcule cos(x) avec x en radians.
    Utilise la série de Taylor.
    
    Args:
        x:  Angle en radians
    
    Returns:
        float: cos(x)
    """
    x = _normaliser_angle(x)
    resultat = 0.0
    terme = 1.0
    
    for n in range(25):
        resultat += terme
        terme *= -x * x / ((2 * n + 1) * (2 * n + 2))
    
    return resultat


def tangente(x: float) -> float:
    """
    Calcule tan(x) avec x en radians.
    tan(x) = sin(x) / cos(x)
    
    Args:
        x:  Angle en radians
    
    Returns:
        float: tan(x)
    
    Raises:
        TangenteDomainError: Si cos(x) ≈ 0
    """
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

#=============================================================================
# FONCTIONS TRIGONOMÉTRIQUES (DEGRÉS)
#=============================================================================

def degres_vers_radians(degres: float) -> float:
    """
    Convertit des degrés en radians. 
    
    Args:
        degres: Angle en degrés
    
    Returns:
        float: Angle en radians
    
    Formula:
        radians = degres * π / 180
    """
    return degres * PI / 180.0


def sinus_degres(degres: float) -> float:
    """Calcule sin(x) avec x en degrés."""
    return sinus(degres_vers_radians(degres))


def cosinus_degres(degres: float) -> float:
    """Calcule cos(x) avec x en degrés."""
    return cosinus(degres_vers_radians(degres))


def tangente_degres(degres: float) -> float:
    """Calcule tan(x) avec x en degrés."""
    return tangente(degres_vers_radians(degres))


#=============================================================================
# LOGARITHMES - SÉRIES DE TAYLOR
#=============================================================================

def logarithme_neperien(x: float) -> float:
    """
    Calcule ln(x) (logarithme népérien, base e).
    
    Utilise la série de Taylor pour ln(1+u) avec u = (x-1)/(x+1).
    Cette transformation améliore la convergence.
    
    Args:
        x:  Nombre strictement positif
    
    Returns:
        float: ln(x)
    
    Raises:
        LogarithmeError: Si x <= 0
    
    Formule:
        ln(x) = 2 * [u + u³/3 + u⁵/5 + ...] où u = (x-1)/(x+1)
    """
    if x <= 0:
        raise LogarithmeError(x)
    
    if x == 1:
        return 0.0
    
    # Pour améliorer la convergence, on utilise la transformation : 
    # ln(x) = 2 * artanh((x-1)/(x+1))
    # où artanh(u) = u + u³/3 + u⁵/5 + ... 
    
    u = (x - 1) / (x + 1)
    u_carre = u * u
    
    resultat = 0.0
    terme = u
    
    for n in range(100):  # 100 itérations pour bonne précision
        resultat += terme / (2 * n + 1)
        terme *= u_carre
    
    return 2 * resultat


def logarithme_base10(x: float) -> float:
    """
    Calcule log(x) (logarithme base 10).
    
    Utilise la formule : log₁₀(x) = ln(x) / ln(10)
    
    Args:
        x: Nombre strictement positif
    
    Returns:
        float: log₁₀(x)
    
    Raises:
        LogarithmeError: Si x <= 0
    """
    if x <= 0:
        raise LogarithmeError(x)
    
    # log₁₀(x) = ln(x) / ln(10)
    ln_10 = 2.302585092994046  # Valeur précalculée de ln(10)
    return logarithme_neperien(x) / ln_10


#=============================================================================
# EXPONENTIELLE - SÉRIE DE TAYLOR
#=============================================================================

def exponentielle(x:  float) -> float:
    """
    Calcule e^x (exponentielle de x).
    
    Utilise la série de Taylor :  e^x = 1 + x + x²/2! + x³/3! + ... 
    
    Args:
        x: L'exposant
    
    Returns: 
        float: e^x
    
    Examples:
        >>> exponentielle(0)
        1.0
        >>> exponentielle(1)
        2.718281828...  (≈ E)
    """
    # Série de Taylor :  e^x = Σ(n=0 à ∞) x^n / n!
    resultat = 1.0  # Premier terme (x^0 / 0!  = 1)
    terme = 1.0
    
    for n in range(1, 100):  # 100 termes suffisent
        terme *= x / n  # Calcul efficace du terme suivant
        resultat += terme
        
        # Arrêter si le terme devient négligeable
        if valeur_absolue(terme) < 1e-15:
            break
    
    return resultat