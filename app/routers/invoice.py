from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import SessionDep
from app.models.invoice import Invoice
from app.schemas import InvoiceCreate, InvoiceRead, InvoiceUpdate

router = APIRouter(
    prefix="/invoice",
    tags=["invoice"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=InvoiceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice(
        invoice_data: InvoiceCreate,
        session: SessionDep,
):
    invoice = Invoice.model_validate(invoice_data)

    try:
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear invoice\n{e}",
        )

    return invoice


@router.get("/", response_model=list[InvoiceRead])
async def list_invoices(session: SessionDep):
    invoices = session.exec(select(Invoice)).all()
    return invoices


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(
        invoice_id: int,
        session: SessionDep,
):
    invoice = session.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice no encontrado",
        )

    return invoice


@router.patch("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(
        invoice_id: int,
        invoice_data: InvoiceUpdate,
        session: SessionDep,
):
    invoice_db = session.get(Invoice, invoice_id)
    if not invoice_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice no encontrado",
        )

    update_data = invoice_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(invoice_db, field, value)

    try:
        session.add(invoice_db)
        session.commit()
        session.refresh(invoice_db)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar invoice {invoice_id}\n{e}",
        )

    return invoice_db


@router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_invoice(
        invoice_id: int,
        session: SessionDep,
):
    invoice_db = session.get(Invoice, invoice_id)
    if not invoice_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice no encontrado",
        )

    try:
        session.delete(invoice_db)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar invoice {invoice_id}\n{e}",
        )
