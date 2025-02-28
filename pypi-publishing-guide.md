# Guia: Como Publicar o ChatbotFlow no PyPI

## 1. Preparação do Projeto

Antes de publicar, certifique-se que seu projeto está corretamente estruturado:

```
chatbot-flow/
├── LICENSE
├── README.md
├── setup.py
├── setup.cfg (opcional)
├── pyproject.toml (recomendado para projetos modernos)
├── chatbot_flow/
│   ├── __init__.py
│   ├── core.py
│   ├── utils.py
│   └── ...
└── tests/
    ├── __init__.py
    └── ...
```

## 2. Criação dos Arquivos de Configuração

### 2.1 setup.py

Crie um arquivo `setup.py` na raiz do projeto:

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chatbot-flow",
    version="0.1.0",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Biblioteca Python para gerenciar fluxos de conversas em chatbots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/chatbot-flow",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "regex>=2021.4.4",
        # Adicione outras dependências aqui
    ],
)
```

### 2.2 pyproject.toml (Recomendado para projetos modernos)

Para projetos modernos, crie um arquivo `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py36', 'py37', 'py38', 'py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.pytest]
testpaths = ["tests"]
```

### 2.3 setup.cfg (Opcional)

Um arquivo `setup.cfg` pode complementar a configuração:

```ini
[metadata]
license_files = LICENSE

[bdist_wheel]
universal = 1

[flake8]
max-line-length = 88
exclude = .git,__pycache__,build,dist
```

### 2.4 MANIFEST.in (Opcional)

Para incluir arquivos não-Python (como documentação ou dados):

```
include LICENSE
include README.md
include requirements.txt
recursive-include tests *
recursive-exclude * __pycache__
recursive-exclude * *.py[cod]
```

## 3. Verificação do Pacote

Antes de publicar, é recomendável verificar se seu pacote está bem estruturado:

```bash
# Instale as ferramentas necessárias
pip install build twine

# Construa o pacote
python -m build

# Verifique o pacote
twine check dist/*
```

## 4. Criação de Contas

### 4.1 Conta no PyPI

1. Acesse [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Crie sua conta
3. Verifique seu e-mail
4. Recomendado: Configure a autenticação de dois fatores

### 4.2 Conta no TestPyPI (Opcional, mas recomendado)

1. Acesse [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. Crie sua conta
3. Verifique seu e-mail

## 5. Configuração do Token de API

Por segurança, use tokens de API em vez de senha:

1. Acesse sua conta no PyPI
2. Vá para "Account settings" > "API tokens"
3. Crie um novo token (escolha escopo específico para o projeto)
4. Guarde o token com segurança

Crie um arquivo `~/.pypirc` em seu diretório home:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # seu token do PyPI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # seu token do TestPyPI
```

Proteja este arquivo:

```bash
chmod 600 ~/.pypirc
```

## 6. Publicação no TestPyPI (Recomendado para testes)

```bash
# Limpe distribuições antigas
rm -rf build/ dist/

# Construa o pacote
python -m build

# Faça upload para o TestPyPI
twine upload --repository testpypi dist/*
```

Teste a instalação:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chatbot-flow
```

## 7. Publicação no PyPI

Quando estiver satisfeito com os testes:

```bash
# Limpe distribuições antigas
rm -rf build/ dist/

# Construa o pacote
python -m build

# Faça upload para o PyPI
twine upload dist/*
```

## 8. Verificação Pós-Publicação

Teste a instalação do pacote publicado:

```bash
# Crie um ambiente virtual para testes
python -m venv test-env
source test-env/bin/activate  # No Windows: test-env\Scripts\activate

# Instale o pacote
pip install chatbot-flow

# Teste importação e uso básico
python -c "from chatbot_flow import Chatbot; print('Importação bem-sucedida!')"
```

## 9. Manutenção e Atualizações

### 9.1 Versionamento Semântico

Use versionamento semântico (SemVer):
- Versão `1.0.0`: Versão estável inicial
- Versão `1.0.1`: Correções de bugs
- Versão `1.1.0`: Novos recursos compatíveis
- Versão `2.0.0`: Mudanças incompatíveis

### 9.2 Publicação de Atualizações

Para atualizar seu pacote:

1. Atualize a versão em `setup.py`
2. Atualize o `CHANGELOG.md` (se tiver)
3. Construa e faça upload novamente:
   ```bash
   python -m build
   twine upload dist/*
   ```

### 9.3 GitHub Releases (Recomendado)

Sincronize as versões do PyPI com releases no GitHub:

1. Crie uma tag para a versão: `git tag v0.1.0`
2. Envie a tag: `git push origin v0.1.0`
3. Crie um release no GitHub com notas da versão

## 10. Automatização com GitHub Actions

Para automatizar a publicação, crie um arquivo `.github/workflows/publish.yml`:

```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

Configure os secrets `PYPI_USERNAME` e `PYPI_PASSWORD` nas configurações do seu repositório GitHub.

## 11. Dicas e Melhores Práticas

### 11.1 Documentação

- Mantenha README.md atualizado
- Considere usar Sphinx para documentação mais completa
- Documente todas as APIs públicas

### 11.2 Testes

- Mantenha cobertura de testes alta
- Configure integração contínua (CI)
- Teste em diferentes versões do Python

### 11.3 Comunidade

- Defina diretrizes de contribuição (CONTRIBUTING.md)
- Responda a issues e pull requests
- Mantenha um CHANGELOG.md

### 11.4 SEO e Descoberta

- Escolha um nome descritivo e único
- Use palavras-chave relevantes na descrição
- Adicione tópicos ao repositório GitHub

## 12. Solução de Problemas Comuns

### 12.1 Nome já em uso

Se o nome "chatbot-flow" já estiver em uso no PyPI, considere alternativas:
- chatbotflow (sem hífen)
- python-chatbot-flow
- pychatbotflow

### 12.2 Erros de upload

- Verifique configurações do ~/.pypirc
- Verifique se a versão não existe já no PyPI
- Verifique permissões de arquivos

### 12.3 Dependências não resolvidas

- Especifique versões mínimas em install_requires
- Evite dependências excessivas

## 13. Recursos Adicionais

- [Guia oficial de empacotamento do Python](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
- [PyPI Help](https://pypi.org/help/)
- [Packaging User Guide](https://packaging.python.org/)
