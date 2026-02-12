"""
Test rapide du module Director avec un script d'arnaque Microsoft Support.
"""
from simulateur_arnaque.scripts import script_loader
from simulateur_arnaque.agents import director

if __name__ == "__main__":
    # Charger le script Microsoft Support
    script = script_loader.load_script("microsoft_support")
    # Historique simulé : virus puis AnyDesk
    history = [
        {"role": "scammer", "content": "Bonjour, ici le support Microsoft, votre ordinateur a un virus !"},
        {"role": "victim", "content": "Oh non, que dois-je faire ?"},
        {"role": "scammer", "content": "Installez AnyDesk pour que je puisse vous aider."}
    ]
    update = director.analyze_conversation(history, script)
    print("--- Résultat DirectorUpdate ---")
    print(update)
    print("\n--- dynamic_context_from_director ---")
    print(update.dynamic_context_from_director)
