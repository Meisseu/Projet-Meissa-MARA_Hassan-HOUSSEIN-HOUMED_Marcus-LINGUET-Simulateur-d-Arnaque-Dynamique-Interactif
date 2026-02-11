"""
Tests unitaires pour le système d'audience (Partie 3)

Tests pour:
- ModeratorAgent
- AudienceInterface
- AudienceEventManager
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from simulateur_arnaque.agents.moderator import ModeratorAgent
from simulateur_arnaque.audience_interface import AudienceInterface, AudienceEvent
from simulateur_arnaque.audience_events import AudienceEventManager


class TestModeratorAgent:
    """Tests pour l'agent modérateur"""
    
    @pytest.fixture
    def mock_llm(self):
        """Mock du LLM pour les tests"""
        with patch('simulateur_arnaque.agents.moderator.ChatOpenAI') as mock:
            yield mock
    
    def test_moderator_initialization(self, mock_llm):
        """Test l'initialisation de l'agent modérateur"""
        moderator = ModeratorAgent(api_key="test_key", model="gpt-4-turbo-preview")
        
        assert moderator is not None
        assert moderator.system_prompt is not None
        assert "modérateur" in moderator.system_prompt.lower()
    
    def test_default_events_returned(self):
        """Test que les événements par défaut sont bien retournés"""
        moderator = ModeratorAgent(api_key="test_key")
        default_events = moderator._get_default_events()
        
        assert len(default_events) == 3
        assert all('event' in e and 'description' in e for e in default_events)
        assert "Poupoune" in default_events[0]['event']
    
    def test_parse_response_valid_format(self):
        """Test le parsing d'une réponse bien formatée"""
        moderator = ModeratorAgent(api_key="test_key")
        
        response = """1. Le chien aboie - Il demande à sortir
2. La sonnette retentit - C'est le facteur
3. Jeanne tousse - Elle a besoin d'eau"""
        
        events = moderator._parse_response(response)
        
        assert len(events) == 3
        assert events[0]['event'] == "Le chien aboie"
        assert "sortir" in events[0]['description']
    
    def test_format_suggestions(self):
        """Test le formatage des suggestions"""
        moderator = ModeratorAgent(api_key="test_key")
        suggestions = ["Event 1", "Event 2", "Event 3"]
        
        formatted = moderator._format_suggestions(suggestions)
        
        assert "- Event 1" in formatted
        assert "- Event 2" in formatted
        assert formatted.count("-") == 3


class TestAudienceInterface:
    """Tests pour l'interface audience"""
    
    def test_interface_initialization(self):
        """Test l'initialisation de l'interface"""
        interface = AudienceInterface(mode="console")
        
        assert interface.mode == "console"
        assert interface.suggestion_history == []
        assert interface.event_history == []
    
    def test_simulated_suggestions(self):
        """Test la génération de suggestions simulées"""
        interface = AudienceInterface(mode="simulated")
        suggestions = interface._get_simulated_suggestions()
        
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)
        assert any("chien" in s.lower() for s in suggestions)
    
    def test_display_options(self, capsys):
        """Test l'affichage des options"""
        interface = AudienceInterface(mode="console")
        events = [
            {'event': 'Event 1', 'description': 'Desc 1'},
            {'event': 'Event 2', 'description': 'Desc 2'},
            {'event': 'Event 3', 'description': 'Desc 3'}
        ]
        
        interface.display_options(events)
        captured = capsys.readouterr()
        
        assert "Event 1" in captured.out
        assert "Event 2" in captured.out
        assert "VOTE" in captured.out
    
    def test_vote_simulated(self):
        """Test le vote simulé"""
        interface = AudienceInterface(mode="simulated")
        events = [
            {'event': 'Event 1', 'description': 'Desc 1'},
            {'event': 'Event 2', 'description': 'Desc 2'},
            {'event': 'Event 3', 'description': 'Desc 3'}
        ]
        
        winner = interface._vote_simulated(events)
        
        assert winner in events
        assert 'event' in winner
        assert 'description' in winner
        assert len(interface.event_history) == 1
    
    def test_get_event_constraint(self):
        """Test la génération de contrainte d'événement"""
        interface = AudienceInterface()
        event = {
            'event': 'Le chien aboie',
            'description': 'Il veut sortir'
        }
        
        constraint = interface.get_event_constraint(event)
        
        assert "Le chien aboie" in constraint
        assert "sortir" in constraint
        assert "ÉVÉNEMENT" in constraint
    
    def test_audience_event_dataclass(self):
        """Test la dataclass AudienceEvent"""
        event = AudienceEvent(
            event="Test event",
            description="Test description",
            votes=42
        )
        
        assert event.event == "Test event"
        assert event.description == "Test description"
        assert event.votes == 42
        assert event.timestamp is not None


class TestAudienceEventManager:
    """Tests pour le gestionnaire d'événements"""
    
    @pytest.fixture
    def mock_moderator(self):
        """Mock de l'agent modérateur"""
        moderator = Mock(spec=ModeratorAgent)
        moderator.filter_and_select.return_value = [
            {'event': 'Event 1', 'description': 'Desc 1'},
            {'event': 'Event 2', 'description': 'Desc 2'},
            {'event': 'Event 3', 'description': 'Desc 3'}
        ]
        moderator.generate_fallback_events.return_value = [
            {'event': 'Fallback 1', 'description': 'Desc 1'},
            {'event': 'Fallback 2', 'description': 'Desc 2'},
            {'event': 'Fallback 3', 'description': 'Desc 3'}
        ]
        return moderator
    
    @pytest.fixture
    def mock_interface(self):
        """Mock de l'interface audience"""
        interface = Mock(spec=AudienceInterface)
        interface.suggestion_history = []
        interface.event_history = []
        interface.collect_suggestions.return_value = ["Suggestion 1", "Suggestion 2"]
        interface.conduct_vote.return_value = {
            'event': 'Winning Event',
            'description': 'Winning Description'
        }
        interface.get_event_constraint.return_value = "CONSTRAINT TEXT"
        return interface
    
    def test_manager_initialization(self, mock_moderator, mock_interface):
        """Test l'initialisation du gestionnaire"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface,
            vote_frequency=5
        )
        
        assert manager.moderator == mock_moderator
        assert manager.interface == mock_interface
        assert manager.vote_frequency == 5
        assert manager.turn_counter == 0
    
    def test_should_trigger_audience(self, mock_moderator, mock_interface):
        """Test le déclenchement des tours d'audience"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface,
            vote_frequency=3
        )
        
        assert not manager.should_trigger_audience()  # Turn 1
        assert not manager.should_trigger_audience()  # Turn 2
        assert manager.should_trigger_audience()      # Turn 3
        assert not manager.should_trigger_audience()  # Turn 4
        assert not manager.should_trigger_audience()  # Turn 5
        assert manager.should_trigger_audience()      # Turn 6
    
    def test_process_audience_round_with_suggestions(self, mock_moderator, mock_interface):
        """Test le traitement d'un tour avec suggestions"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface
        )
        
        constraint = manager.process_audience_round(
            conversation_context="Test context",
            current_objective="Test objective",
            collect_mode="simulated",
            vote_mode="simulated"
        )
        
        assert constraint is not None
        assert constraint == "CONSTRAINT TEXT"
        assert mock_interface.collect_suggestions.called
        assert mock_moderator.filter_and_select.called
        assert mock_interface.conduct_vote.called
    
    def test_process_audience_round_without_suggestions(self, mock_moderator, mock_interface):
        """Test le traitement d'un tour sans suggestions"""
        mock_interface.collect_suggestions.return_value = []
        
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface
        )
        
        constraint = manager.process_audience_round(
            conversation_context="Test context",
            collect_mode="simulated",
            vote_mode="simulated"
        )
        
        assert constraint is not None
        assert mock_moderator.generate_fallback_events.called
    
    def test_get_current_constraint(self, mock_moderator, mock_interface):
        """Test la récupération de la contrainte actuelle"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface
        )
        
        # Avant traitement
        assert manager.get_current_constraint() is None
        
        # Après traitement
        manager.process_audience_round(
            conversation_context="Test",
            collect_mode="none",
            vote_mode="simulated"
        )
        assert manager.get_current_constraint() is not None
    
    def test_clear_constraint(self, mock_moderator, mock_interface):
        """Test l'effacement de la contrainte"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface
        )
        
        manager.process_audience_round(
            conversation_context="Test",
            collect_mode="none",
            vote_mode="simulated"
        )
        
        assert manager.get_current_constraint() is not None
        manager.clear_constraint()
        assert manager.get_current_constraint() is None
    
    def test_get_statistics(self, mock_moderator, mock_interface):
        """Test la récupération des statistiques"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface
        )
        
        manager.turn_counter = 5
        manager.last_event = {'event': 'Test', 'description': 'Test'}
        
        stats = manager.get_statistics()
        
        assert stats['total_turns'] == 5
        assert stats['last_event'] is not None
        assert 'total_suggestions' in stats
        assert 'total_events' in stats
    
    def test_reset(self, mock_moderator, mock_interface):
        """Test la réinitialisation du gestionnaire"""
        manager = AudienceEventManager(
            moderator=mock_moderator,
            interface=mock_interface
        )
        
        manager.turn_counter = 10
        manager.current_constraint = "TEST"
        manager.last_event = {'test': 'data'}
        
        manager.reset()
        
        assert manager.turn_counter == 0
        assert manager.current_constraint is None
        assert manager.last_event is None


class TestIntegration:
    """Tests d'intégration pour le système complet"""
    
    @patch('simulateur_arnaque.agents.moderator.ChatOpenAI')
    def test_full_audience_flow_simulated(self, mock_openai):
        """Test le flux complet en mode simulé"""
        # Configuration du mock LLM
        mock_response = Mock()
        mock_response.content = """1. Le chien aboie - Il veut sortir
2. La sonnette retentit - C'est le facteur
3. Jeanne tousse - Elle a besoin d'eau"""
        
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_openai.return_value = mock_llm_instance
        
        # Créer le gestionnaire complet
        from simulateur_arnaque.audience_events import create_audience_manager
        
        manager = create_audience_manager(
            api_key="test_key",
            interface_mode="simulated",
            vote_frequency=3
        )
        
        # Simuler quelques tours
        assert not manager.should_trigger_audience()  # Turn 1
        assert not manager.should_trigger_audience()  # Turn 2
        
        # Tour 3: Événement audience
        if manager.should_trigger_audience():
            constraint = manager.process_audience_round(
                conversation_context="L'arnaqueur demande accès à l'ordinateur",
                current_objective="Résister poliment",
                collect_mode="simulated",
                vote_mode="simulated"
            )
            
            assert constraint is not None
            assert isinstance(constraint, str)
            assert len(constraint) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
