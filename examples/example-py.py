"""
Exemplo simples de uso da biblioteca ChatbotFlow.
"""

import os
import sys
import logging

# Adicionar o diretório pai ao path para importar o pacote
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot_flow import Chatbot
from chatbot_flow.utils import load_flow_from_file, create_simple_flow

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Método 1: Carregar fluxo a partir de um arquivo JSON
def run_from_file():
    print("=== Iniciando chatbot com fluxo de arquivo JSON ===")
    
    # Carregar o fluxo do arquivo JSON
    flow_path = os.path.join(os.path.dirname(__file__), 'custom_flow.json')
    flow = load_flow_from_file(flow_path)
    
    # Criar o chatbot
    bot = Chatbot(flow)
    
    # Loop de interação
    print(f"Bot: {bot.flow_manager.states['start']['responses'][0]}")
    
    while True:
        user_input = input("Você: ")
        
        # Verificar se o usuário quer sair
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando chatbot...")
            break
            
        # Processar a mensagem
        response = bot.process_message(user_input)
        
        # Exibir a resposta
        print(f"Bot: {response['text']}")
        
        # Exibir ações, se houver
        if 'actions' in response and response['actions']:
            print("Opções:")
            for i, action in enumerate(response['actions']):
                print(f"  {i+1}. {action['text']}")


# Método 2: Criar um fluxo simples programaticamente
def run_simple():
    print("=== Iniciando chatbot com fluxo simples ===")
    
    # Criar um fluxo simples
    flow = create_simple_flow(
        welcome_message="Olá! Sou um chatbot simples. Como posso ajudar?",
        fallback_message="Desculpe, não entendi. Pode tentar novamente?",
        goodbye_message="Até logo! Foi um prazer conversar com você."
    )
    
    # Criar o chatbot
    bot = Chatbot(flow)
    
    # Loop de interação
    print(f"Bot: {flow['states']['start']['responses'][0]}")
    
    while True:
        user_input = input("Você: ")
        
        # Verificar se o usuário quer sair
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando chatbot...")
            break
            
        # Processar a mensagem
        response = bot.process_message(user_input)
        
        # Exibir a resposta
        print(f"Bot: {response['text']}")


if __name__ == "__main__":
    # Escolha qual método executar
    choice = input("Escolha o modo (1: JSON, 2: Simples): ")
    
    if choice == "1":
        run_from_file()
    else:
        run_simple()