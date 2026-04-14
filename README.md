
# Cinema Social API

Este projeto é uma API voltada para uma rede social de cinema. A ideia central é permitir que pessoas apaixonadas por filmes possam se conectar, compartilhar opiniões e acompanhar novidades em um único lugar.

## 🎬 Visão Geral

A API será a base para um ecossistema social focado em cinema, com recursos pensados para a experiência de fãs e cinéfilos. O objetivo é criar um espaço onde usuários possam interagir, descobrir conteúdos e construir sua identidade cinematográfica.

## 🎯 Objetivo do Projeto

- Criar a infraestrutura de uma rede social temática de cinema.
- Permitir que usuários registrem preferências, avaliações e comentários sobre filmes.
- Facilitar interações sociais como seguir perfis, curtir opiniões e montar listas pessoais.

## 👥 Para Quem é

- Cinéfilos que gostam de registrar e compartilhar suas experiências.
- Comunidades que desejam discutir filmes e tendências do mercado.
- Pessoas buscando recomendações e debates sobre cinema.

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