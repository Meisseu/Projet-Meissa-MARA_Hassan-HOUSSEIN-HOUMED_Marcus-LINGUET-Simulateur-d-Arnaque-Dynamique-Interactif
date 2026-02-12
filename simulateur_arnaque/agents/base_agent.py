"""
BaseAgent - Classe de base pour tous les agents LLM
"""

from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from ..config.llm_config import OPENAI_API_KEY, OPENAI_MODEL


class BaseAgent(ABC):
    """Classe abstraite pour tous les agents"""
    
    def __init__(self, name: str, temperature: float = 0.5):
        """
        Initialiser un agent
        
        Args:
            name: Nom de l'agent
            temperature: Température du LLM (0.0 = déterministe, 1.0 = créatif)
        """
        self.name = name
        self.temperature = temperature
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name=OPENAI_MODEL,
            temperature=temperature
        )
    
    @abstractmethod
    def process(self, input_text: str) -> str:
        """Traiter une entrée et retourner une réponse"""
        pass
    
    def get_info(self) -> dict:
        """Retourner les informations de l'agent"""
        return {
            "name": self.name,
            "temperature": self.temperature,
            "model": OPENAI_MODEL
        }