# Calculatrice Tkinter — Version 3.1

Dernière mise à jour : 2026-10-09  
Version actuelle : **3.1**

Une calculatrice scientifique avec interface graphique (CustomTkinter). Le
moteur de calcul est écrit en Python pur : tokenisation, conversion en notation
polonaise inversée (RPN), évaluation, et fonctions trigonométriques /
logarithmiques calculées par séries de Taylor — sans `eval` ni bibliothèque
mathématique externe.

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
- [Syntaxe](#syntaxe)
- [Raccourcis clavier](#raccourcis-clavier)
- [Tests](#tests)
- [Structure du projet](#structure-du-projet)
- [Limitations connues](#limitations-connues)
- [Contribuer](#contribuer)
- [Contributeurs](#contributeurs)
- [Licence](#licence)
- [Contact](#contact)

---

## Aperçu
Cette calculatrice fournit une interface claire pour les opérations
arithmétiques et un ensemble de fonctions scientifiques (racines, logarithmes,
exponentielle, trigonométrie en radians et en degrés, puissances). Elle gère
explicitement les erreurs (division par zéro, racine d'un nombre négatif,
logarithme d'un nombre ≤ 0, tangente non définie…) et garde un historique des
calculs. Le projet est orienté vers la pédagogie : le code est découpé en
modules commentés pour être facile à lire et à étendre.

## Fonctionnalités principales
- **Opérations** : addition, soustraction, multiplication, division, modulo `%`, puissance `^`.
- **Fonctions** : `sqrt`, `sqr`, `abs`, `inv`, `ln`, `log`, `exp`.
- **Trigonométrie** : `sin`, `cos`, `tan` (radians) et `sind`, `cosd`, `tand` (degrés).
- **Comparaison** : `min(a,b)` et `max(a,b)`.
- **Constantes** : `PI`, `E` et `ANS` (dernier résultat).
- **Modes** : `RAD`/`DEG` pour la trigonométrie, `DEC`/`FRAC` (décimal ou fraction).
- **Pourcentages** : `100 + 20%` → 120 (TVA), `200 - 15%` → 170 (réduction).
- **Historique** : consultation, recherche, export en CSV/TXT, effacement.
- **Graphiques** : tracé de fonctions de `x` sur un canevas, avec zoom.
- **Gestion des erreurs** : messages explicites, l'application ne plante pas.
- **Support clavier** et bouton « Copier » du résultat.

## Version actuelle
- Version : **3.1**
- État : stable.

## Historique des versions (évolution)
- **1.0** — Première version : interface Tkinter de base et opérations arithmétiques (`bd9ecd8`).
- **Fonctions scientifiques** — nombres négatifs, `sqrt`, modulo `%`, `abs`, `sin`/`cos`/`tan` (`963bcbf`).
- **3.0** — `ln`, `log`, `exp`, puissance `^`, `inv`, `sqr` ; constantes `PI`/`E`/`ANS` ;
  trigonométrie en degrés (`sind`, `cosd`, `tand`) ; affichage en fractions ;
  historique (recherche, export CSV/TXT) ; graphiques ; calcul de pourcentage (`036a2d5`).
- **3.1** — Corrections d'affichage et du validateur (`61efbe3`).
- **Documentation** — ajout du README (`000db75`).

> Pour la liste complète des commits et les détails techniques, consultez l'historique Git du dépôt.

## Installation

### Prérequis
- **Python 3.8 ou plus récent** (testé sous Python 3.13).
- **Tkinter** (généralement inclus avec Python sous Windows/macOS ; paquet séparé sous certaines distributions Linux).
- (Optionnel) `venv`/`virtualenv` pour isoler l'environnement.

Dépendance externe :
- **`customtkinter`** (interface graphique moderne). Le moteur de calcul, lui,
  n'utilise que la bibliothèque standard. La dépendance est listée dans
  `requirements.txt`.

### Installation pas à pas (recommandée)
1. Cloner le dépôt :
   - `git clone https://github.com/Manonsigilla/calculatrice-tkinter.git`
   - `cd calculatrice-tkinter`
2. (Optionnel) Créer et activer un environnement virtuel :
   - `python -m venv .venv`
   - Sous Linux/macOS : `source .venv/bin/activate`
   - Sous Windows : `.venv\Scripts\activate`
3. Installer les dépendances :
   - `pip install -r requirements.txt`
4. Vérifier que Tkinter est disponible :
   - Debian/Ubuntu : `sudo apt-get install python3-tk`
   - Fedora : `sudo dnf install python3-tkinter`
   - macOS : Tkinter est inclus dans la distribution python.org.
   - Windows : Tkinter est inclus dans l'installateur officiel de Python.
5. Lancer l'application (depuis la **racine du projet**) :
   - `python -m src.main`

> ⚠️ `python src/main.py` **ne fonctionne pas** : les modules s'importent avec le
> préfixe `src.` (ex. `from src.interface import …`), ce qui exige que la racine
> du projet soit dans le `sys.path` — c'est le cas avec `python -m src.main`.

### Exemples de commandes
```bash
git clone https://github.com/Manonsigilla/calculatrice-tkinter.git && cd calculatrice-tkinter
pip install -r requirements.txt
python -m src.main
```

Si vous rencontrez une erreur indiquant l'absence du module Tkinter, reportez-vous
à la section « Prérequis » ci-dessus et installez le paquet système approprié.

## Utilisation
- Saisir les chiffres et les opérations à l'aide de la souris **ou** du clavier.
- Les boutons `π`, `e` et `ANS` insèrent les constantes correspondantes (`ANS` =
  dernier résultat).
- Basculer `RAD`/`DEG` pour la trigonométrie, `DEC`/`FRAC` pour afficher le
  résultat en décimal ou en fraction.
- Le bouton « Copier » place le dernier résultat dans le presse-papier.
- « Graph » ouvre une fenêtre de tracé : entrer une fonction de `x`
  (ex. `sin(x)`, `x^2`, `ln(x)`, `2*x+3`), puis dessiner, zoomer, réinitialiser.
- L'historique (`Voir`, `Rechercher`, `Export`, `Effacer`) conserve les calculs
  précédents et permet de les rechercher et de les exporter.
- En cas d'erreur (ex. division par zéro), un message lisible est affiché et
  l'application reste stable.

## Syntaxe

| Catégorie | Éléments |
|---|---|
| Opérateurs | `+` `-` `*` `/` `%` (modulo) `^` (puissance) |
| Fonctions | `sqrt(x)` `sqr(x)` `abs(x)` `inv(x)` `ln(x)` `log(x)` `exp(x)` |
| Trigonométrie | `sin(x)` `cos(x)` `tan(x)` — `sind(x)` `cosd(x)` `tand(x)` en degrés |
| Comparaison | `min(a,b)` `max(a,b)` (exactement 2 arguments) |
| Constantes | `PI` `E` `ANS` |
| Regroupement | `(` `)` |

**Exemples**

```
3 + 5 * 2            → 13
(2 + 3) * 4          → 20
2^3^2                → 512          (puissance associative à droite)
sqrt(16) + sqr(3)    → 13
min(3, 7) * 2        → 6
ln(E)                → 1
exp(2)               → 7.389…
100 + 20%            → 120
```

## Raccourcis clavier

| Touche | Action |
|---|---|
| `Entrée` | Calculer |
| `Échap` | Tout effacer |
| `Retour arrière` | Effacer le dernier caractère |
| `0`–`9` | Chiffres |
| `+` `-` `*` `/` `%` `^` | Opérateurs |
| `(` `)` `.` `,` | Parenthèses et séparateurs |

## Tests

40 tests unitaires (calculateur, validateur, historique) :

```bash
python -m pytest tests/ -v
```

Ou sans pytest :

```bash
python -m unittest discover -s tests
```

## Structure du projet

```
calculatrice-tkinter/
├── src/
│   ├── main.py          # Point d'entrée
│   ├── interface.py     # Interface graphique (CustomTkinter)
│   ├── calculateur.py   # Moteur de calcul (tokenizer + RPN)
│   ├── validateur.py    # Validation des expressions
│   ├── graphique.py     # Tracé de fonctions
│   ├── fractions.py     # Conversion décimal → fraction
│   ├── historique.py    # Historique persistant (JSON)
│   └── exceptions.py    # Erreurs personnalisées
├── tests/               # Tests unitaires (unittest)
├── requirements.txt
└── README.md
```

## Limitations connues
- La **virgule** est le séparateur d'arguments de `min`/`max`, pas un séparateur
  décimal : écrire `3.5`, pas `3,5`.
- La **multiplication implicite** n'est pas supportée : écrire `2*PI`, pas `2PI`.
- La **notation scientifique** n'est pas supportée : écrire `1000`, pas `1e3`.
- Le **moins unaire** est prioritaire sur la puissance : `-2^2` vaut `4`
  (et non `-4` comme dans la convention mathématique usuelle).
- Un résultat trop grand (dépassement de capacité, ex. `9^400`) donne une erreur
  explicite plutôt qu'un nombre infini.

## Contribuer
Les contributions sont bienvenues ! Quelques lignes directrices :
1. Forkez le dépôt et créez une branche de travail nommée `feature/` ou `fix/` suivie d'une courte description.
2. Faites des commits atomiques et descriptifs.
3. Ouvrez une pull request en décrivant clairement l'objectif et les changements.
4. Respectez les bonnes pratiques Python (PEP8) et commentez le code si nécessaire.
5. Si vous ajoutez des dépendances, justifiez-les et mettez à jour `requirements.txt`.

Si vous n'êtes pas sûr·e de la meilleure façon d'implémenter une amélioration,
ouvrez d'abord une issue pour discussion.

## Contributeurs
- Manon Sigilla — GitHub: [@Manonsigilla](https://github.com/Manonsigilla)
- Angie Valencia — GitHub: [@angie-valencia](https://github.com/angie-valencia)
- Louis Varennes — GitHub: [@louis-varennes](https://github.com/louis-varennes)

## Licence
Libre d'utilisation, projet scolaire.

## Contact
Pour questions, suggestions ou signalement de bugs :
- Ouvrez une issue sur le dépôt : https://github.com/Manonsigilla/calculatrice-tkinter/issues
- Ou contactez les auteurs via leur profil GitHub

---

Merci d'utiliser ce projet ! Les retours et contributions sont appréciés pour
améliorer la stabilité, l'ergonomie et les fonctionnalités.
