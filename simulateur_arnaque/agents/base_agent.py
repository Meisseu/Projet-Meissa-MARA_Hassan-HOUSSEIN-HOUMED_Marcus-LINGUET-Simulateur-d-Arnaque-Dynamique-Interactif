"""
BaseAgent - Classe de base pour tous les agents LLM
"""

from abc import ABC, abstractmethod
from langchain_google_vertexai import ChatVertexAI
from google.oauth2 import service_account
from ..config.llm_config import GOOGLE_PROJECT_ID, GOOGLE_LOCATION, GOOGLE_MODEL, GOOGLE_CREDENTIALS
import os


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
        
        # Charger les credentials explicitement avec le bon scope
        credentials = None
        if os.path.exists(GOOGLE_CREDENTIALS):
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        
        self.llm = ChatVertexAI(
            project=GOOGLE_PROJECT_ID,
            location=GOOGLE_LOCATION,
            model_name=GOOGLE_MODEL,
            temperature=temperature,
            credentials=credentials
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