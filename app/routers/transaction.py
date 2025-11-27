from fastapi import HTTPException, status, APIRouter, Query
from sqlmodel import select

from app.db import SessionDep
from app.models.customers import Customer
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRead, TransactionUpdate, TransactionCreate

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TransactionRead])
async def list_transaction(
        session: SessionDep,
        skip: int = Query(0, description="Registros a omitir"),
        limit: int = Query(10, description="Numero de registros")
):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction no encontrada")
    return transaction_db


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_dict = transaction_data.model_dump()

    customer = session.get(Customer, transaction_dict.get("customer_id"))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer no encontrado")

    transaction_db = Transaction(**transaction_dict)

    try:
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear transaction\n{e}",
        )

    return transaction_db


@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
        transaction_id: int,
        transaction_data: TransactionUpdate,
        session: SessionDep,
):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction no encontrada")

    update_data = transaction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction_db, field, value)

    try:
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar transaction {transaction_id}\n{e}",
        )

    return transaction_db


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction no encontrada")

    try:
        session.delete(transaction_db)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar transaction {transaction_id}\n{e}",
        )
