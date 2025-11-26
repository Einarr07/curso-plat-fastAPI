import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

postgresql_url = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@'
    f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
engine = create_engine(postgresql_url, echo=True)


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
