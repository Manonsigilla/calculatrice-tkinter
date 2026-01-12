# tests/test_calculateur.py
"""
Tests unitaires pour le module calculateur.
"""

import unittest
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour pouvoir importer src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.calculateur import calculer, tokenize, infix_to_rpn, evaluer_rpn
from src.exceptions import DivisionParZeroError


class TestCalculateur(unittest.TestCase):
    """Tests du module calculateur"""
    
    def test_addition_simple(self):
        """Test addition de base"""
        self.assertEqual(calculer("2 + 3"), 5)
    
    def test_soustraction_simple(self):
        """Test soustraction de base"""
        self.assertEqual(calculer("10 - 5"), 5)
    
    def test_multiplication_simple(self):
        """Test multiplication de base"""
        self.assertEqual(calculer("3 * 4"), 12)
    
    def test_division_simple(self):
        """Test division de base"""
        self.assertEqual(calculer("10 / 2"), 5)
    
    def test_priorite_multiplication(self):
        """Test priorité :  multiplication avant addition"""
        self.assertEqual(calculer("2 + 3 * 4"), 14)  # Pas 20 ! 
    
    def test_priorite_division(self):
        """Test priorité : division avant soustraction"""
        self.assertEqual(calculer("10 - 6 / 2"), 7)  # Pas 2 !
    
    def test_parentheses(self):
        """Test priorité avec parenthèses"""
        self.assertEqual(calculer("(2 + 3) * 4"), 20)
    
    def test_expression_complexe(self):
        """Test expression complexe"""
        self.assertEqual(calculer("2 + 3 * 4 - 5 / 5"), 13)
    
    def test_division_par_zero(self):
        """Test division par zéro"""
        with self.assertRaises(DivisionParZeroError):
            calculer("5 / 0")
    
    def test_nombres_decimaux(self):
        """Test avec nombres décimaux"""
        self.assertAlmostEqual(calculer("3.5 + 2.5"), 6.0)
    
    # TODO: Ajouter 10+ tests supplémentaires


if __name__ == "__main__":
    unittest.main()