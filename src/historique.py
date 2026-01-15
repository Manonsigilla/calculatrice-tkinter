# src/historique.py
"""
Module de gestion de l'historique des calculs. 
Stocke les opérations dans un fichier JSON pour persistance.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class Historique:
    """Gère l'historique des calculs effectués"""
    
    def __init__(self, fichier='historique.json'):
        """
        Initialise l'historique et charge les données existantes.
        
        Args:
            fichier:  Nom du fichier JSON pour stocker l'historique
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
            list: Liste des opérations (copie pour éviter modifications externes)
        
        Example:
            >>> hist = Historique()
            >>> hist.ajouter("2 + 3", 5.0)
            >>> hist.afficher()
            [{'expression': '2 + 3', 'resultat': 5.0, 'timestamp': '... '}]
        """
        # Retourner une copie pour éviter modifications externes
        return self.operations.copy()
    
    def effacer(self):
        """
        Vide complètement l'historique. 
        
        Example:
            >>> hist = Historique()
            >>> hist.effacer()
            >>> len(hist.afficher())
            0
        """
        self. operations.clear()
        self.sauvegarder()
    
    def sauvegarder(self):
        """
        Sauvegarde l'historique dans le fichier JSON. 
        Utilise une sauvegarde atomique pour éviter la corruption.
        """
        try:
            # Sauvegarde atomique :  écrire dans un fichier temporaire
            # puis remplacer l'ancien fichier
            fichier_temp = self.fichier + '.tmp'
            
            with open(fichier_temp, 'w', encoding='utf-8') as f:
                json.dump(self.operations, f, indent=2, ensure_ascii=False)
            
            # Remplacer l'ancien fichier par le nouveau (opération atomique)
            # os.replace est atomique sur la plupart des systèmes
            if os.path.exists(self.fichier):
                os.replace(fichier_temp, self.fichier)
            else:
                os.rename(fichier_temp, self.fichier)
                
        except Exception as e: 
            print(f"Erreur lors de la sauvegarde de l'historique : {e}")
            # Nettoyer le fichier temporaire en cas d'erreur
            if os.path.exists(fichier_temp):
                try:
                    os.remove(fichier_temp)
                except:
                    pass
    
    def charger(self):
        """
        Charge l'historique depuis le fichier JSON. 
        Si le fichier n'existe pas, initialise un historique vide. 
        Si le fichier est corrompu, crée un backup et réinitialise.
        """
        if Path(self.fichier).exists():
            try:
                with open(self.fichier, 'r', encoding='utf-8') as f:
                    self. operations = json.load(f)
                    
                # Validation :  s'assurer que c'est une liste
                if not isinstance(self.operations, list):
                    raise ValueError("Le fichier historique n'est pas une liste")
                    
            except json.JSONDecodeError:
                print("⚠️ Fichier historique corrompu, création d'un backup")
                self._creer_backup()
                self.operations = []
                
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de l'historique : {e}")
                self._creer_backup()
                self.operations = []
        else:
            self.operations = []
    
    def _creer_backup(self):
        """Crée un backup du fichier corrompu"""
        try:
            if Path(self.fichier).exists():
                backup_name = f"{self.fichier}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(self.fichier, backup_name)
                print(f"📦 Backup créé : {backup_name}")
        except Exception as e:
            print(f"Impossible de créer un backup : {e}")
    
    def obtenir_dernier(self):
        """
        Retourne la dernière opération effectuée.
        
        Returns:
            dict ou None: La dernière opération, ou None si l'historique est vide
        """
        if self.operations:
            return self. operations[-1]
        return None
    
    def compter(self) -> int:
        """
        Retourne le nombre d'opérations dans l'historique.
        
        Returns:
            int:  Nombre d'opérations
        """
        return len(self.operations)
    
    def rechercher(self, terme: str) -> list:
        """
        Recherche des opérations contenant un terme spécifique.
        
        Args:
            terme: Le terme à rechercher dans les expressions
        
        Returns:
            list:  Liste des opérations correspondantes
        """
        resultats = []
        for op in self.operations:
            if terme in op['expression']:
                resultats.append(op)
        return resultats