import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Única fuente de verdad para los orígenes CORS permitidos por ambiente.
CORS_ORIGINS_BY_ENVIRONMENT = {
    "development": [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:4173",
    ],
    "qa": [
        "https://qa.calculoschile.cl",
    ],
    "production": [
        "https://calculoschile.cl",
        "https://www.calculoschile.cl",
    ],
}


class Settings:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").strip().lower()
        self.cors_origins = self._resolve_cors_origins()

    def _resolve_cors_origins(self):
        try:
            return CORS_ORIGINS_BY_ENVIRONMENT[self.environment]
        except KeyError:
            valores_validos = ", ".join(CORS_ORIGINS_BY_ENVIRONMENT)
            raise RuntimeError(
                f"ENVIRONMENT='{self.environment}' no es válido. "
                f"Valores permitidos: {valores_validos}"
            ) from None


settings = Settings()
