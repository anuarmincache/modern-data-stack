# dbt — arboviroses

Modelos em cima do DuckDB local (`casos_raw` e `clima_raw`).

O perfil está em `profiles.yml`. O caminho do banco vem de `DUCKDB_PATH` ou, por padrão, de `../../data/processed/arboviroses.duckdb` em relação a este diretório.

```bash
cd infra/dbt
uv run dbt run --profiles-dir .
uv run dbt test --profiles-dir .
```

A ingestão precisa ter rodado antes. Sem as tabelas raw, o `dbt run` falha.
