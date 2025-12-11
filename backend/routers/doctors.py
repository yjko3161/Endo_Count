from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, get_current_user

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=schemas.DoctorRead, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: schemas.DoctorCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = (
        db.query(models.Doctor)
        .filter(models.Doctor.hospital_id == payload.hospital_id, models.Doctor.doctor_code == payload.doctor_code)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="doctor_code already exists for hospital")

    record = models.Doctor(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[schemas.DoctorRead])
def list_doctors(hospital_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(models.Doctor)
    if hospital_id:
        query = query.filter(models.Doctor.hospital_id == hospital_id)
    return query.order_by(models.Doctor.order_no, models.Doctor.doctor_code).all()


@router.patch("/{doctor_id}", response_model=schemas.DoctorRead)
def update_doctor(doctor_id: int, payload: schemas.DoctorCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.Doctor).get(doctor_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    for key, value in payload.dict().items():
        setattr(record, key, value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
