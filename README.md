# API-CINE

Uma API robusta e moderna para gerenciamento de filmes e usuários em plataformas de cinema. Desenvolvida com FastAPI, a API-CINE oferece funcionalidades completas para autenticação de usuários, gerenciamento de filmes favoritos e consulta de informações cinematográficas.

## Descrição

API-CINE é uma aplicação backend desenvolvida para plataformas de streaming e catálogos de filmes. Permite que usuários se cadastrem, façam login de forma segura e gerenciem seus filmes favoritos. A API utiliza autenticação baseada em tokens JWT para garantir segurança nas rotas protegidas.

## Funcionalidades

- ✅ **Autenticação de Usuários**: Cadastro e login seguro com hash de senha (bcrypt).
- ✅ **Geração de Tokens JWT**: Autenticação baseada em tokens com expiração configurável.
- ✅ **Gerenciamento de Filmes**: Listar, buscar e adicionar filmes aos favoritos.
- ✅ **Perfil do Usuário**: Visualizar dados e filmes favoritos do usuário autenticado.
- ✅ **Rotas Protegidas**: Endpoints com autenticação obrigatória.
- ✅ **Validação de Dados**: Validação completa com Pydantic.

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alto desempenho.
- **SQLAlchemy**: ORM para gerenciamento de banco de dados.
- **JWT (PyJWT)**: Autenticação baseada em tokens.
- **Bcrypt (Passlib)**: Hashing seguro de senhas.
- **Pydantic**: Validação de dados e serialização.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.
- **Uvicorn**: Servidor ASGI para executar a aplicação.

## Inicialização

1. Comandos:
   ```bash
   py -m venv venv 

   venv\Scripts\Activate.ps1  

   pip install -r requirements.txt 

   uvicorn main:app --reload