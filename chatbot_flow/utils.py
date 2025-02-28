"""
Utilidades para a biblioteca ChatbotFlow.
"""

import json
import os
from typing import Dict, Any, List, Optional


def load_flow_from_file(file_path: str) -> Dict[str, Any]:
    """
    Carrega um fluxo de conversa a partir de um arquivo JSON.
    
    Args:
        file_path: Caminho para o arquivo JSON
        
    Returns:
        Definição do fluxo como um dicionário
        
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        json.JSONDecodeError: Se o arquivo não contiver JSON válido
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_flow_to_file(flow: Dict[str, Any], file_path: str) -> None:
    """
    Salva um fluxo de conversa em um arquivo JSON.
    
    Args:
        flow: Definição do fluxo
        file_path: Caminho para o arquivo JSON
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(flow, f, indent=2, ensure_ascii=False)


def extract_entities(message: str, entity_patterns: Dict[str, str]) -> Dict[str, str]:
    """
    Extrai entidades de uma mensagem usando expressões regulares.
    
    Args:
        message: Mensagem do usuário
        entity_patterns: Dicionário de padrões regex para cada entidade
        
    Returns:
        Dicionário com as entidades extraídas
    """
    import re
    
    entities = {}
    
    for entity_name, pattern in entity_patterns.items():
        match = re.search(pattern, message)
        if match:
            entities[entity_name] = match.group(1)
    
    return entities


def create_simple_flow(
    welcome_message: str,
    fallback_message: str = "Desculpe, não entendi. Pode reformular?",
    goodbye_message: str = "Até logo! Foi um prazer ajudar."
) -> Dict[str, Any]:
    """
    Cria um fluxo simples com estados básicos.
    
    Args:
        welcome_message: Mensagem de boas-vindas
        fallback_message: Mensagem de fallback
        goodbye_message: Mensagem de despedida
        
    Returns:
        Fluxo básico como um dicionário
    """
    return {
        "name": "Simple Chatbot Flow",
        "version": "1.0",
        "states": {
            "start": {
                "responses": [welcome_message],
                "transitions": [
                    {
                        "condition": {
                            "pattern": "\\b(tchau|adeus|até logo)\\b"
                        },
                        "target": "end"
                    },
                    {
                        "target": "fallback"
                    }
                ]
            },
            "fallback": {
                "responses": [fallback_message],
                "transitions": [
                    {
                        "condition": {
                            "pattern": "\\b(tchau|adeus|até logo)\\b"
                        },
                        "target": "end"
                    },
                    {
                        "target": "start"
                    }
                ]
            },
            "end": {
                "responses": [goodbye_message]
            }
        },
        "intents": {
            "goodbye": ["tchau", "adeus", "até logo", "até mais", "até a próxima"],
            "greeting": ["olá", "oi", "bom dia", "boa tarde", "boa noite"]
        }
    }
