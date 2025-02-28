"""
ChatbotFlow - Uma biblioteca para gerenciar fluxos de conversas em chatbots.

Esta biblioteca permite definir fluxos de conversa baseados em JSON para controlar
o comportamento de chatbots de maneira flexível e extensível.
"""

__version__ = "0.1.0"

from chatbot_flow.core import Chatbot
from chatbot_flow.flow_manager import FlowManager
from chatbot_flow.exceptions import (
    FlowError,
    InvalidStateError,
    InvalidTransitionError,
)

__all__ = [
    "Chatbot",
    "FlowManager",
    "FlowError",
    "InvalidStateError",
    "InvalidTransitionError",
]
