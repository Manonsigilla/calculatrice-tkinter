# src/main.py
"""
Point d'entrée principal de l'application calculatrice.
Lance l'interface graphique. 
"""

from src.interface import CalculatriceGUI


def main():
    """
    Fonction principale qui lance l'application. 
    """
    # Créer l'application
    app = CalculatriceGUI()
    # Lancer la boucle principale
    app.run()  # ← Utilise . run() au lieu de .mainloop()


if __name__ == "__main__": 
    main()