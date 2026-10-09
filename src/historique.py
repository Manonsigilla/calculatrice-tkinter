# src/historique.py
"""
Module de gestion de l'historique des calculs. 
Stocke les opérations dans un fichier JSON pour persistance.

VERSION 3.0 - NOUVEAUTÉS :
--------------------------
    - Recherche dans l'historique
    - Export en CSV
    - Export en format texte
    - Filtrage par date
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


def _afficher(message: str) -> None:
    """
    Affiche un message sur la sortie standard de façon sûre.

    Sur Windows, la console utilise souvent l'encodage cp1252 qui ne sait pas
    représenter les emojis (✅, ❌, ⚠️, 📦) : un simple print() levait alors une
    UnicodeEncodeError. Dans exporter_csv/exporter_texte, cette exception
    survenait APRÈS l'écriture du fichier et faisait échouer l'export (le
    fichier était écrit mais la fonction ne renvoyait jamais True).
    """
    try:
        print(message)
    except UnicodeEncodeError:
        # Repli : remplacer les caractères non représentables
        encodage = getattr(__import__('sys').stdout, 'encoding', None) or 'ascii'
        print(message.encode(encodage, 'replace').decode(encodage))


class Historique:
    """
    Gère l'historique des calculs effectués
    
    Fonctionnalités : 
        - Ajout d'opérations
        - Affichage de l'historique
        - Recherche dans l'historique
        - Export CSV
        - Sauvegarde/chargement persistant
    """
    
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
        self.operations.clear()
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
            _afficher(f"Erreur lors de la sauvegarde de l'historique : {e}")
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
                    self.operations = json.load(f)

                # Validation :  s'assurer que c'est une liste
                if not isinstance(self.operations, list):
                    raise ValueError("Le fichier historique n'est pas une liste")

                # Ne conserver que les opérations bien formées. Un fichier
                # (même valide en JSON) pouvait contenir des entrées
                # inattendues ; l'affichage et la recherche levaient alors un
                # TypeError (« string indices must be integers ») et les
                # boutons « Voir » / « Rechercher » plantaient silencieusement.
                champs_requis = {'expression', 'resultat', 'timestamp'}
                operations_valides = [
                    op for op in self.operations
                    if isinstance(op, dict) and champs_requis <= op.keys()
                ]
                if len(operations_valides) != len(self.operations):
                    _afficher(
                        f"⚠️ {len(self.operations) - len(operations_valides)} "
                        f"entrée(s) invalide(s) ignorée(s) dans l'historique"
                    )
                self.operations = operations_valides

            except json.JSONDecodeError:
                _afficher("⚠️ Fichier historique corrompu, création d'un backup")
                self._creer_backup()
                self.operations = []
                
            except Exception as e:
                _afficher(f"⚠️ Erreur lors du chargement de l'historique : {e}")
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
                _afficher(f"📦 Backup créé : {backup_name}")
        except Exception as e:
            _afficher(f"Impossible de créer un backup : {e}")
    
    def obtenir_historique(self):
        """
        Retourne l'historique sous forme de tuple (expression, resultat, timestamp)
        pour l'affichage dans l'interface. 
        
        Returns:
            list: Liste de tuples (expression, resultat, timestamp)
        """
        resultats = []
        for op in self.operations:
            resultats.append((
                op['expression'],
                op['resultat'],
                op['timestamp']
            ))
        return resultats

    def obtenir_dernier(self):
        """
        Retourne la dernière opération effectuée.
        
        Returns:
            dict ou None: La dernière opération, ou None si l'historique est vide
        """
        if self.operations:
            return self.operations[-1]
        return None
    
    def compter(self) -> int:
        """
        Retourne le nombre d'opérations dans l'historique.
        
        Returns:
            int:  Nombre d'opérations
        """
        return len(self.operations)
    
    #=========================================================================
    # NOUVELLES FONCTIONNALITÉS VERSION 3.0
    #=========================================================================
    
    def rechercher(self, terme: str) -> List[dict]:
        """
        Recherche des opérations contenant un terme spécifique.
        
        La recherche est insensible à la casse et cherche dans les expressions. 
        
        Args:
            terme: Le terme à rechercher
        
        Returns:
            list:  Liste des opérations correspondantes
        
        Examples:
            >>> hist = Historique()
            >>> hist.ajouter("sin(PI)", 0.0)
            >>> hist.ajouter("cos(0)", 1.0)
            >>> resultats = hist.rechercher("sin")
            >>> len(resultats)
            1
        """
        resultats = []
        terme_lower = terme.lower()
        
        for op in self.operations:
            # Rechercher dans l'expression
            if terme_lower in op['expression'].lower():
                resultats.append(op)
        
        return resultats
    
    def filtrer_par_date(self, date_debut: str = None, date_fin: str = None) -> List[dict]:
        """
        Filtre l'historique par plage de dates.
        
        Args:
            date_debut:  Date de début au format ISO (ex: "2024-01-01")
            date_fin:  Date de fin au format ISO (ex: "2024-12-31")
        
        Returns: 
            list:  Opérations dans la plage de dates
        """
        resultats = []
        
        for op in self.operations:
            timestamp = op['timestamp']

            # Comparer uniquement la portion de date. Un timestamp ISO complet
            # ("2024-12-31T10:30:00") est toujours supérieur à la date seule
            # ("2024-12-31") : sans cette troncature, les calculs du jour même
            # étaient exclus de la fin de plage.
            if date_debut and timestamp[:len(date_debut)] < date_debut:
                continue
            if date_fin and timestamp[:len(date_fin)] > date_fin:
                continue

            resultats.append(op)
        
        return resultats
    
    def exporter_csv(self, nom_fichier: str = "historique_export.csv") -> bool:
        """
        Exporte l'historique au format CSV.
        
        Le fichier CSV contient 3 colonnes :  Expression, Résultat, Date
        
        Args:
            nom_fichier: Nom du fichier CSV à créer
        
        Returns: 
            bool: True si l'export a réussi, False sinon
        
        Examples:
            >>> hist = Historique()
            >>> hist.exporter_csv("mes_calculs.csv")
            True
        """
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                # En-tête CSV
                f.write("Expression,Résultat,Date\n")
                
                # Données
                for op in self.operations:
                    # Échapper les virgules dans l'expression
                    expression = op['expression'].replace(',', ';')
                    resultat = op['resultat']
                    timestamp = op['timestamp']
                    
                    f.write(f'"{expression}",{resultat},"{timestamp}"\n')
            
            _afficher(f"✅ Historique exporté vers {nom_fichier}")
            return True
            
        except Exception as e:
            _afficher(f"❌ Erreur lors de l'export CSV : {e}")
            return False
    
    def exporter_texte(self, nom_fichier: str = "historique_export.txt") -> bool:
        """
        Exporte l'historique au format texte lisible.
        
        Args:
            nom_fichier:  Nom du fichier texte à créer
        
        Returns: 
            bool: True si l'export a réussi, False sinon
        """
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("HISTORIQUE DES CALCULS\n")
                f.write("=" * 60 + "\n\n")
                
                if not self.operations:
                    f.write("Aucun calcul dans l'historique.\n")
                else:
                    for i, op in enumerate(self.operations, 1):
                        f. write(f"#{i}\n")
                        f.write(f"  Expression : {op['expression']}\n")
                        f.write(f"  Résultat   : {op['resultat']}\n")
                        f.write(f"  Date       : {op['timestamp']}\n")
                        f.write("\n")
                
                f.write("=" * 60 + "\n")
                f.write(f"Total : {len(self.operations)} calcul(s)\n")
            
            _afficher(f"✅ Historique exporté vers {nom_fichier}")
            return True
            
        except Exception as e:
            _afficher(f"❌ Erreur lors de l'export texte : {e}")
            return False