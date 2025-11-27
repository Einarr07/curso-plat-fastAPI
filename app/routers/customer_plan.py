from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select

from app.db import SessionDep
from app.models.customer_plan import CustomerPlan, StatusEnum
from app.models.customers import Customer
from app.models.plan import Plan
from app.schemas.customer_plan import CustomerPlanRead

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    responses={404: {"description": "Not found"}},
)


@router.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
async def get_subscription_customer(
        customer_id: int,
        session: SessionDep,
        plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")

    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_db.id)
        .where(CustomerPlan.status == plan_status)
    )
    plans = session.exec(query).all()
    
    return plans


@router.post("/customer/{customer_id}/plan/{plan_id}", response_model=CustomerPlanRead,
             status_code=status.HTTP_201_CREATED)
async def create_subscription(
        customer_id: int,
        plan_id: int,
        session: SessionDep,
        plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='El cliente o el plan no existe'
        )

    customer_plan_db = CustomerPlan(
        customer_id=customer_db.id,
        plan_id=plan_db.id,
        status=plan_status
    )

    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db
