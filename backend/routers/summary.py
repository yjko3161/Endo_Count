from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, get_current_user

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/daily", response_model=schemas.DailySummaryResponse)
def daily_summary(date_filter: date, db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (
        db.query(
            models.Doctor.doctor_code,
            models.Doctor.name.label("doctor_name"),
            models.EndoExam.exam_type_code,
            models.EndoExam.patient_type_code,
            models.EndoExam.sedation_yn,
            models.EndoExam.id,
        )
        .join(models.EndoExam, models.EndoExam.doctor_id == models.Doctor.id)
        .filter(
            models.EndoExam.exam_date == date_filter,
            models.EndoExam.hospital_id == user.hospital_id,
            models.EndoExam.deleted_yn.is_(False),
        )
        .all()
    )

    counts: dict[tuple[str, str, str, str], int] = {}
    for row in rows:
        key = (row.doctor_code, row.doctor_name, row.exam_type_code, row.patient_type_code, row.sedation_yn)
        counts[key] = counts.get(key, 0) + 1

    results = [
        schemas.DailySummaryItem(
            doctor_code=k[0],
            doctor_name=k[1],
            exam_type_code=k[2],
            patient_type_code=k[3],
            sedation_yn=k[4],
            count=v,
        )
        for k, v in counts.items()
    ]

    return schemas.DailySummaryResponse(date=date_filter, results=results)


@router.get("/handover/daily", response_model=schemas.DailyHandoverResponse)
def daily_handover(date_filter: date, db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (
        db.query(
            models.Doctor.doctor_code,
            models.Doctor.name.label("doctor_name"),
            models.EndoExam.exam_type_code,
            models.EndoExam.patient_type_code,
            models.EndoExam.sedation_yn,
            models.EndoExam.id,
        )
        .join(models.EndoExam, models.EndoExam.doctor_id == models.Doctor.id)
        .filter(
            models.EndoExam.exam_date == date_filter,
            models.EndoExam.hospital_id == user.hospital_id,
            models.EndoExam.deleted_yn.is_(False),
        )
        .all()
    )

    counts: dict[tuple[str, str, str, str, str], int] = {}
    for row in rows:
        key = (row.patient_type_code, row.doctor_code, row.doctor_name, row.sedation_yn, row.exam_type_code)
        counts[key] = counts.get(key, 0) + 1

    sections = [
        schemas.DailyHandoverSection(
            patient_type_code=k[0],
            doctor_code=k[1],
            doctor_name=k[2],
            sedation_yn=k[3],
            exam_type_code=k[4],
            count=v,
        )
        for k, v in counts.items()
    ]

    return schemas.DailyHandoverResponse(date=date_filter, sections=sections)
