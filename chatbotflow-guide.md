# Guia de Uso: Regex e Composição de Fluxos no ChatbotFlow

## 1. Expressões Regulares (Regex) no ChatbotFlow

As expressões regulares são fundamentais para definir condições de transição entre estados no ChatbotFlow. Elas permitem que o chatbot identifique padrões nas mensagens do usuário e direcione a conversa de acordo.

### 1.1 Sintaxe Básica de Regex

No ChatbotFlow, as expressões regulares são definidas no campo `pattern` dentro de `condition` nas transições:

```json
"transitions": [
  {
    "condition": {
      "pattern": "\\b(olá|oi|e aí)\\b"
    },
    "target": "saudacao_resposta"
  }
]
```

### 1.2 Padrões Comuns de Regex

| Padrão | Descrição | Exemplo |
|--------|-----------|---------|
| `\\b` | Indica limite de palavra | `\\bolá\\b` - Encontra "olá" como palavra completa |
| `(...)` | Agrupamento | `(olá\|oi)` - Encontra "olá" ou "oi" |
| `\|` | Alternância | `gato\|cachorro` - Encontra "gato" ou "cachorro" |
| `\\d` | Qualquer dígito | `\\d{5}` - Encontra 5 dígitos seguidos |
| `\\s` | Espaço em branco | `palavra\\s+outra` - Encontra "palavra" seguida de espaços e "outra" |
| `*` | 0 ou mais repetições | `\\w*` - Encontra 0 ou mais caracteres alfanuméricos |
| `+` | 1 ou mais repetições | `\\w+` - Encontra 1 ou mais caracteres alfanuméricos |
| `?` | 0 ou 1 repetição | `colou?r` - Encontra "color" ou "colour" |
| `{n}` | Exatamente n repetições | `\\d{5}` - Encontra exatamente 5 dígitos |
| `{n,m}` | De n a m repetições | `\\d{2,4}` - Encontra de 2 a 4 dígitos |
| `.` | Qualquer caractere | `a.b` - Encontra "aab", "abb", etc. |
| `[...]` | Classe de caracteres | `[aeiou]` - Encontra qualquer vogal |
| `[^...]` | Negação de classe | `[^0-9]` - Encontra qualquer caractere que não seja dígito |

### 1.3 Exemplos Práticos de Regex para Chatbots

#### Identificar pedido de informação
```json
"pattern": "\\b(como|onde|qual|quem|quando)\\b.*\\?"
```

#### Capturar número de pedido
```json
"pattern": "\\b(pedido|ordem)\\s+(?:número\\s+)?(\\d+)\\b"
```

#### Detectar intenção de compra
```json
"pattern": "\\b(comprar|adquirir|quero|desejo)\\s+(um|uma|o|a|os|as)?\\s+([\\w\\s]+)"
```

#### Reconhecer cumprimentos
```json
"pattern": "\\b(olá|oi|bom\\s+dia|boa\\s+tarde|boa\\s+noite)\\b"
```

### 1.4 Boas Práticas para Uso de Regex

1. **Teste suas expressões regulares**: Utilize ferramentas online como regex101.com para validar suas expressões antes de implementá-las.
2. **Comece simples**: Inicie com padrões simples e vá refinando conforme necessário.
3. **Use grupos de captura**: Eles permitem extrair informações específicas das mensagens do usuário.
4. **Considere variações**: Pense nas diferentes formas como um usuário pode expressar a mesma intenção.
5. **Escape caracteres especiais**: Use `\\` para escapar caracteres especiais como `.`, `*`, `+`, etc.

## 2. Composição de Fluxos de Conversa em JSON

Um fluxo de conversa no ChatbotFlow é definido como uma estrutura JSON com estados, respostas e transições. Vamos explorar como compor estes fluxos.

### 2.1 Estrutura Básica do Fluxo JSON

```json
{
  "name": "Nome do Fluxo",
  "version": "1.0",
  "states": {
    "estado_inicial": {
      "responses": ["Resposta inicial"],
      "transitions": [
        {
          "condition": {
            "pattern": "expressao_regular"
          },
          "target": "proximo_estado"
        }
      ]
    },
    "proximo_estado": {
      "responses": ["Resposta do próximo estado"]
    }
  },
  "intents": {
    "saudacao": ["olá", "oi", "bom dia", "boa tarde"]
  }
}
```

### 2.2 Componentes do Fluxo

#### 2.2.1 Metadados
- `name`: Nome descritivo do fluxo
- `version`: Versão do fluxo (útil para controle de versão)

#### 2.2.2 Estados (`states`)
Cada estado representa um ponto na conversa e contém:
- `responses`: Lista de possíveis respostas (uma será escolhida aleatoriamente)
- `transitions`: Lista de possíveis transições para outros estados

#### 2.2.3 Transições (`transitions`)
Cada transição define:
- `condition`: Condição para ativar a transição (geralmente um padrão regex)
- `target`: Estado de destino quando a condição é atendida
- `actions` (opcional): Ações a serem executadas durante a transição

#### 2.2.4 Intenções (`intents`)
Agrupamento de palavras-chave ou frases por intenção do usuário:
```json
"intents": {
  "saudacao": ["olá", "oi", "bom dia"],
  "despedida": ["tchau", "até logo", "adeus"]
}
```

### 2.3 Tipos de Estados Comuns

#### 2.3.1 Estado de Boas-vindas
```json
"welcome": {
  "responses": ["Olá! Como posso ajudar você hoje?"],
  "transitions": [
    {
      "condition": {
        "pattern": ".*"
      },
      "target": "menu_principal"
    }
  ]
}
```

#### 2.3.2 Estado de Menu
```json
"menu_principal": {
  "responses": [
    "Escolha uma opção:\n1. Fazer um pedido\n2. Verificar status\n3. Falar com atendente"
  ],
  "transitions": [
    {
      "condition": {
        "pattern": "\\b(1|um|fazer|pedido)\\b"
      },
      "target": "fazer_pedido"
    },
    {
      "condition": {
        "pattern": "\\b(2|dois|verificar|status)\\b"
      },
      "target": "verificar_status"
    },
    {
      "condition": {
        "pattern": "\\b(3|três|atendente|humano)\\b"
      },
      "target": "falar_atendente"
    }
  ]
}
```

#### 2.3.3 Estado de Coleta de Informação
```json
"coletar_nome": {
  "responses": ["Por favor, me informe seu nome completo:"],
  "transitions": [
    {
      "condition": {
        "pattern": "([A-Za-z]+ [A-Za-z]+)"
      },
      "target": "coletar_email",
      "actions": [
        {
          "type": "save_context",
          "key": "nome_cliente",
          "value": "${match.1}"
        }
      ]
    }
  ]
}
```

#### 2.3.4 Estado de Fallback
```json
"fallback": {
  "responses": [
    "Desculpe, não entendi. Poderia reformular?",
    "Não compreendi sua mensagem. Pode dizer de outra forma?"
  ],
  "transitions": [
    {
      "condition": {
        "pattern": ".*"
      },
      "target": "menu_principal"
    }
  ]
}
```

### 2.4 Exemplo de Fluxo Completo

Vamos criar um fluxo completo para um chatbot de suporte técnico:

```json
{
  "name": "Suporte Técnico",
  "version": "1.0",
  "states": {
    "inicio": {
      "responses": [
        "Bem-vindo ao Suporte Técnico. Como posso ajudar você hoje?"
      ],
      "transitions": [
        {
          "condition": {
            "pattern": "\\b(problema|erro|não funciona|defeito)\\b"
          },
          "target": "identificar_problema"
        },
        {
          "condition": {
            "pattern": "\\b(dúvida|como|funciona|ajuda)\\b"
          },
          "target": "responder_duvida"
        },
        {
          "condition": {
            "pattern": "\\b(humano|atendente|pessoa)\\b"
          },
          "target": "transferir_humano"
        }
      ]
    },
    "identificar_problema": {
      "responses": [
        "Entendi que você está enfrentando um problema. Por favor, selecione a categoria do problema:\n1. Problema de login\n2. Sistema lento\n3. Erro ao salvar\n4. Outro problema"
      ],
      "transitions": [
        {
          "condition": {
            "pattern": "\\b(1|um|login|senha)\\b"
          },
          "target": "problema_login"
        },
        {
          "condition": {
            "pattern": "\\b(2|dois|lento|devagar|performance)\\b"
          },
          "target": "problema_lentidao"
        },
        {
          "condition": {
            "pattern": "\\b(3|três|salvar|salvamento|perda)\\b"
          },
          "target": "problema_salvamento"
        },
        {
          "condition": {
            "pattern": "\\b(4|quatro|outro)\\b"
          },
          "target": "outro_problema"
        }
      ]
    },
    "problema_login": {
      "responses": [
        "Problemas de login são comuns. Vamos tentar algumas soluções:\n1. Verifique se o CAPS LOCK está ativado\n2. Tente redefinir sua senha\n3. Limpe os cookies do navegador\n\nAlguma dessas soluções ajudou?"
      ],
      "transitions": [
        {
          "condition": {
            "pattern": "\\b(sim|ajudou|resolveu|funcionou)\\b"
          },
          "target": "problema_resolvido"
        },
        {
          "condition": {
            "pattern": "\\b(não|nenhuma|continua|persiste)\\b"
          },
          "target": "transferir_humano"
        }
      ]
    },
    "problema_resolvido": {
      "responses": [
        "Ótimo! Fico feliz em saber que seu problema foi resolvido. Posso ajudar com mais alguma coisa?"
      ],
      "transitions": [
        {
          "condition": {
            "pattern": "\\b(sim|claro|por favor)\\b"
          },
          "target": "inicio"
        },
        {
          "condition": {
            "pattern": "\\b(não|obrigado|nada|tchau)\\b"
          },
          "target": "despedida"
        }
      ]
    },
    "transferir_humano": {
      "responses": [
        "Entendo. Vou transferir você para um atendente humano. Por favor, aguarde um momento enquanto fazemos a conexão."
      ],
      "transitions": [
        {
          "condition": {
            "pattern": ".*"
          },
          "target": "espera_atendente",
          "actions": [
            {
              "type": "notify",
              "message": "Transferência para atendente solicitada"
            }
          ]
        }
      ]
    },
    "despedida": {
      "responses": [
        "Obrigado por usar nosso suporte técnico. Tenha um ótimo dia!"
      ]
    }
  },
  "intents": {
    "saudacao": ["olá", "oi", "bom dia", "boa tarde", "boa noite"],
    "problemas": ["erro", "problema", "não funciona", "quebrado", "defeito"],
    "agradecimento": ["obrigado", "grato", "valeu", "agradeço"]
  }
}
```

### 2.5 Dicas para Design de Fluxos Eficientes

1. **Planeje o fluxo visualmente**: Antes de escrever o JSON, crie um diagrama do fluxo.
2. **Mantenha estados focados**: Cada estado deve ter um propósito claro.
3. **Preveja diferentes caminhos**: Usuários raramente seguem o caminho "feliz" esperado.
4. **Use fallbacks inteligentes**: Quando o chatbot não entender, ofereça orientação.
5. **Mantenha o contexto**: Use o armazenamento de contexto para lembrar informações importantes.
6. **Teste com usuários reais**: O comportamento real dos usuários pode surpreender.
7. **Itere e melhore**: Analise logs de conversa e refine seu fluxo continuamente.

## 3. Padrões Avançados

### 3.1 Uso de Contexto

O contexto permite que o chatbot "lembre" de informações ao longo da conversa:

```json
"coletar_email": {
  "responses": ["Qual é o seu email?"],
  "transitions": [
    {
      "condition": {
        "pattern": "([\\w._%+-]+@[\\w.-]+\\.[a-zA-Z]{2,})"
      },
      "target": "confirmar_dados",
      "actions": [
        {
          "type": "save_context",
          "key": "email_cliente",
          "value": "${match.1}"
        }
      ]
    }
  ]
},
"confirmar_dados": {
  "responses": ["Obrigado. Seu nome é ${context.nome_cliente} e seu email é ${context.email_cliente}. Está correto?"]
}
```

### 3.2 Fluxos Condicionais

Você pode criar transições baseadas em valores armazenados no contexto:

```json
"verificar_premium": {
  "responses": ["Verificando seu tipo de conta..."],
  "transitions": [
    {
      "condition": {
        "type": "context_eq",
        "key": "tipo_conta",
        "value": "premium"
      },
      "target": "menu_premium"
    },
    {
      "condition": {
        "type": "default"
      },
      "target": "menu_padrao"
    }
  ]
}
```

### 3.3 Integração com APIs

É possível chamar APIs durante as transições:

```json
"verificar_clima": {
  "responses": ["Verificando o clima para você..."],
  "transitions": [
    {
      "condition": {
        "pattern": ".*"
      },
      "target": "mostrar_clima",
      "actions": [
        {
          "type": "api_call",
          "method": "GET",
          "url": "https://api.weather.com?city=${context.cidade}",
          "response_key": "clima"
        }
      ]
    }
  ]
},
"mostrar_clima": {
  "responses": ["O clima em ${context.cidade} é ${context.clima.temperatura}°C com ${context.clima.condicao}."]
}
```

## 4. Depuração e Testes

### 4.1 Ferramentas de Teste

```python
from chatbot_flow.testing import FlowTester

tester = FlowTester("meu_fluxo.json")

# Teste de caminho feliz
test_result = tester.test_conversation([
    "Olá",
    "Quero fazer um pedido",
    "Pizza de pepperoni",
    "2",
    "Cartão de crédito"
])

print(test_result.success)  # True/False
print(test_result.coverage)  # Porcentagem de estados cobertos
print(test_result.path)     # Caminho percorrido
```

### 4.2 Logs e Monitoramento

Configure logs para depurar seu fluxo:

```python
import logging
from chatbot_flow import Chatbot

logging.basicConfig(level=logging.DEBUG)

bot = Chatbot("meu_fluxo.json")
# Os logs mostrarão detalhes sobre transições, padrões, etc.
```

## 5. Considerações Finais

- Mantenha seus fluxos modulares para facilitar a manutenção
- Documente bem as intenções e padrões de regex
- Considere usar ferramentas visuais para desenhar fluxos complexos
- Monitore métricas como taxa de fallback e comprimento das conversas
- Atualize regularmente seus fluxos com base no feedback dos usuários

---

Este guia fornece uma base sólida para trabalhar com regex e fluxos no ChatbotFlow. Para casos mais avançados, consulte a documentação completa da biblioteca.
