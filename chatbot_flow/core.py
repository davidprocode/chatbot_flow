"""
Módulo principal que implementa a classe Chatbot.
"""

import logging
from typing import Dict, Any, Optional, List, Callable

from .flow_manager import FlowManager
from .exceptions import FlowError, InvalidStateError

logger = logging.getLogger(__name__)


class Chatbot:
    """
    Classe principal para gerenciar um chatbot baseado em fluxos de conversa.
    
    Attributes:
        flow_manager (FlowManager): Gerenciador do fluxo de conversa
        context (Dict[str, Any]): Contexto da conversa atual
        current_state (str): Estado atual do chatbot no fluxo
        history (List[Dict]): Histórico da conversa
    """
    
    def __init__(self, flow_definition: Dict[str, Any], initial_state: str = "start"):
        """
        Inicializa um novo chatbot com um fluxo de conversa definido.
        
        Args:
            flow_definition: Definição do fluxo em formato JSON/dicionário
            initial_state: Estado inicial do fluxo
        """
        self.flow_manager = FlowManager(flow_definition)
        self.context = {}
        self.current_state = initial_state
        self.history = []
        
        # Validar o estado inicial
        if not self.flow_manager.state_exists(initial_state):
            raise InvalidStateError(f"Estado inicial '{initial_state}' não existe no fluxo")
        
        logger.info(f"Chatbot inicializado com estado '{initial_state}'")
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Processa uma mensagem do usuário e retorna uma resposta.
        
        Args:
            message: Mensagem do usuário
        
        Returns:
            Resposta do chatbot contendo texto e metadados
        """
        # Registrar a mensagem no histórico
        self.history.append({
            "role": "user",
            "message": message,
            "state": self.current_state
        })
        
        # Determinar a próxima transição com base na mensagem
        next_state, response_data = self.flow_manager.determine_transition(
            self.current_state, 
            message, 
            self.context
        )
        
        # Atualizar o estado atual
        previous_state = self.current_state
        self.current_state = next_state
        
        # Registrar a resposta no histórico
        self.history.append({
            "role": "bot",
            "message": response_data["text"],
            "state": next_state,
            "from_state": previous_state
        })
        
        logger.debug(f"Transição: {previous_state} -> {next_state}")
        
        return response_data
    
    def reset(self, initial_state: str = "start") -> None:
        """
        Reinicia o chatbot para o estado inicial.
        
        Args:
            initial_state: Estado inicial (opcional)
        """
        self.current_state = initial_state
        self.context = {}
        logger.info(f"Chatbot reiniciado para o estado '{initial_state}'")
    
    def save_state(self) -> Dict[str, Any]:
        """
        Salva o estado atual do chatbot.
        
        Returns:
            Estado atual serializado
        """
        return {
            "current_state": self.current_state,
            "context": self.context,
            "history": self.history
        }
    
    def load_state(self, state_data: Dict[str, Any]) -> None:
        """
        Carrega um estado previamente salvo.
        
        Args:
            state_data: Estado serializado a ser carregado
        """
        self.current_state = state_data.get("current_state", "start")
        self.context = state_data.get("context", {})
        self.history = state_data.get("history", [])
        logger.info(f"Estado carregado. Estado atual: '{self.current_state}'")
    
    def register_hook(self, event_name: str, callback: Callable) -> None:
        """
        Registra um hook para eventos específicos.
        
        Args:
            event_name: Nome do evento ('before_transition', 'after_transition', etc)
            callback: Função de callback a ser chamada
        """
        self.flow_manager.register_hook(event_name, callback)
