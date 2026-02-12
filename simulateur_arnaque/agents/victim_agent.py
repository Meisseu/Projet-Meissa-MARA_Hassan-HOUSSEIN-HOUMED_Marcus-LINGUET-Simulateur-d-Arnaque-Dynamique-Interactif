"""
VictimAgent - Agent Jeanne Dubois avec mémoire et réponses intelligentes
"""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .base_agent import BaseAgent
from .victim_prompt import get_victim_prompt
from ..config.llm_config import VICTIM_TEMPERATURE


class VictimAgent(BaseAgent):
    """Agent représentant Mme Jeanne Dubois"""
    
    def __init__(self):
        """Initialiser l'agent victime"""
        super().__init__(name="Jeanne Dubois", temperature=VICTIM_TEMPERATURE)
        
        # Mémoire conversationnelle
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Objectif courant
        self.current_objective = "Listen politely and be confused"
        self.audience_constraint = ""
        
        # Template du prompt
        self.prompt_template = PromptTemplate(
            input_variables=["chat_history", "scammer_input", "objective", "audience_constraint"],
            template=get_victim_prompt("{objective}", "{audience_constraint}") + "\n\nChat History:\n{chat_history}\n\nScammer: {scammer_input}\n\nJeanne:"
        )
        
        # Chaîne LangChain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template, memory=self.memory)
    
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
            # Générer la réponse
            response = self.chain.run(
                scammer_input=scammer_input,
                objective=self.current_objective,
                audience_constraint=self.audience_constraint
            )
            
            return response.strip()
        
        except Exception as e:
            print(f"❌ Error in VictimAgent: {e}")
            return "Oh dear... I'm sorry, I got confused. Could you repeat that please?"
    
    def reset_memory(self):
        """Réinitialiser la mémoire (nouvelle conversation)"""
        self.memory.clear()
        self.current_objective = "Listen politely and be confused"
        self.audience_constraint = ""
    
    def get_state(self) -> dict:
        """Retourner l'état courant de l'agent"""
        return {
            "name": self.name,
            "temperature": self.temperature,
            "current_objective": self.current_objective,
            "audience_constraint": self.audience_constraint,
            "memory_length": len(self.memory.buffer) if hasattr(self.memory, 'buffer') else 0
        }
    
    def process(self, input_text: str) -> str:
        """
        Méthode abstraite de BaseAgent
        Utilise respond() pour traiter l'input
        """
        return self.respond(input_text)