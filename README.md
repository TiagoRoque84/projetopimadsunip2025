# Plataforma de Quiz Python

Este projeto é um sistema de quiz em Python com suporte a:

- Cadastro e login de usuários
- Sistema de perguntas por categoria
- Registro de acertos, pontuação e estatísticas
- Rankings geral e por categoria
- Interface via terminal
- Funcionalidades administrativas:
  - Adição, edição, exclusão e visualização de questões
  - Listagem e remoção de usuários

## Requisitos
- Python 3.10 ou superior

## Executando
```bash
python nome_do_arquivo.py
```

## Arquivos necessários
- `dados.json`: base de dados com usuários e perguntas 

## Estrutura de dados
Os dados são armazenados em `dados.json` no seguinte formato:
```json
{
  "usuarios": [...],
  "questoes": {
    "matematica": [["2+2?", "4"]],
    "portugues": [["Plural de pão?", "pães"]]
  }
}
```
