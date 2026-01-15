# tests/test_historique.py
"""
Tests unitaires pour le module historique.
"""

import unittest
import sys
import os
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.historique import Historique


class TestHistorique(unittest. TestCase):
    """Tests du module historique"""
    
    def setUp(self):
        """Crée un historique de test avant chaque test"""
        self. fichier_test = 'test_historique.json'
        self.historique = Historique(fichier=self.fichier_test)
        # S'assurer qu'on part d'un historique vide
        self.historique.effacer()
    
    def tearDown(self):
        """Nettoie après chaque test"""
        # Supprimer le fichier de test
        if os.path.exists(self.fichier_test):
            os.remove(self.fichier_test)
        if os.path.exists(self. fichier_test + '.tmp'):
            os.remove(self. fichier_test + '.tmp')
    
    def test_historique_vide_initial(self):
        """Test historique vide au départ"""
        self.assertEqual(len(self.historique.afficher()), 0)
    
    def test_ajouter_operation(self):
        """Test ajout d'une opération"""
        self.historique.ajouter("2 + 3", 5.0)
        operations = self.historique.afficher()
        
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]['expression'], "2 + 3")
        self.assertEqual(operations[0]['resultat'], 5.0)
        self.assertIn('timestamp', operations[0])
    
    def test_ajouter_plusieurs_operations(self):
        """Test ajout de plusieurs opérations"""
        self.historique.ajouter("2 + 3", 5.0)
        self.historique.ajouter("10 / 2", 5.0)
        self.historique.ajouter("3 * 4", 12.0)
        
        self.assertEqual(len(self.historique.afficher()), 3)
    
    def test_effacer_historique(self):
        """Test effacement de l'historique"""
        self.historique.ajouter("2 + 3", 5.0)
        self.historique.ajouter("10 / 2", 5.0)
        
        self.assertEqual(len(self.historique. afficher()), 2)
        
        self.historique.effacer()
        self.assertEqual(len(self.historique.afficher()), 0)
    
    def test_persistance_fichier(self):
        """Test que l'historique est sauvegardé dans le fichier"""
        self.historique.ajouter("2 + 3", 5.0)
        
        # Créer un nouvel objet qui charge depuis le même fichier
        historique2 = Historique(fichier=self.fichier_test)
        
        operations = historique2.afficher()
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]['expression'], "2 + 3")
    
    def test_obtenir_dernier(self):
        """Test obtention de la dernière opération"""
        self.assertIsNone(self.historique.obtenir_dernier())
        
        self.historique. ajouter("2 + 3", 5.0)
        self.historique.ajouter("10 / 2", 5.0)
        
        dernier = self.historique.obtenir_dernier()
        self.assertIsNotNone(dernier)
        self.assertEqual(dernier['expression'], "10 / 2")
    
    def test_compter_operations(self):
        """Test comptage des opérations"""
        self.assertEqual(self.historique.compter(), 0)
        
        self.historique.ajouter("2 + 3", 5.0)
        self.assertEqual(self.historique.compter(), 1)
        
        self.historique.ajouter("10 / 2", 5.0)
        self.assertEqual(self.historique.compter(), 2)
    
    def test_rechercher_operations(self):
        """Test recherche dans l'historique"""
        self.historique.ajouter("2 + 3", 5.0)
        self.historique.ajouter("10 / 2", 5.0)
        self.historique.ajouter("2 * 5", 10.0)
        
        resultats = self.historique.rechercher("2")
        self.assertEqual(len(resultats), 3)  # Toutes contiennent "2"
        
        resultats = self.historique.rechercher("/")
        self.assertEqual(len(resultats), 1)  # Seule "10 / 2"
    
    def test_nombres_decimaux(self):
        """Test avec nombres décimaux"""
        self.historique.ajouter("3.5 + 2.5", 6.0)
        
        operations = self.historique.afficher()
        self.assertEqual(operations[0]['resultat'], 6.0)


if __name__ == "__main__":
    unittest.main()