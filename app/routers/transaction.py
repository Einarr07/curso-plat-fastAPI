from fastapi import HTTPException, status, APIRouter
from sqlmodel import select

from app.db import SessionDep
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRead, TransactionUpdate, TransactionCreate

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TransactionRead], status_code=status.HTTP_200_OK)
async def list_transaction(session: SessionDep):
    return session.exec(select(Transaction)).all()


@router.get("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
async def get_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return transaction_db


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction = Transaction.model_validate((transaction_data.model_dump()))
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.put("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
async def update_transaction(
        transaction_id: int,
        transaction_data: TransactionUpdate,
        session: SessionDep,
):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    transaction_data.amount = transaction_data.amount
    transaction_db.description = transaction_data.description

    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(transaction_db)
    session.commit()
