from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    description: str | None = None
    email: EmailStr
    age: int


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
