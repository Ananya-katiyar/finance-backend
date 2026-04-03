from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models import User
from app.database import engine
from app.schemas import UserCreate
from app.dependencies.auth import require_role
from app.models import UserRole, User

router = APIRouter()

from app.schemas import UserCreate
@router.post("/register")
def register_user(user: UserCreate):
    with Session(engine) as session:
        hashed_pw = hash_password(user.password)

        db_user = User(
            email=user.email,
            password=hashed_pw,
            role="viewer",
            status="active"
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return {"message": "User created successfully"}
    
@router.post("/login")
def login_user(form: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        
        statement = select(User).where(User.email == form.username)
        db_user = session.exec(statement).first()

        # check if user exists
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid email")

        # verify password
        if not verify_password(form.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        # create token
        token = create_access_token({"sub": db_user.email})

        return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}

@router.get("/admin-only")
def admin_only(current_user: User = Depends(require_role(UserRole.admin))):
    return {"message": f"Welcome admin {current_user.email}"}

@router.get("/analyst-only")
def analyst_only(current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin))):
    return {"message": f"Welcome {current_user.role.value} {current_user.email}"} 
