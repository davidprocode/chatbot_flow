"""
Exceções personalizadas para a biblioteca ChatbotFlow.
"""


class FlowError(Exception):
    """Exceção base para erros relacionados ao fluxo de conversa."""
    pass


class InvalidStateError(FlowError):
    """Erro lançado quando um estado inválido é referenciado."""
    pass


class InvalidTransitionError(FlowError):
    """Erro lançado quando uma transição inválida é tentada."""
    pass


class FlowValidationError(FlowError):
    """Erro lançado quando o JSON de fluxo não é válido."""
    pass
