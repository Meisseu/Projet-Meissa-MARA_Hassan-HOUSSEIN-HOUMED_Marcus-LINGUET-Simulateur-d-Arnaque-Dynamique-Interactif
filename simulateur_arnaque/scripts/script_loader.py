"""
Module de chargement de scripts d'arnaque.
"""
import json
import os

def load_script(script_id):
    """Charge un script d'arnaque à partir d'un fichier JSON."""
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, f"{script_id}.json")
    with open(script_path, "r", encoding="utf-8") as f:
        return json.load(f)
