"""
Agents Package - Contient tous les agents LLM du simulateur

Agents disponibles:
- BaseAgent: Classe de base pour tous les agents
- VictimAgent: Mme Jeanne Dubois (victime)
- ModeratorAgent: Modérateur d'événements audience
"""

from .base_agent import BaseAgent
from .victim_agent import VictimAgent
from .moderator import ModeratorAgent

__all__ = ["BaseAgent", "VictimAgent", "ModeratorAgent"]