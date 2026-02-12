"""
Tools Package - Contient tous les outils pour les agents

Tools disponibles:
- AudioEffectsManager: Gère les effets sonores
- Audio tools: play_dog_bark, play_cough, play_doorbell, etc.
"""

from .audio_tools import AudioEffectsManager, get_audio_tools, get_audio_manager

__all__ = ["AudioEffectsManager", "get_audio_tools", "get_audio_manager"]