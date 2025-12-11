from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])


@router.post("/", response_model=schemas.HospitalSettingRead, status_code=status.HTTP_201_CREATED)
def create_setting(payload: schemas.HospitalSettingCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = models.HospitalSetting(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[schemas.HospitalSettingRead])
def list_settings(hospital_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(models.HospitalSetting)
    if hospital_id:
        query = query.filter(models.HospitalSetting.hospital_id == hospital_id)
    return query.all()


@router.delete("/{setting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_setting(setting_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.HospitalSetting).get(setting_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    db.delete(record)
    db.commit()
