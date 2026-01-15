# tests/test_validateur.py
"""
Tests unitaires pour le module validateur.
"""

import unittest
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent. parent))

from src.validateur import Validateur
from src.exceptions import (
    ExpressionVideError,
    CaractereInvalideError,
    ParenthesesError,
    OperateurError,
    NombreInvalideError
)


class TestValidateur(unittest.TestCase):
    """Tests du module validateur"""
    
    def setUp(self):
        """Initialise un validateur pour chaque test"""
        self.validateur = Validateur()
    
    # ========== Tests d'expressions valides ==========
    
    def test_expression_simple_valide(self):
        """Test expression simple valide"""
        valide, msg = self.validateur.valider_expression("2 + 3")
        self.assertTrue(valide)
        self.assertEqual(msg, "")
    
    def test_expression_decimale_valide(self):
        """Test avec nombres décimaux"""
        valide, msg = self.validateur. valider_expression("3.5 + 2.5")
        self.assertTrue(valide)
    
    def test_expression_parentheses_valide(self):
        """Test avec parenthèses"""
        valide, msg = self.validateur.valider_expression("(2 + 3) * 4")
        self.assertTrue(valide)
    
    def test_expression_complexe_valide(self):
        """Test expression complexe"""
        valide, msg = self.validateur.valider_expression("(2 + 3) * (4 - 1) / 5")
        self.assertTrue(valide)
    
    def test_nombre_negatif_valide(self):
        """Test avec nombre négatif"""
        valide, msg = self.validateur. valider_expression("-3 + 5")
        self.assertTrue(valide)
    
    def test_nombre_negatif_parentheses(self):
        """Test nombre négatif entre parenthèses"""
        valide, msg = self.validateur.valider_expression("(-3 + 5)")
        self.assertTrue(valide)
    
    def test_decimal_sans_zero_debut(self):
        """Test nombre décimal commençant par point"""
        valide, msg = self.validateur.valider_expression(". 5 + 3")
        self.assertTrue(valide)
    
    def test_decimal_sans_decimales(self):
        """Test nombre décimal finissant par point"""
        valide, msg = self.validateur.valider_expression("5.  + 3")
        self.assertTrue(valide)
    
    # ========== Tests d'expressions invalides ==========
    
    def test_expression_vide(self):
        """Test expression vide"""
        valide, msg = self.validateur. valider_expression("")
        self.assertFalse(valide)
        self.assertIn("Aucune expression", msg)
    
    def test_expression_espaces_seulement(self):
        """Test expression avec seulement des espaces"""
        valide, msg = self.validateur.valider_expression("   ")
        self.assertFalse(valide)
        self.assertIn("Aucune expression", msg)
    
    def test_caractere_invalide_lettre(self):
        """Test caractère invalide (lettre)"""
        valide, msg = self.validateur. valider_expression("2 + a")
        self.assertFalse(valide)
        self.assertIn("Caractère 'a'", msg)
        self.assertIn("position", msg)
    
    def test_caractere_invalide_symbole(self):
        """Test caractère invalide (symbole)"""
        valide, msg = self.validateur.valider_expression("5 & 3")
        self.assertFalse(valide)
        self.assertIn("Caractère '&'", msg)
    
    def test_parenthese_non_fermee(self):
        """Test parenthèse non fermée"""
        valide, msg = self.validateur.valider_expression("(2 + 3")
        self.assertFalse(valide)
        self.assertIn("parenthèse", msg. lower())
        self.assertIn("manquante", msg.lower())
    
    def test_parenthese_non_ouverte(self):
        """Test parenthèse fermante sans ouvrante"""
        valide, msg = self.validateur.valider_expression("2 + 3)")
        self.assertFalse(valide)
        self.assertIn("sans ouvrante", msg)
    
    def test_parentheses_vides(self):
        """Test parenthèses vides"""
        valide, msg = self. validateur.valider_expression("2 + ()")
        self.assertFalse(valide)
        self.assertIn("vides", msg.lower())
    
    def test_operateurs_consecutifs_invalides(self):
        """Test opérateurs consécutifs invalides"""
        valide, msg = self.validateur.valider_expression("5 + * 3")
        self.assertFalse(valide)
        self.assertIn("inattendu", msg.lower())
    
    def test_operateur_en_fin(self):
        """Test opérateur en fin d'expression"""
        valide, msg = self.validateur.valider_expression("5 + 3 *")
        self.assertFalse(valide)
        self.assertIn("fin", msg.lower())
    
    def test_nombre_multi_points(self):
        """Test nombre avec plusieurs points"""
        valide, msg = self.validateur. valider_expression("5.3. 2 + 1")
        self.assertFalse(valide)
        self.assertIn("invalide", msg.lower())
        self.assertIn("5.3.2", msg)
    
    def test_division_multiplication_debut(self):
        """Test opérateur * ou / en début"""
        valide, msg = self.validateur.valider_expression("* 5")
        self.assertFalse(valide)
        self.assertIn("début", msg.lower())
    
    def test_operateur_apres_parenthese_ouvrante(self):
        """Test opérateur invalide après parenthèse ouvrante"""
        valide, msg = self.validateur.valider_expression("(* 5)")
        self.assertFalse(valide)
    
    def test_operateur_avant_parenthese_fermante(self):
        """Test opérateur avant parenthèse fermante"""
        valide, msg = self. validateur.valider_expression("(5 +)")
        self.assertFalse(valide)
        self.assertIn("avant ')'", msg)


if __name__ == "__main__":
    unittest.main()