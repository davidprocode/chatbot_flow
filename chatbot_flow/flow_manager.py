"""
Módulo para gerenciar o fluxo de conversa do chatbot.
"""

import json
import logging
import re
from typing import Dict, Any, Tuple, List, Callable, Optional

from .exceptions import FlowValidationError, InvalidStateError, InvalidTransitionError

logger = logging.getLogger(__name__)


class FlowManager:
    """
    Gerencia o fluxo de conversa do chatbot com base em uma definição JSON.
    
    Attributes:
        flow_definition (Dict): Definição completa do fluxo
        states (Dict): Estados disponíveis no fluxo
        hooks (Dict): Callbacks registrados para eventos
    """
    
    def __init__(self, flow_definition: Dict[str, Any]):
        """
        Inicializa o gerenciador de fluxo.
        
        Args:
            flow_definition: Definição do fluxo em formato JSON/dicionário
        """
        if isinstance(flow_definition, str):
            try:
                self.flow_definition = json.loads(flow_definition)
            except json.JSONDecodeError as e:
                raise FlowValidationError(f"JSON de fluxo inválido: {str(e)}")
        else:
            self.flow_definition = flow_definition
            
        self.validate_flow()
        
        self.states = self.flow_definition.get("states", {})
        self.hooks = {
            "before_transition": [],
            "after_transition": [],
            "on_error": []
        }
        
        logger.info(f"FlowManager inicializado com {len(self.states)} estados")
    
    def validate_flow(self) -> None:
        """
        Valida a estrutura do fluxo de conversa.
        
        Raises:
            FlowValidationError: Se o fluxo for inválido
        """
        if not isinstance(self.flow_definition, dict):
            raise FlowValidationError("Fluxo deve ser um dicionário")
            
        if "states" not in self.flow_definition:
            raise FlowValidationError("Fluxo deve conter a chave 'states'")
            
        if not isinstance(self.flow_definition["states"], dict):
            raise FlowValidationError("A chave 'states' deve ser um dicionário")
            
        for state_name, state_data in self.flow_definition["states"].items():
            if "responses" not in state_data:
                raise FlowValidationError(f"Estado '{state_name}' deve ter respostas definidas")
                
            if "transitions" in state_data and not isinstance(state_data["transitions"], list):
                raise FlowValidationError(f"Transições do estado '{state_name}' devem ser uma lista")
        
        logger.debug("Fluxo validado com sucesso")
    
    def state_exists(self, state_name: str) -> bool:
        """
        Verifica se um estado existe no fluxo.
        
        Args:
            state_name: Nome do estado a verificar
            
        Returns:
            True se o estado existir, False caso contrário
        """
        return state_name in self.states
    
    def determine_transition(
        self, 
        current_state: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Determina a próxima transição com base na mensagem do usuário.
        
        Args:
            current_state: Estado atual do chatbot
            message: Mensagem do usuário
            context: Contexto da conversa
            
        Returns:
            Tupla contendo o próximo estado e dados da resposta
            
        Raises:
            InvalidStateError: Se o estado atual não existir
        """
        if not self.state_exists(current_state):
            raise InvalidStateError(f"Estado '{current_state}' não existe")
        
        state_data = self.states[current_state]
        
        # Executar hooks antes da transição
        for hook in self.hooks["before_transition"]:
            hook(current_state, message, context)
        
        # Verificar transições
        next_state = current_state  # Por padrão, permanece no mesmo estado
        
        if "transitions" in state_data:
            for transition in state_data["transitions"]:
                # Verificar condição usando padrão ou função
                if self._check_transition_condition(transition, message, context):
                    next_state = transition["target"]
                    break
        
        # Gerar resposta
        response_data = self._generate_response(next_state, context)
        
        # Executar hooks após a transição
        for hook in self.hooks["after_transition"]:
            hook(current_state, next_state, response_data, context)
        
        return next_state, response_data
    
    def _check_transition_condition(
        self, 
        transition: Dict[str, Any], 
        message: str, 
        context: Dict[str, Any]
    ) -> bool:
        """
        Verifica se uma condição de transição é satisfeita.
        
        Args:
            transition: Definição da transição
            message: Mensagem do usuário
            context: Contexto da conversa
            
        Returns:
            True se a condição for satisfeita, False caso contrário
        """
        if "condition" not in transition:
            return True  # Sem condição significa transição automática
            
        condition = transition["condition"]
        
        # Verificar se é um padrão regex
        if "pattern" in condition:
            pattern = condition["pattern"]
            return bool(re.search(pattern, message, re.IGNORECASE))
            
        # Verificar se é uma condição baseada em intenção
        elif "intent" in condition:
            # Aqui você poderia integrar com um sistema de NLU
            # Por enquanto, usaremos uma abordagem simples baseada em palavras-chave
            intent = condition["intent"]
            keywords = self.flow_definition.get("intents", {}).get(intent, [])
            return any(keyword.lower() in message.lower() for keyword in keywords)
            
        # Verificar se é uma condição baseada em variável de contexto
        elif "context_var" in condition:
            var_name = condition["context_var"]
            expected_value = condition.get("value")
            
            if var_name not in context:
                return False
                
            if expected_value is not None:
                return context[var_name] == expected_value
            else:
                return bool(context[var_name])
                
        return False
    
    def _generate_response(
        self, 
        state_name: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gera uma resposta com base no estado atual.
        
        Args:
            state_name: Nome do estado
            context: Contexto da conversa
            
        Returns:
            Dados da resposta (texto e metadados)
        """
        if not self.state_exists(state_name):
            raise InvalidStateError(f"Estado '{state_name}' não existe")
            
        state_data = self.states[state_name]
        responses = state_data.get("responses", [])
        
        if not responses:
            return {"text": "Não sei como responder a isso."}
            
        # Por enquanto, apenas retorna a primeira resposta
        # Em uma implementação mais avançada, poderíamos selecionar 
        # aleatoriamente ou com base em condições
        response = responses[0]
        
        if isinstance(response, str):
            return {"text": response}
        else:
            return {
                "text": response.get("text", ""),
                "actions": response.get("actions", []),
                "metadata": response.get("metadata", {})
            }
    
    def register_hook(self, event_name: str, callback: Callable) -> None:
        """
        Registra um hook para eventos específicos.
        
        Args:
            event_name: Nome do evento ('before_transition', 'after_transition', 'on_error')
            callback: Função de callback a ser chamada
        """
        if event_name in self.hooks:
            self.hooks[event_name].append(callback)
            logger.debug(f"Hook registrado para evento '{event_name}'")
        else:
            logger.warning(f"Evento '{event_name}' não suportado para hooks")
