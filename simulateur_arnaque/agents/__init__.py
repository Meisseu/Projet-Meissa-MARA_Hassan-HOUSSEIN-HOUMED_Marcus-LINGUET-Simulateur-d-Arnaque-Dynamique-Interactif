"""
Agents Package - Contient tous les agents LLM du simulateur

Agents disponibles:
- BaseAgent: Classe de base pour tous les agents
- VictimAgent: Mme Jeanne Dubois (victime)
"""

from agents.base_agent import BaseAgent
from agents.victim_agent import VictimAgent

__all__ = ["BaseAgent", "VictimAgent"]