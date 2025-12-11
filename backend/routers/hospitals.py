from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, get_current_user

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.post("/", response_model=schemas.HospitalRead, status_code=status.HTTP_201_CREATED)
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(models.Hospital).filter(models.Hospital.code == hospital.code).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hospital code already exists")
    record = models.Hospital(**hospital.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[schemas.HospitalRead])
def list_hospitals(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Hospital).all()


@router.patch("/{hospital_id}", response_model=schemas.HospitalRead)
def update_hospital(hospital_id: int, data: schemas.HospitalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.Hospital).get(hospital_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    for key, value in data.dict().items():
        setattr(record, key, value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
