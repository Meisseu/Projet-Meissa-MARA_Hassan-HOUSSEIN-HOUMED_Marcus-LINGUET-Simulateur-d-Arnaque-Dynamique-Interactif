"""
VictimAgent - Agent Jeanne Dubois avec mémoire et réponses intelligentes
"""

from .base_agent import BaseAgent
from .victim_prompt import get_victim_prompt
from ..config.llm_config import VICTIM_TEMPERATURE


class VictimAgent(BaseAgent):
    """Agent représentant Mme Jeanne Dubois"""
    
    def __init__(self):
        """Initialiser l'agent victime"""
        super().__init__(name="Jeanne Dubois", temperature=VICTIM_TEMPERATURE)
        
        # Mémoire conversationnelle (simple liste de messages)
        self.chat_history = []
        
        # Objectif courant
        self.current_objective = "Listen politely and be confused"
        self.audience_constraint = ""
        
    def _format_history(self) -> str:
        """Formater l'historique de conversation"""
        if not self.chat_history:
            return ""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history])
    
    def respond(self, scammer_input: str, objective: str = None, audience_constraint: str = "") -> str:
        """
        Générer une réponse de Jeanne
        
        Args:
            scammer_input: Ce que l'arnaqueur a dit
            objective: Objectif tactique courant
            audience_constraint: Contrainte du public (optionnel)
        
        Returns:
            str: Réponse de Jeanne
        """
        # Mettre à jour les objectifs si fournis
        if objective:
            self.current_objective = objective
        if audience_constraint:
            self.audience_constraint = audience_constraint
        
        try:
            # Construire le prompt complet
            history_text = self._format_history()
            full_prompt = get_victim_prompt(self.current_objective, self.audience_constraint)
            
            if history_text:
                full_prompt += f"\n\nChat History:\n{history_text}"
            
            full_prompt += f"\n\nScammer: {scammer_input}\n\nJeanne:"
            
            # Générer la réponse avec le LLM
            response = self.llm.invoke(full_prompt).content
            
            # Sauvegarder dans l'historique
            self.chat_history.append({"role": "Scammer", "content": scammer_input})
            self.chat_history.append({"role": "Jeanne", "content": response})
            
            return response.strip()
        
        except Exception as e:
            print(f"❌ Error in VictimAgent: {e}")
            return "Oh dear... I'm sorry, I got confused. Could you repeat that please?"
    
    def reset_memory(self):
        """Réinitialiser la mémoire (nouvelle conversation)"""
        self.chat_history = []
        self.current_objective = "Listen politely and be confused"
        self.audience_constraint = ""
    
    def get_state(self) -> dict:
        """Retourner l'état courant de l'agent"""
        return {
            "name": self.name,
            "temperature": self.temperature,
            "current_objective": self.current_objective,
            "audience_constraint": self.audience_constraint,
            "memory_length": len(self.chat_history)
        }
    
    def process(self, input_text: str) -> str:
        """
        Méthode abstraite de BaseAgent
        Utilise respond() pour traiter l'input
        """
        return self.respond(input_text)