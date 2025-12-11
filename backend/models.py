from datetime import datetime, date, time
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Integer, Boolean, Date, Time
from sqlalchemy.orm import relationship
from backend.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    timezone = Column(String(50), default="Asia/Seoul")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", back_populates="hospital", cascade="all, delete")
    doctors = relationship("Doctor", back_populates="hospital", cascade="all, delete")
    settings = relationship("HospitalSetting", back_populates="hospital", cascade="all, delete")


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    login_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hospital = relationship("Hospital", back_populates="users")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    doctor_code = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    department = Column(String(100))
    is_active = Column(Boolean, default=True)
    order_no = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hospital = relationship("Hospital", back_populates="doctors")
    exams = relationship("EndoExam", back_populates="doctor")


class CodeGroup(Base):
    __tablename__ = "code_groups"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    group_code = Column(String(50), nullable=False)
    group_name = Column(String(100), nullable=False)

    codes = relationship("Code", back_populates="group")


class Code(Base):
    __tablename__ = "codes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("code_groups.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    order_no = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    group = relationship("CodeGroup", back_populates="codes")


class HospitalSetting(Base):
    __tablename__ = "hospital_settings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)

    hospital = relationship("Hospital", back_populates="settings")


class EndoExam(Base):
    __tablename__ = "endo_exams"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    exam_date = Column(Date, nullable=False)
    exam_time = Column(Time)
    patient_id = Column(String(50))
    patient_name = Column(String(100))
    doctor_id = Column(BigInteger, ForeignKey("doctors.id", ondelete="RESTRICT"), nullable=False)
    doctor_code = Column(String(50), nullable=False)
    exam_type_code = Column(String(50), nullable=False)
    patient_type_code = Column(String(50), nullable=False)
    sedation_yn = Column(String(1), nullable=False)
    insurance_type_code = Column(String(50))
    room_no = Column(String(20))
    memo = Column(String(255))
    raw_source = Column(String(50))
    deleted_yn = Column(Boolean, default=False)
    created_by = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = relationship("Doctor", back_populates="exams")
