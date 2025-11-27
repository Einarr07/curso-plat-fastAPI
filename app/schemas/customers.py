from db import engine
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from sqlmodel import Session, select

from ..db import engine
from ..models.customers import Customer


class CustomerBase(BaseModel):
    name: str
    description: str | None = None
    email: EmailStr
    age: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr):
        session = Session(engine)
        query = (
            select(Customer)
            .where(Customer.email == value)
        )
        result = session.exec(query).first()
        if result:
            raise ValidationError("El correo ya existe")
        return value


class CustomerCreate(CustomerBase):
    """Body para POST /customers"""
    pass


class CustomerUpdate(BaseModel):
    """Body para PATCH/PUT /customers/{id}"""
    name: str | None = None
    description: str | None = None
    email: EmailStr | None = None
    age: int | None = None


class CustomerRead(CustomerBase):
    """Respuesta para GET /customers"""
    id: int
