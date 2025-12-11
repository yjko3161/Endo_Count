from datetime import date, time, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class HospitalBase(BaseModel):
    name: str
    code: str
    timezone: str = "Asia/Seoul"
    is_active: bool = True


class HospitalCreate(HospitalBase):
    pass


class HospitalRead(HospitalBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    hospital_id: int
    login_id: str
    name: str
    role: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    last_login_at: Optional[datetime]

    class Config:
        orm_mode = True


class DoctorBase(BaseModel):
    hospital_id: int
    doctor_code: str
    name: str
    department: Optional[str] = None
    is_active: bool = True
    order_no: int = 0


class DoctorCreate(DoctorBase):
    pass


class DoctorRead(DoctorBase):
    id: int

    class Config:
        orm_mode = True


class CodeGroupBase(BaseModel):
    hospital_id: int
    group_code: str
    group_name: str


class CodeGroupCreate(CodeGroupBase):
    pass


class CodeGroupRead(CodeGroupBase):
    id: int

    class Config:
        orm_mode = True


class CodeBase(BaseModel):
    hospital_id: int
    group_id: int
    code: str
    name: str
    order_no: int = 0
    is_active: bool = True


class CodeCreate(CodeBase):
    pass


class CodeRead(CodeBase):
    id: int

    class Config:
        orm_mode = True


class HospitalSettingBase(BaseModel):
    hospital_id: int
    key: str
    value: str


class HospitalSettingCreate(HospitalSettingBase):
    pass


class HospitalSettingRead(HospitalSettingBase):
    id: int

    class Config:
        orm_mode = True


class EndoExamBase(BaseModel):
    hospital_id: int
    exam_date: date
    exam_time: Optional[time] = None
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    doctor_id: int
    doctor_code: str
    exam_type_code: str
    patient_type_code: str
    sedation_yn: str = Field(..., regex="^[YN]$")
    insurance_type_code: Optional[str] = None
    room_no: Optional[str] = None
    memo: Optional[str] = None
    raw_source: Optional[str] = None
    deleted_yn: bool = False
    created_by: Optional[int] = None


class EndoExamCreate(EndoExamBase):
    pass


class EndoExamUpdate(BaseModel):
    exam_date: Optional[date] = None
    exam_time: Optional[time] = None
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    doctor_id: Optional[int] = None
    doctor_code: Optional[str] = None
    exam_type_code: Optional[str] = None
    patient_type_code: Optional[str] = None
    sedation_yn: Optional[str] = Field(None, regex="^[YN]$")
    insurance_type_code: Optional[str] = None
    room_no: Optional[str] = None
    memo: Optional[str] = None
    raw_source: Optional[str] = None
    deleted_yn: Optional[bool] = None


class EndoExamRead(EndoExamBase):
    id: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    login_id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DailySummaryItem(BaseModel):
    doctor_code: str
    doctor_name: str
    exam_type_code: str
    patient_type_code: str
    sedation_yn: str
    count: int


class DailySummaryResponse(BaseModel):
    date: date
    results: List[DailySummaryItem]


class DailyHandoverSection(BaseModel):
    patient_type_code: str
    doctor_code: str
    doctor_name: str
    sedation_yn: str
    exam_type_code: str
    count: int


class DailyHandoverResponse(BaseModel):
    date: date
    sections: List[DailyHandoverSection]
