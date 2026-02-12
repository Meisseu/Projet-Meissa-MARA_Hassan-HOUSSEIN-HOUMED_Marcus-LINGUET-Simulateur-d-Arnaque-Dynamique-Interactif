"""
Agent Modérateur Audience

Cet agent LLM est responsable de:
- Recevoir et filtrer les propositions de l'audience
- Éliminer les suggestions inappropriées ou hors-sujet
- Générer 3 options cohérentes avec le contexte actuel
- Évaluer la pertinence des événements perturbateurs
"""

from typing import List, Dict, Optional
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage


class ModeratorAgent:
    """
    Agent responsable de modérer et sélectionner les événements d'audience
    """
    
    def __init__(self, project_id: str = None, location: str = "us-central1", model: str = "gemini-1.5-flash"):
        """
        Initialise l'agent modérateur
        
        Args:
            project_id: Google Cloud Project ID
            location: Region Google Cloud
            model: Modèle LLM à utiliser
        """
        from ..config.llm_config import GOOGLE_PROJECT_ID
        self.llm = ChatVertexAI(
            project=project_id or GOOGLE_PROJECT_ID,
            location=location,
            model_name=model,
            temperature=0.7
        )
        
        self.system_prompt = """Tu es un modérateur d'événements pour un simulateur d'arnaque téléphonique éducatif.

Ton rôle est d'évaluer les propositions d'événements perturbateurs suggérés par l'audience et de sélectionner les 3 meilleures options.

CONTEXTE:
Une vieille dame (Mme Jeanne Dubois, 78 ans) est au téléphone avec un potentiel arnaqueur. 
L'audience peut proposer des événements du quotidien qui vont perturber la conversation et aider Jeanne à gagner du temps.

RÈGLES DE FILTRAGE:
1. REJETER toute suggestion violente, vulgaire ou inappropriée
2. REJETER les événements impossibles ou trop fantaisistes
3. PRIVILÉGIER les événements réalistes du quotidien d'une personne âgée
4. ASSURER que l'événement est cohérent avec le contexte actuel de la conversation
5. FAVORISER les événements drôles et déstabilisants pour l'arnaqueur

EXEMPLES D'ÉVÉNEMENTS APPROPRIÉS:
- Le chien (Poupoune) aboie et demande à sortir
- La sonnette de la porte retentit (facteur, livreur)
- La casserole sur le feu déborde
- Le téléphone fixe sonne (un autre appel)
- Jeanne doit prendre ses médicaments
- La voisine frappe à la fenêtre
- Le chat renverse un vase
- L'émission de télé favorite commence
- Une quinte de toux qui l'empêche de parler

EXEMPLES D'ÉVÉNEMENTS À REJETER:
- Violence physique ou verbale
- Événements sexuels ou vulgaires
- Catastrophes naturelles ou accidents graves
- Arrivée de la police ou d'autorités (trop direct)
- Tout ce qui termine la conversation brutalement
- Événements technologiques complexes (hacking, etc.)

Ta mission: Analyser les suggestions, filtrer les inappropriées, et sélectionner les 3 meilleures qui sont:
1. Réalistes et cohérentes avec le contexte
2. Potentiellement drôles ou déstabilisantes
3. Permettent de gagner du temps sans terminer la conversation
"""
    
    def filter_and_select(
        self, 
        suggestions: List[str], 
        conversation_context: str,
        current_objective: str = ""
    ) -> List[Dict[str, str]]:
        """
        Filtre les suggestions de l'audience et sélectionne les 3 meilleures
        
        Args:
            suggestions: Liste des suggestions de l'audience
            conversation_context: Résumé du contexte actuel de la conversation
            current_objective: Objectif actuel de Mme Dubois
            
        Returns:
            Liste de 3 dictionnaires contenant 'event' et 'description'
        """
        if not suggestions:
            return self._get_default_events()
        
        # Construire le prompt avec le contexte
        user_prompt = f"""CONTEXTE DE LA CONVERSATION:
{conversation_context}

OBJECTIF ACTUEL DE JEANNE:
{current_objective}

SUGGESTIONS DE L'AUDIENCE ({len(suggestions)}):
{self._format_suggestions(suggestions)}

Ta tâche:
1. Élimine toutes les suggestions inappropriées selon les règles
2. Évalue la cohérence de chaque suggestion avec le contexte
3. Sélectionne les 3 MEILLEURES suggestions
4. Pour chaque suggestion retenue, fournis une description courte (1 phrase) de l'impact

Format de réponse (IMPORTANT - Respecte exactement ce format):
1. [Nom de l'événement] - Description de l'impact (max 1 phrase)
2. [Nom de l'événement] - Description de l'impact (max 1 phrase)
3. [Nom de l'événement] - Description de l'impact (max 1 phrase)

Si moins de 3 suggestions sont appropriées, propose des événements pertinents que tu crées toi-même.
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parser la réponse
        selected_events = self._parse_response(response.content)
        
        # Assurer qu'on a bien 3 événements
        if len(selected_events) < 3:
            selected_events.extend(
                self._get_default_events()[len(selected_events):3]
            )
        
        return selected_events[:3]
    
    def _format_suggestions(self, suggestions: List[str]) -> str:
        """Formate les suggestions pour le prompt"""
        return "\n".join([f"- {s}" for s in suggestions])
    
    def _parse_response(self, response: str) -> List[Dict[str, str]]:
        """
        Parse la réponse du LLM pour extraire les événements
        
        Returns:
            Liste de dictionnaires {'event': str, 'description': str}
        """
        events = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            
            # Enlever le numéro au début (1., 2., 3.)
            line = line.split('.', 1)[1].strip() if '.' in line else line
            
            # Séparer événement et description
            if '-' in line:
                parts = line.split('-', 1)
                event = parts[0].strip().strip('[]')
                description = parts[1].strip()
            else:
                event = line
                description = "Événement perturbateur"
            
            events.append({
                'event': event,
                'description': description
            })
        
        return events
    
    def _get_default_events(self) -> List[Dict[str, str]]:
        """
        Retourne des événements par défaut si aucune suggestion valide
        """
        return [
            {
                'event': "Poupoune (le chien) aboie à la porte",
                'description': "Le chien devient insistant et Jeanne doit aller le calmer"
            },
            {
                'event': "La sonnette retentit",
                'description': "Quelqu'un est à la porte (facteur ou livreur)"
            },
            {
                'event': "Jeanne a une quinte de toux",
                'description': "Elle doit s'excuser et prendre un verre d'eau"
            }
        ]
    
    def generate_fallback_events(self, conversation_context: str) -> List[Dict[str, str]]:
        """
        Génère des événements contextuels quand l'audience ne propose rien
        
        Args:
            conversation_context: Contexte de la conversation
            
        Returns:
            3 événements générés par le LLM
        """
        prompt = f"""CONTEXTE:
{conversation_context}

Génère 3 événements réalistes et perturbants qui pourraient arriver à Jeanne Dubois pendant cet appel.
Ces événements doivent être crédibles pour une dame de 78 ans à son domicile.

Format de réponse:
1. [Nom de l'événement] - Description de l'impact
2. [Nom de l'événement] - Description de l'impact
3. [Nom de l'événement] - Description de l'impact
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        events = self._parse_response(response.content)
        
        return events[:3] if events else self._get_default_events()


def create_moderator_agent(api_key: str, model: str = "gpt-4-turbo-preview") -> ModeratorAgent:
    """
    Fonction helper pour créer un agent modérateur
    
    Args:
        api_key: Clé API OpenAI
        model: Modèle LLM à utiliser
        
    Returns:
        Instance de ModeratorAgent configurée
    """
    return ModeratorAgent(api_key=api_key, model=model)
