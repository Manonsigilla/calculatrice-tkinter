# Calculatrice Tkinter — Version 3.1

Dernière mise à jour : 2026-01-18  
Version actuelle : **3.1**

Une application de calculatrice graphique légère développée en Python avec Tkinter, conçue pour combiner simplicité d'utilisation, fiabilité et petites fonctionnalités avancées pour un usage quotidien.

---

## Table des matières
- [Aperçu](#aperçu)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Version actuelle](#version-actuelle)
- [Historique des versions (évolution)](#historique-des-versions-évolution)
- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Installation pas à pas](#installation-pas-à-pas)
  - [Exemples de commandes](#exemples-de-commandes)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [Contributeurs](#contributeurs)
- [Licence](#licence)
- [Contact](#contact)

---

## Aperçu
Cette calculatrice vise à fournir une interface claire pour les opérations arithmétiques basiques et quelques fonctionnalités étendues (mémoire, historique, gestion d'erreurs). Le projet est orienté vers la pédagogie et la facilité d'extension : le code est volontairement simple et commenté pour que d'autres puisse s'en inspirer ou l'améliorer.

## Fonctionnalités principales
- Opérations basiques : addition, soustraction, multiplication, division.
- Gestion des erreurs (division par zéro, saisie invalide).
- Support clavier (saisie via le clavier numérique et touches opérateurs).
- Mémoire simple (M+, M-, MR, MC).
- Historique des calculs (consultable dans l'interface).
- Interface responsive adaptée à un usage bureau.

## Version actuelle
- Version : **3.1**
- Etat : stable, corrections de bugs et améliorations d'accessibilité.

## Historique des versions (évolution)
- 1.0 — Première version publique
  - Mise en place de l'interface Tkinter de base.
  - Opérations arithmétiques et boutons graphiques.
- 1.1 — Corrections mineures
  - Correction des bugs d'affichage et gestion basique des entrées invalides.
- 1.5 — Amélioration de l'expérience utilisateur
  - Ajout du support clavier.
  - Ajustement du layout pour meilleures dimensions d'écran.
- 2.0 — Refactor et nouvelle ergonomie
  - Réorganisation du code en modules.
  - Nouvelle apparence (thème clair) et meilleure gestion des événements.
- 2.5 — Fonctionnalités avancées
  - Ajout de la mémoire (M+, M-, MR, MC).
  - Ajout d'un panneau d'historique pour revenir sur les calculs précédents.
- 3.0 — Robustesse et tests
  - Renforcement de la gestion des erreurs.
  - Meilleures validations des entrées et nettoyage du code.
  - Ajout d'un petit jeu de tests unitaires (si présent dans le dépôt).
- 3.1 — Améliorations d'accessibilité et performance
  - Corrections de bugs signalés (rendus, comportements de la mémoire).
  - Optimisations mineures de performance au lancement.
  - Améliorations d'accessibilité clavier (focus, labels lisibles pour lecteurs d'écran).
  - Mise à jour de la documentation et du README.

> Remarque : pour la liste complète des commits et détails techniques, consultez l'historique Git du dépôt.

## Installation

### Prérequis
- Python 3.8 ou supérieur.
- Tkinter (généralement inclus avec Python sur Windows/macOS ; sous certaines distributions Linux, paquet séparé).
- (Optionnel) virtualenv/venv pour isoler l'environnement.

Dépendances externes :
- Le projet utilise principalement la bibliothèque standard. S'il existe un fichier `requirements.txt` dans le dépôt, installez les dépendances listées.

### Installation pas à pas (recommandée)
1. Cloner le dépôt :
   - git clone https://github.com/Manonsigilla/calculatrice-tkinter.git
   - cd calculatrice-tkinter
2. (Optionnel) Créer et activer un environnement virtuel :
   - python3 -m venv .venv
   - Sous Linux/macOS : source .venv/bin/activate
   - Sous Windows : .venv\Scripts\activate
3. Installer les dépendances (si `requirements.txt` existe) :
   - pip install -r requirements.txt
4. Vérifier que Tkinter est disponible :
   - Sous Debian/Ubuntu : sudo apt-get install python3-tk
   - Sous Fedora : sudo dnf install python3-tkinter
   - Sous macOS : Tkinter est inclus dans la distribution python.org. Si installé via Homebrew, vérifier les paquets correspondants.
   - Sous Windows : Tkinter est généralement inclus dans l'installateur officiel de Python.
5. Lancer l'application :
   - python3 calculatrice.py
   - (Remplacez `calculatrice.py` par le nom du fichier principal si différent.)

### Exemples de commandes
- Cloner et lancer rapidement :
  - git clone https://github.com/Manonsigilla/calculatrice-tkinter.git && cd calculatrice-tkinter
  - python3 calculatrice.py

Si vous rencontrez une erreur indiquant l'absence de module Tkinter, reportez-vous à la section "Prérequis" ci-dessus et installez le paquet système approprié.

## Utilisation
- Saisir les chiffres et les opérations à l'aide de la souris ou du clavier.
- Utiliser les boutons mémoire pour stocker/recuperer des valeurs :
  - M+ : ajouter la valeur affichée à la mémoire
  - M- : soustraire la valeur affichée de la mémoire
  - MR : rappeler la mémoire
  - MC : effacer la mémoire
- L'historique conserve les calculs précédents ; cliquer sur un élément de l'historique pour le réutiliser (si la fonctionnalité est activée).
- En cas d'erreur (ex. division par zéro), un message lisible est affiché et l'application reste stable.

## Contribuer
Les contributions sont bienvenues ! Voici quelques lignes directrices :
1. Forkez le dépôt et créez une branche de travail nommée `feature/` ou `fix/` suivie d'une courte description.
2. Faites des commits atomiques et descriptifs.
3. Ouvrez une pull request en décrivant clairement l'objectif et les changements.
4. Respectez les bonnes pratiques Python (PEP8) et commentez le code si nécessaire.
5. Si vous ajoutez des dépendances, justifiez-les et mettez à jour `requirements.txt`.

Si vous n'êtes pas sûr.e de la meilleure façon d'implémenter une amélioration, ouvrez d'abord une issue pour discussion.

## Contributeurs
- Manon Sigilla — GitHub: [@Manonsigilla](https://github.com/Manonsigilla)
- Angie Valencia — GitHub: [@Angie](https://github.com/angie-valencia)
- Louis Varennes — GitHub: [@Louis](https://github.com/louis-varennes)


## Licence
Libre d'utilisation, projet scolaire

## Contact
Pour questions, suggestions ou signalement de bugs :
- Ouvrez une issue sur le dépôt : https://github.com/Manonsigilla/calculatrice-tkinter/issues
- Ou contactez les auteurs via leur profil GitHub

---

Merci d'utiliser ce projet ! Les retours et contributions sont appréciés pour améliorer la stabilité, l'ergonomie et les fonctionnalités.
