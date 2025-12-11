import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import Base, engine
from backend.routers import auth, hospitals, users, doctors, codes, settings as hospital_settings, exams, summary

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Endo_Count Suite v3", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(hospitals.router)
app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(codes.router)
app.include_router(hospital_settings.router)
app.include_router(exams.router)
app.include_router(summary.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.app_env}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=settings.app_port, reload=True)
