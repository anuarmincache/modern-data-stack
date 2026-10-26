# Observatório de Arboviroses

[![CI Pipeline](https://github.com/anuarmincache/modern-data-stack/actions/workflows/ci.yml/badge.svg)](https://github.com/anuarmincache/modern-data-stack/actions)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Painel de dengue, chikungunya e zika em 31 municípios (capitais, mais Maringá, Londrina, Ribeirão Preto e Foz do Iguaçu), com casos do [InfoDengue/Fiocruz](https://info.dengue.mat.br/) e clima do Open-Meteo, de 2020 a 2025.

O dashboard publicado está em <https://modern-data-stack-esap3ujuz6qen2mjso4prh.streamlit.app/>.

## O que está pronto e o que é laboratório

| Peça | Estado |
|---|---|
| `streamlit_app.py` | Dashboard no ar. Lê o InfoDengue na hora. Não usa o DuckDB nem o dbt. |
| `src/ingestion` + DuckDB + dbt | Pipeline local. O banco **não vai no Git**. É preciso coletar e transformar antes da API e do dashboard local. |
| `src/dashboard/app.py` | Dashboard local em cima do mart `mart_arboviroses`. |
| FastAPI | Seis rotas sobre o mart. Consultas parametrizadas. |
| scikit-learn + MLflow | Random Forest com validação walk-forward. Um modelo por município e doença. |
| Docker Compose | API, Streamlit local, MLflow, MinIO, Airflow, ZooKeeper e Kafka. |
| MinIO | O serviço sobe. Nenhum módulo da aplicação grava nele. |
| Airflow | As DAGs estão versionadas e a UI sobe. A imagem oficial não instala as dependências deste repositório, então as tasks falham até a imagem ser estendida. |
| Kafka | Producer e consumer de demonstração. O listener `localhost:9092` vale para cliente no host. |
| Spark, Kubernetes, Terraform | Não fazem parte deste repositório. |

Há dois dashboards de propósito. O publicado consulta a API pública. O local consulta o banco analítico. Eles não compartilham estado.

## Leitura dos modelos

Números do treino já registrado neste projeto, validação walk-forward, casos estimados do InfoDengue:

| Município | Doença | R² | MAE | RMSE |
|---|---|---:|---:|---:|
| Londrina | Dengue | 0.962 | 57.5 | 77.1 |
| Ribeirão Preto | Dengue | 0.942 | 100.1 | 184.4 |
| Maringá | Dengue | 0.934 | 60.9 | 95.9 |
| Florianópolis | Dengue | 0.927 | 45.3 | 61.7 |
| Maceió | Dengue | 0.918 | 12.7 | 18.0 |

No conjunto dos 93 modelos, o R² médio ficou em 0.508 e o melhor em 0.962. A feature dominante é `casos_lag1` (importância perto de 0.97). O R² alto descreve persistência semanal: a semana anterior explica a seguinte. Não é um alerta prospectivo validado em operação, e o clima entra pouco na previsão.

## Como rodar

Pré-requisitos: Python 3.12 e [uv](https://docs.astral.sh/uv/). Docker só para o Compose.

```bash
git clone https://github.com/anuarmincache/modern-data-stack.git
cd modern-data-stack
uv sync
cp .env.example .env
```

A chave `GROQ_API_KEY` fica só no `.env` ou nos secrets do Streamlit Cloud. O arquivo `.env` não entra no Git.

### Pipeline local

A coleta chama InfoDengue e Open-Meteo. São 31 municípios, 3 doenças e vários anos: demora e depende de rede. Rodar de novo não duplica a mesma semana epidemiológica nem o mesmo dia de clima.

```bash
uv run python -m src.ingestion.pipeline
cd infra/dbt && uv run dbt run --profiles-dir . && uv run dbt test --profiles-dir .
uv run streamlit run src/dashboard/app.py
uv run uvicorn src.api.main:app --reload
```

Sem o mart, a API e o dashboard local não têm o que consultar.

### Testes

```bash
uv run pytest
uv run ruff check src tests streamlit_app.py main.py
```

### Docker

```bash
docker compose up -d --build
```

| Serviço | URL | Observação |
|---|---|---|
| Dashboard local | http://localhost:8501 | Exige o DuckDB em `./data` |
| API | http://localhost:8000/docs | Idem |
| MLflow | http://localhost:5000 | Imagem com MLflow 3.12 fixo |
| Airflow | http://localhost:8080 | `admin` / `admin`, só laboratório |
| MinIO | http://localhost:9001 | `minioadmin` / `minioadmin`, não usado pelo código |
| Kafka | `localhost:9092` | Cliente no host |

O primeiro build baixa a stack. O contexto do Docker ignora `.venv`, `data` e artefatos do MLflow.

## API

Base: `http://localhost:8000`

| Rota | Descrição |
|---|---|
| `GET /health` | Status |
| `GET /municipios` | Municípios cobertos |
| `GET /doencas` | dengue, chikungunya, zika |
| `GET /historico/{municipio}/{doenca}?limit=` | Série, `limit` de 1 a 520 |
| `GET /alertas?nivel_minimo=` | Nível de 1 a 4 |
| `GET /ranking/{doenca}?ano=` | Ranking anual |
| `GET /resumo` | Agregado por doença |

Município e doença fora da lista de cobertura respondem 404. Parâmetro fora da faixa responde 422.

## Layout

```
src/ingestion     InfoDengue e Open-Meteo
src/storage       DuckDB
src/ml            features, walk-forward, MLflow
src/api           FastAPI
src/dashboard     Streamlit sobre o mart
streamlit_app.py  Streamlit publicado
infra/dbt         staging e mart
infra/airflow     DAGs semanais
infra/docker      imagens da API, do Streamlit e do MLflow
tests             pytest
```

## Licença

MIT. Ver [LICENSE](LICENSE).

## Autor

Anuar José Mincache — [GitHub](https://github.com/anuarmincache) — fisicanuar@gmail.com

Dados de casos: InfoDengue/Fiocruz. Clima: Open-Meteo.
