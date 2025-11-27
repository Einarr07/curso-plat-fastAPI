from fastapi import APIRouter, status
from sqlmodel import select

from app.db import SessionDep
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanRead

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[PlanRead], status_code=status.HTTP_200_OK)
async def list_plan(session: SessionDep):
    return session.exec(select(Plan)).all()


@router.post("/", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data: PlanCreate, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db
