from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # InfoDengue
    infodengue_base_url: str = Field(
        default="https://info.dengue.mat.br/api/alertcity"
    )

    # OpenMeteo
    openmeteo_base_url: str = Field(
        default="https://archive-api.open-meteo.com/v1/archive"
    )

    # DuckDB
    duckdb_path: Path = Field(default=ROOT_DIR / "data" / "processed" / "arboviroses.duckdb")

    # MinIO
    minio_endpoint: str = Field(default="localhost:9000")
    minio_access_key: str = Field(default="minioadmin")
    minio_secret_key: str = Field(default="minioadmin")
    minio_bucket: str = Field(default="arboviroses")

    # MLflow
    mlflow_tracking_uri: str = Field(default="http://localhost:5000")

    # Ollama
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3")

    # Groq (somente via ambiente; nunca commitar a chave)
    groq_api_key: str = Field(default="")

    # Kafka
    kafka_bootstrap_servers: str = Field(default="localhost:9092")

    # CORS da API. Origens separadas por vírgula. "*" só para laboratório local.
    cors_origins: str = Field(default="*")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()