from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import engine
from app.models import UserRole, User
from app.schemas import RecordCreate, RecordUpdate
from app.dependencies.auth import get_current_user, require_role
from app.services.record_service import create_record, get_records, update_record, delete_record
from typing import Optional

router = APIRouter()


@router.post("/records")
def post_record(
    record: RecordCreate,
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin))
):
    with Session(engine) as session:
        return create_record(session, record, current_user.id)


@router.get("/records")
def list_records(
    type: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        return get_records(session, current_user.id, type, category)


@router.put("/records/{id}")
def put_record(
    id: int,
    record: RecordUpdate,
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin))
):
    with Session(engine) as session:
        return update_record(session, id, record, current_user.id)


@router.delete("/records/{id}")
def remove_record(
    id: int,
    current_user: User = Depends(require_role(UserRole.admin))
):
    with Session(engine) as session:
        delete_record(session, id)
        return {"message": f"Record {id} deleted"}