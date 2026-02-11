"""
Audio Tools - Outils audio pour créer des bruitages contextuels
"""

from langchain.tools import tool
from datetime import datetime
import json


class AudioEffectsManager:
    """Gestionnaire des effets sonores"""
    
    def __init__(self):
        """Initialiser le gestionnaire d'audio"""
        self.effects_log = []
    
    @tool
    def play_dog_bark():
        """Poupoune le chien aboie - à utiliser quand l'arnaqueur est pressant"""
        return "[SOUND: DOG_BARKING - Scooty is barking urgently]"
    
    @tool
    def play_cough():
        """Jeanne a une quinte de toux - interrompt la conversation"""
        return "[SOUND: COUGHING - A 10-second coughing fit]"
    
    @tool
    def play_doorbell():
        """La sonnette sonne - quelqu'un à la porte"""
        return "[SOUND: DOORBELL - Ding dong! Someone at the door]"
    
    @tool
    def play_tv_background():
        """La télé joue en arrière-plan - 'Les Feux de l'Amour'"""
        return "[SOUND: TV_BACKGROUND - TV volume increases, 'Les Feux de l'Amour' is playing]"
    
    @tool
    def play_phone_ring():
        """Le téléphone sonne"""
        return "[SOUND: PHONE_RINGING - Her landline phone is ringing]"
    
    @tool
    def play_cat_meow():
        """Fluffy le chat miaule"""
        return "[SOUND: CAT_MEOWING - Fluffy the cat is meowing]"
    
    def log_sound(self, sound_name: str):
        """Enregistrer un effet sonore"""
        self.effects_log.append({
            "timestamp": datetime.now().isoformat(),
            "sound": sound_name
        })
    
    def get_log(self) -> list:
        """Obtenir le log des sons"""
        return self.effects_log
    
    def clear_log(self):
        """Effacer le log"""
        self.effects_log = []
    
    def export_log(self, filename: str = "audio_log.json"):
        """Exporter le log en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.effects_log, f, indent=2, ensure_ascii=False)


# Instance globale
audio_manager = AudioEffectsManager()

# Tools exportables pour LangChain
AUDIO_TOOLS = [
    AudioEffectsManager.play_dog_bark,
    AudioEffectsManager.play_cough,
    AudioEffectsManager.play_doorbell,
    AudioEffectsManager.play_tv_background,
    AudioEffectsManager.play_phone_ring,
    AudioEffectsManager.play_cat_meow,
]


def get_audio_tools():
    """Retourner la liste des tools audio"""
    return AUDIO_TOOLS


def get_audio_manager():
    """Retourner l'instance du gestionnaire audio"""
    return audio_manager