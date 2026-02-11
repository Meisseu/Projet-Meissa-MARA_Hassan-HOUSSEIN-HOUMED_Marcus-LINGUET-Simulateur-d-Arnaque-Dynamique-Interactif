"""
Config Package - Configuration centralisée de l'application

Modules:
- llm_config: Configuration LLM et paramètres globaux
"""

from config.llm_config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    VICTIM_TEMPERATURE,
    DIRECTOR_TEMPERATURE,
    DEBUG_MODE
)

__all__ = [
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "VICTIM_TEMPERATURE",
    "DIRECTOR_TEMPERATURE",
    "DEBUG_MODE"
]