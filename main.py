def main() -> None:
    print(
        "\n".join(
            [
                "Observatório de Arboviroses",
                "  Testes:           uv run pytest",
                "  API:              uv run uvicorn src.api.main:app --reload",
                "  Dashboard local:  uv run streamlit run src/dashboard/app.py",
                "  Dashboard cloud:  uv run streamlit run streamlit_app.py",
                "  Ingestão:         uv run python -m src.ingestion.pipeline",
            ]
        )
    )


if __name__ == "__main__":
    main()
