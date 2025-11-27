# conftest.py
import os

import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from app.db import get_session
from app.main import app

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# ⚠️ Usa una BD distinta para test
DB_NAME = os.getenv("DB_NAME_TEST", "curso_plat_fastapi_test")

postgresql_url = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 👉 Engine para Postgres, sin StaticPool ni connect_args raros
engine = create_engine(
    postgresql_url,
    echo=False,  # pon True si quieres ver las queries
)


@pytest.fixture(name="session")
def session_fixture():
    # Crea todas las tablas antes del test
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Borra todas las tablas al terminar el test
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Sobrescribimos la dependencia get_session para que use
    # la sesión de test (ligada a nuestro engine de tests)
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
