# src/historique.py
"""
Module de gestion de l'historique des calculs. 
Stocke les opérations dans un fichier JSON pour persistance.
"""

import json
from datetime import datetime
from pathlib import Path


class Historique:
    """Gère l'historique des calculs effectués"""
    
    def __init__(self, fichier='historique.json'):
        """
        Initialise l'historique et charge les données existantes.
        
        Args:
            fichier: Nom du fichier JSON pour stocker l'historique
        """
        self.fichier = fichier
        self.operations = []
        self.charger()
    
    def ajouter(self, expression: str, resultat: float):
        """
        Ajoute une opération à l'historique.
        
        Args:
            expression: L'expression calculée (ex: "2 + 3")
            resultat: Le résultat du calcul (ex: 5.0)
        
        Example:
            >>> hist = Historique()
            >>> hist.ajouter("2 + 3", 5.0)
        """
        operation = {
            'expression': expression,
            'resultat': resultat,
            'timestamp': datetime.now().isoformat()
        }
        self.operations.append(operation)
        self.sauvegarder()
    
    def afficher(self) -> list:
        """
        Retourne toutes les opérations de l'historique.
        
        Returns:
            list: Liste des opérations
        
        Example:
            >>> hist = Historique()
            >>> hist.ajouter("2 + 3", 5.0)
            >>> hist.afficher()
            [{'expression': '2 + 3', 'resultat': 5.0, 'timestamp': '... '}]
        """
        return self.operations
    
    def effacer(self):
        """
        Vide complètement l'historique. 
        
        Example:
            >>> hist = Historique()
            >>> hist.effacer()
            >>> len(hist.afficher())
            0
        """
        self.operations.clear()
        self.sauvegarder()
    
    def sauvegarder(self):
        """
        Sauvegarde l'historique dans le fichier JSON.
        """
        try:
            with open(self.fichier, 'w', encoding='utf-8') as f:
                json.dump(self.operations, f, indent=2, ensure_ascii=False)
        except Exception as e: 
            print(f"Erreur lors de la sauvegarde de l'historique :  {e}")
    
    def charger(self):
        """
        Charge l'historique depuis le fichier JSON.
        Si le fichier n'existe pas, initialise un historique vide.
        """
        if Path(self.fichier).exists():
            try:
                with open(self.fichier, 'r', encoding='utf-8') as f:
                    self. operations = json.load(f)
            except json.JSONDecodeError:
                print("Fichier historique corrompu, création d'un nouvel historique")
                self.operations = []
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique : {e}")
                self.operations = []
        else: 
            self.operations = []
    
    def obtenir_dernier(self):
        """
        Retourne la dernière opération effectuée.
        
        Returns:
            dict ou None: La dernière opération, ou None si l'historique est vide
        """
        if self.operations:
            return self.operations[-1]
        return None