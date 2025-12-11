from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, get_current_user
from backend.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(models.User).filter(models.User.login_id == payload.login_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login_id already exists")

    record = models.User(
        hospital_id=payload.hospital_id,
        login_id=payload.login_id,
        name=payload.name,
        role=payload.role,
        is_active=payload.is_active,
        password=get_password_hash(payload.password),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.User).all()


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, payload: schemas.UserCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.User).get(user_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for key in ["hospital_id", "login_id", "name", "role", "is_active"]:
        setattr(record, key, getattr(payload, key))
    record.password = get_password_hash(payload.password)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
