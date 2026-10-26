# Observatório de Arboviroses

[![CI Pipeline](https://github.com/anuarmincache/modern-data-stack/actions/workflows/ci.yml/badge.svg)](https://github.com/anuarmincache/modern-data-stack/actions)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Dashboard de dengue, chikungunya e zika em 31 municípios (capitais, mais Maringá, Londrina, Ribeirão Preto e Foz do Iguaçu), de 2020 a 2025.

Aplicação: <https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/>

O app está em `streamlit_app.py`. Ele consulta o [InfoDengue/Fiocruz](https://info.dengue.mat.br/) e o Open-Meteo na hora. O mapa usa OpenStreetMap, sem chave.

## O que o dashboard faz

- Métricas da última semana, mapa de alertas e série temporal
- Clima e casos no município escolhido
- Simulador: Random Forest treinado na hora com os casos daquele município e doença, e projeção de 4 semanas
- Lista de municípios em alerta
- Assistente em português via Groq (Llama 3.3 70B), usando os números já carregados na tela
- Download em CSV e relatório em PDF

A chave `GROQ_API_KEY` fica nos secrets do Streamlit Cloud. Sem ela, o restante do dashboard funciona e o assistente avisa que a chave não está configurada.

## Como rodar localmente

Python 3.12 e [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/anuarmincache/modern-data-stack.git
cd modern-data-stack
uv sync
uv run streamlit run streamlit_app.py
```

Para o assistente na máquina local, crie `.streamlit/secrets.toml` com `GROQ_API_KEY`. Esse arquivo não entra no Git.

## Licença

MIT. Ver [LICENSE](LICENSE).

## Autor

Anuar José Mincache — [GitHub](https://github.com/anuarmincache) — fisicanuar@gmail.com

Dados de casos: InfoDengue/Fiocruz. Clima: Open-Meteo.
