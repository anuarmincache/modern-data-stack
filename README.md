# Observatório de Arboviroses

[![App](https://img.shields.io/badge/dashboard-ao_vivo-FF4B4B?logo=streamlit&logoColor=white)](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)
[![Municípios](https://img.shields.io/badge/31_municípios-2020--2025-e67e22)](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)
[![Dengue](https://img.shields.io/badge/dengue_SE_53%2F2025-6.290_casos-c0392b)](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)
[![São Paulo](https://img.shields.io/badge/São_Paulo-2.306_casos-d35400)](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)
[![CI](https://github.com/anuarmincache/modern-data-stack/actions/workflows/ci.yml/badge.svg)](https://github.com/anuarmincache/modern-data-stack/actions)

Dashboard de dengue, chikungunya e zika nas capitais e em Maringá, Londrina, Ribeirão Preto e Foz do Iguaçu.

**[Abrir o dashboard](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)**

Os números abaixo saíram do [InfoDengue/Fiocruz](https://info.dengue.mat.br/) em 26 de outubro de 2026, com o mesmo recorte do app: 2020 até a semana epidemiológica 53 de 2025.

## O que aparece primeiro

| | |
|---|---:|
| Municípios | **31** |
| Registros semanais (3 doenças) | **26.164** |
| Casos estimados de dengue na SE 53/2025 | **6.290** |
| Desses, só em São Paulo | **2.306** (37%) |

> São Paulo sozinho teve 2.306 casos estimados, 37% da semana. Goiânia, o segundo, teve 627.

Na dengue, nenhum dos 31 estava em nível de epidemia. Eram 18 em nível moderado e 13 em nível baixo.

| Município | Casos estimados | Nível InfoDengue |
|---|---:|---|
| São Paulo | 2.306 | Moderado |
| Goiânia | 627 | Moderado |
| Belo Horizonte | 419 | Moderado |
| Londrina | 361 | Baixo |
| Brasília | 305 | Moderado |
| Ribeirão Preto | 260 | Baixo |
| Rio de Janeiro | 215 | Moderado |
| Recife | 195 | Moderado |

Em chikungunya, na mesma semana, o único nível 4 (epidemia) foi **Campo Grande**, com 44 casos estimados. O total das 31 cidades foi 207.

## Onde a previsão acompanha a série

O botão de previsão do dashboard treina um Random Forest com as semanas anteriores (defasagens de 1, 2 e 4 semanas e a média móvel) e mede o erro nas últimas 12 semanas. Dengue, 314 semanas por município:

| Município | R² | Erro médio (casos/semana) |
|---|---:|---:|
| Salvador | 0,779 | 11,2 |
| Maceió | 0,742 | 10,6 |
| Natal | 0,689 | 6,9 |
| Foz do Iguaçu | 0,645 | 24,4 |
| Belém | 0,641 | 5,9 |

A mediana dos 31 municípios é **0,22**. O modelo repete o patamar recente da série. Onde a dengue muda de ritmo no fim do período, o R² cai. O nível de alerta continua sendo o do InfoDengue.

## Na tela

- Mapa OpenStreetMap, sem chave, com o município colorido pelo nível de alerta
- Série temporal e o cruzamento com temperatura e chuva (Open-Meteo)
- Projeção de 4 semanas para o município e a doença escolhidos
- Assistente em português (Groq, Llama 3.3 70B) usando os números já carregados
- CSV e relatório em PDF

A chave `GROQ_API_KEY` fica nos secrets do Streamlit Cloud. Sem ela, o dashboard abre e o assistente avisa.

## Rodar na sua máquina

Python 3.12 e [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/anuarmincache/modern-data-stack.git
cd modern-data-stack
uv sync
uv run streamlit run streamlit_app.py
```

Para o assistente local, crie `.streamlit/secrets.toml` com `GROQ_API_KEY`. Esse arquivo não entra no Git.

## Licença

MIT. Ver [LICENSE](LICENSE).

## Autor

Anuar José Mincache — [GitHub](https://github.com/anuarmincache) — fisicanuar@gmail.com

Casos: InfoDengue/Fiocruz. Clima: Open-Meteo. Mapa: OpenStreetMap.
