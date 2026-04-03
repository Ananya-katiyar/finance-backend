from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import engine
from app.models import Record, User
from app.dependencies.auth import require_role
from app.models import UserRole
from collections import defaultdict

router = APIRouter()


# GET /dashboard/summary — analyst + admin only
@router.get("/dashboard/summary")
def get_summary(current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin))):
    with Session(engine) as session:
        records = session.exec(select(Record).where(Record.user_id == current_user.id)).all()

        income = sum(r.amount for r in records if r.type == "income")
        expense = sum(r.amount for r in records if r.type == "expense")
        balance = income - expense

        return {
            "income": income,
            "expense": expense,
            "balance": balance
        }


# GET /dashboard/by-category — analyst + admin only
@router.get("/dashboard/by-category")
def get_by_category(current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin))):
    with Session(engine) as session:
        records = session.exec(select(Record).where(Record.user_id == current_user.id)).all()

        totals = defaultdict(float)
        for r in records:
            totals[r.category] += r.amount

        return dict(totals)

# GET /dashboard/monthly — analyst + admin only

@router.get("/dashboard/monthly")
def get_monthly(current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin))):
    with Session(engine) as session:
        records = session.exec(select(Record).where(Record.user_id == current_user.id)).all()

        monthly = defaultdict(lambda: defaultdict(float))
        for r in records:
            key = r.date.strftime("%Y-%m")
            monthly[key][r.type] += r.amount

        return {month: dict(types) for month, types in monthly.items()}