"""
Module de gestion des événements audience

Coordonne l'interaction entre l'interface audience et l'agent modérateur
pour créer des événements perturbateurs cohérents
"""

from typing import List, Dict, Optional
from .agents.moderator import ModeratorAgent
from .audience_interface import AudienceInterface


class AudienceEventManager:
    """
    Gestionnaire central pour orchestrer les événements d'audience
    """
    
    def __init__(
        self,
        moderator: ModeratorAgent,
        interface: AudienceInterface,
        vote_frequency: int = 5
    ):
        """
        Initialise le gestionnaire d'événements audience
        
        Args:
            moderator: Agent modérateur pour filtrer les suggestions
            interface: Interface pour interagir avec l'audience
            vote_frequency: Fréquence d'activation (tous les X tours)
        """
        self.moderator = moderator
        self.interface = interface
        self.vote_frequency = vote_frequency
        self.turn_counter = 0
        self.current_constraint: Optional[str] = None
        self.last_event: Optional[Dict[str, str]] = None
    
    def should_trigger_audience(self) -> bool:
        """
        Détermine si c'est le moment de déclencher un événement audience
        
        Returns:
            True si c'est le tour pour un événement
        """
        self.turn_counter += 1
        return self.turn_counter % self.vote_frequency == 0
    
    def process_audience_round(
        self,
        conversation_context: str,
        current_objective: str = "",
        collect_mode: str = "console",
        vote_mode: str = "simulated"
    ) -> Optional[str]:
        """
        Gère un tour complet d'interaction avec l'audience
        
        Args:
            conversation_context: Contexte actuel de la conversation
            current_objective: Objectif actuel de Mme Dubois
            collect_mode: Mode de collecte des suggestions
            vote_mode: Mode de vote
            
        Returns:
            Contrainte à injecter dans le prompt de la victime, ou None
        """
        print("\n" + "🎬"*30)
        print("PAUSE AUDIENCE - Événement perturbateur!")
        print("🎬"*30 + "\n")
        
        # Étape 1: Collecter les suggestions
        if collect_mode != "none":
            self.interface.mode = collect_mode
            suggestions = self.interface.collect_suggestions(max_suggestions=10)
        else:
            suggestions = []
        
        # Étape 2: Le modérateur filtre et sélectionne 3 options
        if suggestions:
            selected_events = self.moderator.filter_and_select(
                suggestions=suggestions,
                conversation_context=conversation_context,
                current_objective=current_objective
            )
        else:
            # Si pas de suggestions, générer des événements contextuels
            selected_events = self.moderator.generate_fallback_events(
                conversation_context=conversation_context
            )
        
        # Étape 3: Vote de l'audience
        winning_event = self.interface.conduct_vote(
            events=selected_events,
            mode=vote_mode
        )
        
        # Étape 4: Convertir en contrainte pour l'agent victime
        self.current_constraint = self.interface.get_event_constraint(winning_event)
        self.last_event = winning_event
        
        return self.current_constraint
    
    def get_current_constraint(self) -> Optional[str]:
        """
        Récupère la contrainte actuelle (événement en cours)
        
        Returns:
            Contrainte textuelle ou None si pas d'événement actif
        """
        return self.current_constraint
    
    def clear_constraint(self) -> None:
        """
        Efface la contrainte actuelle après son utilisation
        """
        self.current_constraint = None
    
    def get_statistics(self) -> Dict:
        """
        Retourne des statistiques sur les événements audience
        
        Returns:
            Dictionnaire avec les statistiques
        """
        return {
            'total_turns': self.turn_counter,
            'total_suggestions': len(self.interface.suggestion_history),
            'total_events': len(self.interface.event_history),
            'last_event': self.last_event
        }
    
    def reset(self) -> None:
        """
        Réinitialise le gestionnaire pour une nouvelle session
        """
        self.turn_counter = 0
        self.current_constraint = None
        self.last_event = None


def create_audience_manager(
    api_key: str,
    interface_mode: str = "console",
    vote_frequency: int = 5,
    model: str = "gpt-4-turbo-preview"
) -> AudienceEventManager:
    """
    Fonction helper pour créer un gestionnaire d'événements audience complet
    
    Args:
        api_key: Clé API OpenAI
        interface_mode: Mode d'interface ('console', 'simulated', 'web')
        vote_frequency: Fréquence d'activation des événements (tous les X tours)
        model: Modèle LLM pour le modérateur
        
    Returns:
        Instance d'AudienceEventManager configurée
    """
    from .agents.moderator import create_moderator_agent
    from .audience_interface import create_audience_interface
    
    moderator = create_moderator_agent(api_key=api_key, model=model)
    interface = create_audience_interface(mode=interface_mode)
    
    return AudienceEventManager(
        moderator=moderator,
        interface=interface,
        vote_frequency=vote_frequency
    )


# Exemples d'événements prédéfinis pour inspiration
DEFAULT_EVENTS = [
    {
        'event': "Poupoune (le chien) aboie frénétiquement",
        'description': "Le chien veut sortir ou réagit à quelqu'un dehors"
    },
    {
        'event': "La sonnette de la porte retentit",
        'description': "Facteur, livreur, ou voisin à la porte"
    },
    {
        'event': "Jeanne a une quinte de toux",
        'description': "Elle doit s'excuser et prendre un verre d'eau"
    },
    {
        'event': "Le téléphone portable sonne",
        'description': "Un autre appel arrive, probablement sa famille"
    },
    {
        'event': "La casserole sur le feu déborde",
        'description': "Jeanne doit aller éteindre le feu d'urgence"
    },
    {
        'event': "L'émission favorite de Jeanne commence",
        'description': "Les Feux de l'Amour, elle est distraite"
    },
    {
        'event': "Jeanne doit prendre ses médicaments",
        'description': "C'est l'heure de sa médication quotidienne"
    },
    {
        'event': "Le chat renverse un vase",
        'description': "Grand bruit et Jeanne doit nettoyer"
    },
    {
        'event': "La voisine frappe à la fenêtre",
        'description': "Elle veut emprunter quelque chose"
    },
    {
        'event': "Jeanne ne trouve plus ses lunettes",
        'description': "Elle ne peut plus lire ce que demande l'arnaqueur"
    }
]
