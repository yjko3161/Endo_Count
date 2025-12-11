from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, get_current_user

router = APIRouter(prefix="/codes", tags=["codes"])


@router.post("/groups", response_model=schemas.CodeGroupRead, status_code=status.HTTP_201_CREATED)
def create_group(payload: schemas.CodeGroupCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = (
        db.query(models.CodeGroup)
        .filter(models.CodeGroup.hospital_id == payload.hospital_id, models.CodeGroup.group_code == payload.group_code)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="group_code already exists")
    record = models.CodeGroup(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/groups", response_model=list[schemas.CodeGroupRead])
def list_groups(hospital_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(models.CodeGroup)
    if hospital_id:
        query = query.filter(models.CodeGroup.hospital_id == hospital_id)
    return query.all()


@router.post("/items", response_model=schemas.CodeRead, status_code=status.HTTP_201_CREATED)
def create_code(payload: schemas.CodeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = (
        db.query(models.Code)
        .filter(
            models.Code.hospital_id == payload.hospital_id,
            models.Code.group_id == payload.group_id,
            models.Code.code == payload.code,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="code already exists")

    record = models.Code(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/items", response_model=list[schemas.CodeRead])
def list_codes(group_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(models.Code)
    if group_id:
        query = query.filter(models.Code.group_id == group_id)
    return query.order_by(models.Code.order_no, models.Code.code).all()
