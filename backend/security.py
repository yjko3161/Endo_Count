from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _parse_expiry(expires_in: str) -> int:
    try:
        if expires_in.endswith("h"):
            return int(expires_in.rstrip("h")) * 3600
        if expires_in.endswith("m"):
            return int(expires_in.rstrip("m")) * 60
        if expires_in.endswith("d"):
            return int(expires_in.rstrip("d")) * 86400
        return int(expires_in)
    except Exception:
        return 43200  # default 12h


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire_seconds = _parse_expiry(settings.jwt_expires_in)
    expire = datetime.utcnow() + (expires_delta or timedelta(seconds=expire_seconds))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except JWTError:
        return None
