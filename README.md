# Loja de Jogos

Sistema de gerenciamento de loja de jogos via terminal, com banco de dados SQLite e interface interativa.

## Funcionalidades

- Cadastro de clientes e jogos
- Realização de vendas com controle automático de estoque
- Listagem paginada de clientes, jogos e vendas
- Histórico de compras por cliente com gasto total
- Busca de clientes por nome
- Listagem de jogos acima do preço médio

## Tecnologias

- Python 3.10+
- SQLite3 (banco de dados relacional com foreign keys, views, triggers e índices)
- [Rich](https://github.com/Textualize/rich) (formatação colorida no terminal)

## Instalação

```bash
pip install rich
```

## Como usar

```bash
python main.py
```

## Estrutura

```
├── main.py        # Ponto de entrada
├── interface.py   # Interface e menus do terminal
├── banco.py       # Camada de acesso ao banco de dados
└── erro.py        # Exceções customizadas
```
