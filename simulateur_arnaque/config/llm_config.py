"""
Configuration LLM - Paramètres centralisés pour tous les agents
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ===== Configuration OpenAI =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# ===== Paramètres des Agents =====
# Température contrôle la "créativité" du LLM
VICTIM_TEMPERATURE = float(os.getenv("VICTIM_TEMPERATURE", 0.8))  # Haute = plus créatif/imprévisible
DIRECTOR_TEMPERATURE = float(os.getenv("DIRECTOR_TEMPERATURE", 0.3))  # Basse = plus logique/déterministe

# ===== Paramètres de l'Application =====
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ===== Paramètres du Simulateur =====
AUDIENCE_VOTE_FREQUENCY = int(os.getenv("AUDIENCE_VOTE_FREQUENCY", 5))  # Vote tous les X tours
MAX_CONVERSATION_TURNS = int(os.getenv("MAX_CONVERSATION_TURNS", 50))
ENABLE_AUDIO_EFFECTS = os.getenv("ENABLE_AUDIO_EFFECTS", "true").lower() == "true"

# ===== Chemins =====
AUDIO_DIRECTORY = os.getenv("AUDIO_DIRECTORY", "simulateur_arnaque/audio")
LOGS_DIRECTORY = os.getenv("LOGS_DIRECTORY", "logs")

# ===== Validation =====
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY non définie dans .env")