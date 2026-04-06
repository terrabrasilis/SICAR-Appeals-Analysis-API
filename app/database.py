import os
from pathlib import Path

import psycopg2

SECRETS_DIR = Path("/run/secrets")


def _read_secret(secret_name: str) -> str | None:
    secret_path = os.environ.get(secret_name)
    print(secret_path)
    if os.path.exists(secret_path):
        with open(secret_path, 'r') as f:
            return f.read().strip()
    return None


def _get_connection_from_secret(secret_name: str):
    database_url = _read_secret(secret_name)
    if not database_url:
        raise RuntimeError(f"Secret não encontrado: {secret_name}")
    return psycopg2.connect(database_url)


def get_connection_sicar():
    return _get_connection_from_secret("DB_URL_SICAR")


def get_connection_prodes(biome):
    biome = biome.lower()

    secret_map = {
        "pantanal": "DB_URL_PANTANAL",
        "amazonia": "DB_URL_AMAZONIA",
        "cerrado": "DB_URL_CERRADO",
        "pampa": "DB_URL_PAMPA",
        "caatinga": "DB_URL_CAATINGA",
        "mata_atlantica": "DB_URL_MATA_ATLANTICA"
    }

    secret_name = secret_map.get(biome)
    if not secret_name:
        raise ValueError(f"Bioma inválido: {biome}")

    return _get_connection_from_secret(secret_name)