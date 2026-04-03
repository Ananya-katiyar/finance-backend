from sqlmodel import Session, select
from app.models import Record
from app.schemas import RecordCreate, RecordUpdate
from fastapi import HTTPException


def create_record(session: Session, record: RecordCreate, user_id: int) -> Record:
    db_record = Record(**record.model_dump(), user_id=user_id)
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record


def get_records(session: Session, user_id: int, type: str = None, category: str = None):
    query = select(Record).where(Record.user_id == user_id)
    if type:
        query = query.where(Record.type == type)
    if category:
        query = query.where(Record.category == category)
    return session.exec(query).all()


def update_record(session: Session, record_id: int, record: RecordUpdate, user_id: int) -> Record:
    db_record = session.get(Record, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    if db_record.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your record")
    data = record.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_record, key, value)
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record


def delete_record(session: Session, record_id: int) -> None:
    db_record = session.get(Record, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    session.delete(db_record)
    session.commit()