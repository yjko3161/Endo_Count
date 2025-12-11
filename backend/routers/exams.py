from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from backend import models, schemas
from backend.dependencies import get_db, get_current_user

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("/", response_model=schemas.EndoExamRead, status_code=status.HTTP_201_CREATED)
def create_exam(payload: schemas.EndoExamCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = models.EndoExam(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[schemas.EndoExamRead])
def list_exams(date_filter: date, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(models.EndoExam).filter(
        models.EndoExam.exam_date == date_filter,
        models.EndoExam.hospital_id == user.hospital_id,
        models.EndoExam.deleted_yn.is_(False),
    )
    return query.order_by(models.EndoExam.exam_time).all()


@router.patch("/{exam_id}", response_model=schemas.EndoExamRead)
def update_exam(exam_id: int, payload: schemas.EndoExamUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.EndoExam).get(exam_id)
    if not record or record.hospital_id != user.hospital_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(exam_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.EndoExam).get(exam_id)
    if not record or record.hospital_id != user.hospital_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    record.deleted_yn = True
    db.add(record)
    db.commit()
