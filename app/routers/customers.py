from typing import List

from fastapi import HTTPException, status, APIRouter
from sqlmodel import select

from app.db import SessionDep
from app.models.customers import Customer
from app.schemas import CustomerRead, CustomerCreate, CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CustomerRead], status_code=status.HTTP_200_OK)
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/{customer_id}", response_model=CustomerRead, status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer no encontrado")
    return customer_db


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.put("/{customer_id}", response_model=CustomerRead, status_code=status.HTTP_200_OK)
async def replace_customer(
        customer_id: int,
        customer_data: CustomerUpdate,
        session: SessionDep,
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer no encontrado")

    customer_db.name = customer_data.name
    customer_db.description = customer_data.description
    customer_db.email = customer_data.email
    customer_db.age = customer_data.age

    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.patch("/{customer_id}", response_model=CustomerRead, status_code=status.HTTP_202_ACCEPTED)
async def update_customer(
        customer_id: int,
        customer_data: CustomerUpdate,
        session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer no encontrado"
        )

    update_data = customer_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(customer_db, field, value)
    try:
        session.add(customer_db)
        session.commit()
        session.refresh(customer_db)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al actualizar customer {customer_data.id}\n{e}'
        )

    return customer_db


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer no encontrado")
    session.delete(customer_db)
    session.commit()
