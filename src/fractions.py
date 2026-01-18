# src/fractions.py
"""
================================================================================
Module de gestion des fractions - VERSION 3.0
================================================================================

Ce module permet de convertir les nombres décimaux en fractions simplifiées. 
Exemple : 0.5 → 1/2, 0.333... → 1/3, 2.75 → 11/4

================================================================================
"""


def pgcd(a: int, b:  int) -> int:
    """
    Calcule le Plus Grand Commun Diviseur (PGCD) de deux nombres. 
    
    Utilise l'algorithme d'Euclide (300 av. J.-C.).
    
    Args:
        a: Premier nombre entier
        b: Deuxième nombre entier
    
    Returns:
        int: Le PGCD de a et b
    
    Examples:
        >>> pgcd(12, 8)
        4
        >>> pgcd(15, 25)
        5
    
    Algorithme :
        pgcd(a, b) = pgcd(b, a % b) jusqu'à ce que b = 0
    """
    a, b = abs(a), abs(b)  # Travailler avec des valeurs absolues
    
    while b != 0:
        a, b = b, a % b
    
    return a


def decimal_vers_fraction(decimal: float, precision: int = 1000000) -> tuple:
    """
    Convertit un nombre décimal en fraction simplifiée.
    
    Args:
        decimal: Le nombre décimal à convertir
        precision: Précision maximale du dénominateur
    
    Returns: 
        tuple: (numérateur, dénominateur)
    
    Examples:
        >>> decimal_vers_fraction(0.5)
        (1, 2)
        >>> decimal_vers_fraction(0.333333)
        (1, 3)
        >>> decimal_vers_fraction(2.75)
        (11, 4)
    
    Algorithme :
        1. Gérer le signe
        2. Séparer partie entière et décimale
        3. Utiliser l'algorithme des fractions continues
        4. Simplifier avec le PGCD
    """
    # Gérer le signe
    signe = 1 if decimal >= 0 else -1
    decimal = abs(decimal)
    
    # Partie entière
    partie_entiere = int(decimal)
    partie_decimale = decimal - partie_entiere
    
    # Si c'est un entier, retourner directement
    if partie_decimale < 1e-9:
        return (signe * partie_entiere, 1)
    
    # Algorithme des fractions continues (simplifié)
    # On cherche num/den tel que |decimal - num/den| soit minimal
    meilleur_num = 0
    meilleur_den = 1
    meilleure_diff = decimal
    
    for den in range(1, precision + 1):
        num = round(decimal * den)
        diff = abs(decimal - num / den)
        
        if diff < meilleure_diff:
            meilleure_diff = diff
            meilleur_num = num
            meilleur_den = den
        
        # Si la différence est très petite, on a trouvé
        if diff < 1e-10:
            break
    
    # Simplifier la fraction avec le PGCD
    diviseur = pgcd(meilleur_num, meilleur_den)
    numerateur = meilleur_num // diviseur
    denominateur = meilleur_den // diviseur
    
    return (signe * numerateur, denominateur)


def formater_fraction(numerateur: int, denominateur: int) -> str:
    """
    Formate une fraction de manière lisible.
    
    Args:
        numerateur:  Le numérateur
        denominateur: Le dénominateur
    
    Returns: 
        str: La fraction formatée
    
    Examples: 
        >>> formater_fraction(3, 4)
        '3/4'
        >>> formater_fraction(5, 1)
        '5'
        >>> formater_fraction(7, 2)
        '3 + 1/2'
    """
    # Si le dénominateur est 1, c'est un entier
    if denominateur == 1:
        return str(numerateur)
    
    # Si le numérateur est plus grand que le dénominateur, extraire la partie entière
    if abs(numerateur) >= denominateur:
        partie_entiere = numerateur // denominateur
        reste = abs(numerateur % denominateur)
        
        if reste == 0:
            return str(partie_entiere)
        else:
            signe = "-" if numerateur < 0 else ""
            return f"{signe}{abs(partie_entiere)} + {reste}/{denominateur}"
    
    # Fraction simple
    return f"{numerateur}/{denominateur}"


def decimal_vers_fraction_str(decimal: float) -> str:
    """
    Convertit un décimal en chaîne de fraction lisible.
    
    Args:
        decimal: Le nombre à convertir
    
    Returns: 
        str: La fraction formatée
    
    Examples:
        >>> decimal_vers_fraction_str(0.5)
        '1/2'
        >>> decimal_vers_fraction_str(2.75)
        '2 + 3/4'
    """
    num, den = decimal_vers_fraction(decimal)
    return formater_fraction(num, den)