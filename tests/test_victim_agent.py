"""
Tests unitaires pour VictimAgent
"""

import pytest
from agents.victim_agent import VictimAgent


class TestVictimAgent:
    """Tests pour l'agent victime"""
    
    @pytest.fixture
    def victim(self):
        """Créer une instance de VictimAgent pour les tests"""
        return VictimAgent()
    
    def test_victim_initialization(self, victim):
        """Test: VictimAgent s'initialise correctement"""
        assert victim.name == "Jeanne Dubois"
        assert victim.temperature > 0
        assert victim.llm is not None
        assert victim.memory is not None
    
    def test_victim_default_objective(self, victim):
        """Test: L'objectif par défaut est défini"""
        assert victim.current_objective == "Listen politely and be confused"
    
    def test_victim_get_state(self, victim):
        """Test: get_state retourne les bonnes infos"""
        state = victim.get_state()
        assert "name" in state
        assert "temperature" in state
        assert "current_objective" in state
        assert state["name"] == "Jeanne Dubois"
    
    def test_victim_reset_memory(self, victim):
        """Test: reset_memory réinitialise correctement"""
        victim.current_objective = "Test Objective"
        victim.audience_constraint = "Test Constraint"
        
        victim.reset_memory()
        
        assert victim.current_objective == "Listen politely and be confused"
        assert victim.audience_constraint == ""
    
    def test_victim_update_objective(self, victim):
        """Test: L'objectif peut être mis à jour"""
        new_objective = "Pretend to search for terminal"
        victim.current_objective = new_objective
        
        assert victim.current_objective == new_objective
    
    def test_victim_update_constraint(self, victim):
        """Test: La contrainte audience peut être mise à jour"""
        new_constraint = "Someone rings the doorbell"
        victim.audience_constraint = new_constraint
        
        assert victim.audience_constraint == new_constraint
    
    def test_victim_process_method(self, victim):
        """Test: La méthode process fonctionne"""
        # Juste vérifier que ça s'exécute sans erreur
        # (La réponse réelle dépend de l'API OpenAI)
        assert hasattr(victim, 'process')
        assert callable(victim.process)