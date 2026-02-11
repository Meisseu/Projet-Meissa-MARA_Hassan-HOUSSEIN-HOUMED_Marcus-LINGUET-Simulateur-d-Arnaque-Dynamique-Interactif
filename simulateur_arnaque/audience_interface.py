"""
Interface Audience

Module pour gérer l'interaction avec l'audience:
- Collecte des suggestions
- Affichage des options
- Gestion du vote
- Interface console et web (optionnel)
"""

from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class AudienceEvent:
    """Représente un événement proposé ou sélectionné"""
    event: str
    description: str
    votes: int = 0
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class AudienceInterface:
    """
    Gère l'interaction avec l'audience pour les suggestions et votes
    """
    
    def __init__(self, mode: str = "console"):
        """
        Initialise l'interface audience
        
        Args:
            mode: Type d'interface ('console', 'web', 'simulated')
        """
        self.mode = mode
        self.suggestion_history: List[str] = []
        self.event_history: List[AudienceEvent] = []
        
    def collect_suggestions(self, max_suggestions: int = 10, timeout: int = 30) -> List[str]:
        """
        Collecte les suggestions de l'audience
        
        Args:
            max_suggestions: Nombre maximum de suggestions à collecter
            timeout: Temps limite en secondes (non implémenté en mode console)
            
        Returns:
            Liste des suggestions collectées
        """
        if self.mode == "console":
            return self._collect_console_suggestions(max_suggestions)
        elif self.mode == "simulated":
            return self._get_simulated_suggestions()
        else:
            # Mode web à implémenter avec Streamlit
            raise NotImplementedError("Mode web pas encore implémenté")
    
    def _collect_console_suggestions(self, max_suggestions: int) -> List[str]:
        """
        Collecte les suggestions via la console
        """
        print("\n" + "="*60)
        print("🎭 AUDIENCE PARTICIPATION 🎭")
        print("="*60)
        print(f"\nProposez des événements perturbateurs pour aider Mme Dubois!")
        print(f"Maximum {max_suggestions} suggestions.")
        print("Tapez 'fin' pour terminer la collecte.\n")
        
        suggestions = []
        
        for i in range(max_suggestions):
            try:
                suggestion = input(f"Suggestion {i+1}: ").strip()
                
                if suggestion.lower() in ['fin', 'stop', 'exit', '']:
                    break
                
                if suggestion:
                    suggestions.append(suggestion)
                    self.suggestion_history.append(suggestion)
                    print(f"✓ Suggestion enregistrée!")
                
            except (KeyboardInterrupt, EOFError):
                print("\n\nCollecte interrompue.")
                break
        
        print(f"\n✓ {len(suggestions)} suggestion(s) collectée(s).")
        return suggestions
    
    def _get_simulated_suggestions(self) -> List[str]:
        """
        Retourne des suggestions simulées pour les tests/démos
        """
        simulated = [
            "Le chien se met à aboyer comme un fou",
            "La sonnette retentit - c'est le facteur",
            "Jeanne renverse son café sur elle",
            "Le téléphone portable de Jeanne sonne",
            "Un voisin crie pour demander de l'aide",
            "La télévision se met en route toute seule",
            "Jeanne doit aller aux toilettes d'urgence",
            "Le minuteur du four sonne",
        ]
        print("\n[MODE SIMULÉ] Utilisation de suggestions pré-définies")
        return simulated
    
    def display_options(self, events: List[Dict[str, str]]) -> None:
        """
        Affiche les options sélectionnées par le modérateur
        
        Args:
            events: Liste des événements sélectionnés
        """
        print("\n" + "="*60)
        print("📊 VOTE - Choisissez l'événement qui va se produire!")
        print("="*60)
        
        for i, event in enumerate(events, 1):
            print(f"\n{i}. {event['event']}")
            print(f"   → {event['description']}")
    
    def conduct_vote(self, events: List[Dict[str, str]], mode: str = "simulated") -> Dict[str, str]:
        """
        Organise un vote pour sélectionner l'événement
        
        Args:
            events: Liste des événements à voter
            mode: 'console' (vote manuel), 'simulated' (vote aléatoire), 'web' (futur)
            
        Returns:
            Événement gagnant
        """
        if mode == "console":
            return self._vote_console(events)
        elif mode == "simulated":
            return self._vote_simulated(events)
        else:
            raise NotImplementedError(f"Mode de vote '{mode}' pas encore implémenté")
    
    def _vote_console(self, events: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Vote via la console (un seul votant pour démo)
        """
        self.display_options(events)
        
        while True:
            try:
                choice = input("\n🗳️  Votre vote (1-3): ").strip()
                
                if choice.isdigit() and 1 <= int(choice) <= len(events):
                    selected_index = int(choice) - 1
                    winner = events[selected_index]
                    
                    print(f"\n✓ Événement sélectionné: {winner['event']}")
                    
                    # Enregistrer dans l'historique
                    audience_event = AudienceEvent(
                        event=winner['event'],
                        description=winner['description'],
                        votes=1
                    )
                    self.event_history.append(audience_event)
                    
                    return winner
                else:
                    print("❌ Choix invalide. Entrez un nombre entre 1 et 3.")
                    
            except (KeyboardInterrupt, EOFError):
                print("\n\nVote annulé. Sélection par défaut.")
                return events[0]
    
    def _vote_simulated(self, events: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Simule un vote (utile pour tests et démos automatiques)
        """
        import random
        
        # Simuler des votes avec une distribution aléatoire
        votes = [random.randint(10, 100) for _ in events]
        winner_index = votes.index(max(votes))
        winner = events[winner_index]
        
        print("\n[MODE SIMULÉ] Résultats du vote:")
        for i, (event, vote_count) in enumerate(zip(events, votes), 1):
            marker = "🏆" if i-1 == winner_index else "  "
            print(f"{marker} {i}. {event['event']}: {vote_count} votes")
        
        print(f"\n✓ Événement gagnant: {winner['event']}")
        
        # Enregistrer dans l'historique
        audience_event = AudienceEvent(
            event=winner['event'],
            description=winner['description'],
            votes=max(votes)
        )
        self.event_history.append(audience_event)
        
        return winner
    
    def get_event_constraint(self, event: Dict[str, str]) -> str:
        """
        Convertit l'événement en contrainte textuelle pour l'agent victime
        
        Args:
            event: Événement sélectionné
            
        Returns:
            Contrainte textuelle à injecter dans le prompt
        """
        constraint = f"""ÉVÉNEMENT PERTURBATEUR (AUDIENCE):
{event['event']}

Conséquence: {event['description']}

Tu DOIS intégrer cet événement dans ta prochaine réponse de manière naturelle.
Utilise cet événement pour gagner du temps et déstabiliser l'arnaqueur."""
        
        return constraint
    
    def save_history(self, filepath: str = "logs/audience_history.json") -> None:
        """
        Sauvegarde l'historique des suggestions et événements
        
        Args:
            filepath: Chemin du fichier de sauvegarde
        """
        import os
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        history_data = {
            'suggestions': self.suggestion_history,
            'events': [
                {
                    'event': e.event,
                    'description': e.description,
                    'votes': e.votes,
                    'timestamp': e.timestamp.isoformat() if e.timestamp else None
                }
                for e in self.event_history
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Historique sauvegardé dans {filepath}")


def create_audience_interface(mode: str = "console") -> AudienceInterface:
    """
    Fonction helper pour créer une interface audience
    
    Args:
        mode: Type d'interface ('console', 'web', 'simulated')
        
    Returns:
        Instance d'AudienceInterface configurée
    """
    return AudienceInterface(mode=mode)
