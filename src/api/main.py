from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.ingestion.infodengue import DOENCAS, MUNICIPIOS
from src.storage.database import query

app = FastAPI(
    title="Arboviroses Brasil API",
    description="API de vigilância epidemiológica — dengue, chikungunya e zika",
    version="1.0.0",
)

_origens = [origem.strip() for origem in settings.cors_origins.split(",") if origem.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origens or ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/municipios")
def listar_municipios():
    return {"municipios": list(MUNICIPIOS.keys())}


@app.get("/doencas")
def listar_doencas():
    return {"doencas": list(DOENCAS.keys())}


@app.get("/historico/{municipio}/{doenca}")
def historico(
    municipio: str,
    doenca: str,
    limit: int = Query(default=104, ge=1, le=520),
):
    if municipio not in MUNICIPIOS:
        raise HTTPException(status_code=404, detail=f"Município '{municipio}' não encontrado")
    if doenca not in DOENCAS:
        raise HTTPException(status_code=404, detail=f"Doença '{doenca}' não encontrada")

    df = query(
        """
        SELECT
            ano,
            semana,
            semana_epidemiologica,
            data_inicio_se,
            casos_estimados,
            casos_confirmados,
            nivel_alerta,
            media_movel_4s
        FROM mart_arboviroses
        WHERE municipio = ?
          AND doenca = ?
        ORDER BY semana_epidemiologica DESC
        LIMIT ?
        """,
        [municipio, doenca, limit],
    )

    return {
        "municipio": municipio,
        "doenca": doenca,
        "registros": df.to_dict(orient="records"),
    }


@app.get("/alertas")
def alertas(nivel_minimo: int = Query(default=3, ge=1, le=4)):
    df = query(
        """
        SELECT
            municipio,
            doenca,
            ano,
            semana,
            casos_estimados,
            nivel_alerta
        FROM mart_arboviroses
        WHERE nivel_alerta >= ?
        ORDER BY semana_epidemiologica DESC, nivel_alerta DESC
        LIMIT 50
        """,
        [nivel_minimo],
    )

    return {
        "nivel_minimo": nivel_minimo,
        "total": len(df),
        "alertas": df.to_dict(orient="records"),
    }


@app.get("/resumo")
def resumo():
    df = query("""
        SELECT
            doenca,
            COUNT(DISTINCT municipio)  as municipios,
            COUNT(*)                   as registros,
            ROUND(AVG(casos_estimados), 1) as media_casos,
            MAX(casos_estimados)       as max_casos
        FROM mart_arboviroses
        GROUP BY doenca
        ORDER BY doenca
    """)

    return {"resumo": df.to_dict(orient="records")}


@app.get("/ranking/{doenca}")
def ranking(
    doenca: str,
    ano: int = Query(default=2025, ge=2015, le=2100),
):
    if doenca not in DOENCAS:
        raise HTTPException(status_code=404, detail=f"Doença '{doenca}' não encontrada")

    df = query(
        """
        SELECT
            municipio,
            ROUND(AVG(casos_estimados), 1) as media_semanal,
            SUM(casos_estimados)           as total_casos,
            MAX(nivel_alerta)              as nivel_max
        FROM mart_arboviroses
        WHERE doenca = ?
          AND ano = ?
        GROUP BY municipio
        ORDER BY total_casos DESC
        """,
        [doenca, ano],
    )

    return {
        "doenca": doenca,
        "ano": ano,
        "ranking": df.to_dict(orient="records"),
    }
