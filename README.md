# Documentação do Módulo ChatbotFlow

## Visão Geral

ChatbotFlow é uma biblioteca Python para gerenciar fluxos de conversas em chatbots. A biblioteca permite definir fluxos de conversa usando estruturas JSON, facilitando a criação de chatbots com comportamentos complexos sem a necessidade de programação avançada.

## Recursos Principais

- Definição de fluxos de conversa baseados em JSON
- Sistema de estados e transições para controlar o diálogo
- Suporte a padrões regex para identificar intenções do usuário
- Hooks para personalizar o comportamento do chatbot
- Gerenciamento de contexto para conversas com estado
- Suporte a ações e botões para interfaces ricas

## Instalação

```bash
pip install chatbot-flow
```

Ou para instalar a partir do código fonte:

```bash
git clone https://github.com/seuusuario/chatbot-flow.git
cd chatbot-flow
pip install -e .
```

## Uso Básico

```python
from chatbot_flow import Chatbot
from chatbot_flow.utils import load_flow_from_file

# Carregar fluxo de um arquivo JSON
flow = load_flow_from_file("meu_fluxo.json")

# Criar um chatbot
bot = Chatbot(flow)

# Processar uma mensagem do usuário
resposta = bot.process_message("Olá, como vai?")

# Exibir a resposta
print(resposta["text"])
```

## Estrutura do Fluxo JSON

Um fluxo é definido como um objeto JSON com a seguinte estrutura:

```json
{
  "name": "Nome do Fluxo",
  "version": "1.0",
  "states": {
    "state1": {
      "responses": ["Resposta 1", "Resposta 2"],
      "transitions": [
        {
          "condition": {
            "pattern": "regex_pattern"
          },
          "target": "state2"
        }
      ]
    },
    "state2": {
      "responses": ["Outra resposta"]
    }
  },
  "intents": {
    "saudacao": ["olá", "oi", "bom dia"]
  }
}
```

### Elementos Principais

- **states**: Define os estados possíveis do chatbot
- **responses**: Lista de possíveis respostas para um estado
- **transitions**: Regras para mudança de estado
- **condition**: Condições para acionar uma transição
- **target**: Estado de destino para a transição
- **intents**: Agrupamento de palavras-chave por intenção

## Classes Principais

### `Chatbot`

A classe principal que gerencia o fluxo de conversa.

```python
bot = Chatbot(flow_definition, initial_state="start")
```

#### Métodos

- `process_message(message)`: Processa uma mensagem do usuário e retorna uma resposta
- `reset(initial_state="start")`: Reinicia o chatbot para o estado inicial
- `save_state()`: Salva o estado atual do chatbot
- `load_state(state_data)`: Carrega um estado previamente salvo
- `register_hook(event_name, callback)`: Registra um hook para eventos específicos

### `FlowManager`

Gerencia o fluxo de conversa com base na definição JSON.

```python
flow_manager = FlowManager(flow_definition)
```

#### Métodos

- `state_exists(state_name)`: Verifica se um estado existe no fluxo
- `determine_transition(current_state, message, context)`: Determina a próxima transição
- `register_hook(event_name, callback)`: Registra um hook para eventos específicos

## Utilitários

### `load_flow_from_file(file_path)`

Carrega um fluxo de conversa a partir de um arquivo JSON.

### `save_flow_to_file(flow, file_path)`

Salva um fluxo de conversa em um arquivo JSON.

### `create_simple_flow(welcome_message, fallback_message, goodbye_message)`

Cria um fluxo simples com estados básicos.

## Exemplo de Fluxo Completo

Veja um exemplo de fluxo para um bot de atendimento de pedidos:

```json
{
  "name": "Atendimento de Pedidos",
  "version": "1.0",
  "states": {
    "start": {
      "responses": [
        "Olá! Bem-vindo ao nosso atendimento. Como posso ajudar você hoje?"
      ],
      "transitions": [
        {
          "condition": {
            "pattern": "\\b(fazer|realizar|quero)\\s+(um\\s+)?pedido\\b"
          },
          "target": "new_order"
        },
        {
          "condition": {
            "pattern": "\\b(status|andamento|situação)\\s+(do\\s+)?pedido\\b"
          },
          "target": "check_order"
        }
      ]
    },
    "new_order": {
      "responses": [
        "Claro! Vamos fazer seu pedido. Qual produto você deseja?"
      ],
      "transitions": [
        {
          "target": "order_product"
        }
      ]
    },
    "order_product": {
      "responses": [
        "Ótima escolha! Qual a quantidade desejada?"
      ],
      "transitions": [
        {
          "target": "order_quantity"
        }
      ]
    }
  }
}
```

## Hooks e Personalização

É possível personalizar o comportamento do chatbot usando hooks:

```python
def before_transition_hook(current_state, message, context):
    print(f"Transitando do estado {current_state} com a mensagem: {message}")

bot.register_hook("before_transition", before_transition_hook)
```

Hooks disponíveis:
- `before_transition`: Chamado antes de uma transição
- `after_transition`: Chamado depois de uma transição
- `on_error`: Chamado quando ocorre um erro

## Casos de Uso

- Chatbots de atendimento ao cliente
- Assistentes virtuais
- Bots para coleta de informações
- Sistemas de FAQ interativos
- Chatbots para redes sociais e messengers

## Limitações Atuais

- Não possui integração nativa com processamento de linguagem natural (NLP)
- Suporte limitado a contexto em conversas longas
- Sem memória de longo prazo para o usuário

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
