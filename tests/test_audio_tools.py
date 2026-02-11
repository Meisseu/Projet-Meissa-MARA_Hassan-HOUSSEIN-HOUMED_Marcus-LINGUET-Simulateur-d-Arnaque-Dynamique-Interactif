"""
Tests unitaires pour Audio Tools
"""

import pytest
from tools.audio_tools import AudioEffectsManager, get_audio_tools, get_audio_manager


class TestAudioEffectsManager:
    """Tests pour le gestionnaire d'effets audio"""
    
    @pytest.fixture
    def audio_manager(self):
        """Créer une instance pour les tests"""
        manager = AudioEffectsManager()
        manager.clear_log()
        return manager
    
    def test_audio_manager_initialization(self, audio_manager):
        """Test: AudioEffectsManager s'initialise correctement"""
        assert audio_manager.effects_log == []
    
    def test_play_dog_bark(self):
        """Test: play_dog_bark retourne le bon marqueur"""
        result = AudioEffectsManager.play_dog_bark()
        assert "DOG_BARKING" in result
        assert "SOUND:" in result
    
    def test_play_cough(self):
        """Test: play_cough retourne le bon marqueur"""
        result = AudioEffectsManager.play_cough()
        assert "COUGHING" in result
        assert "SOUND:" in result
    
    def test_play_doorbell(self):
        """Test: play_doorbell retourne le bon marqueur"""
        result = AudioEffectsManager.play_doorbell()
        assert "DOORBELL" in result
        assert "SOUND:" in result
    
    def test_play_tv_background(self):
        """Test: play_tv_background retourne le bon marqueur"""
        result = AudioEffectsManager.play_tv_background()
        assert "TV_BACKGROUND" in result
        assert "SOUND:" in result
    
    def test_play_phone_ring(self):
        """Test: play_phone_ring retourne le bon marqueur"""
        result = AudioEffectsManager.play_phone_ring()
        assert "PHONE_RINGING" in result
        assert "SOUND:" in result
    
    def test_play_cat_meow(self):
        """Test: play_cat_meow retourne le bon marqueur"""
        result = AudioEffectsManager.play_cat_meow()
        assert "CAT_MEOWING" in result
        assert "SOUND:" in result
    
    def test_log_sound(self, audio_manager):
        """Test: log_sound enregistre correctement"""
        audio_manager.log_sound("dog_bark")
        assert len(audio_manager.effects_log) == 1
        assert audio_manager.effects_log[0]["sound"] == "dog_bark"
    
    def test_clear_log(self, audio_manager):
        """Test: clear_log vide le log"""
        audio_manager.log_sound("dog_bark")
        audio_manager.clear_log()
        assert audio_manager.effects_log == []
    
    def test_get_audio_tools(self):
        """Test: get_audio_tools retourne une liste"""
        tools = get_audio_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
    
    def test_get_audio_manager(self):
        """Test: get_audio_manager retourne une instance"""
        manager = get_audio_manager()
        assert isinstance(manager, AudioEffectsManager)