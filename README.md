# Endo_Count Suite v3

내시경 검사일지의 저장·집계·인계에 초점을 둔 FastAPI 기반 백엔드와 Streamlit 프로토타입 UI입니다. 모든 데이터는 MariaDB에 저장하며, Google Sheets 연동 없이 바로 DB에서 집계합니다.

## 주요 구성
- **백엔드**: FastAPI + SQLAlchemy + JWT 인증. `backend/` 이하에 API 라우터와 모델/스키마가 정리되어 있습니다.
- **프론트엔드 프로토타입**: 기존 Streamlit 입력/합계 화면(`app.py`)을 유지했습니다. 추후 React/Next 등으로 교체 가능.
- **데이터베이스**: MariaDB 스키마 설계에 맞춘 ORM 모델(`backend/models.py`).

## 사전 준비
1. Python 3.10+ 권장
2. MariaDB 실행 및 계정 준비
3. `.env` 파일 생성 (`.env.example` 참고)
4. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

## .env 예시
```env
APP_ENV=development
APP_PORT=8080
APP_URL=http://localhost:8080

DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=endo_count
DB_USER=endo_user
DB_PASSWORD=strong_password_here

JWT_SECRET=change_this_to_strong_random_string
JWT_EXPIRES_IN=12h

CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 데이터베이스 테이블 요약
`backend/models.py`가 다음 핵심 테이블을 포함합니다.
- `hospitals`, `users`, `doctors`, `code_groups`, `codes`, `hospital_settings`
- `endo_exams`: 내시경 검사 원본 저장, 집계 시 `exam_date`, `doctor_code`, `exam_type_code`, `patient_type_code`, `sedation_yn` 등을 직접 사용

## 백엔드 실행
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8080
```
기본 라우터:
- `POST /auth/login` (OAuth2 Password Grant): JWT 발급
- `GET /health`
- CRUD: `/hospitals`, `/users`, `/doctors`, `/codes/groups`, `/codes/items`, `/settings`
- 검사 기록: `POST/GET/PATCH/DELETE /exams`
- 집계: `GET /summary/daily?date_filter=YYYY-MM-DD`
- 인계장: `GET /summary/handover/daily?date_filter=YYYY-MM-DD`

> 대부분의 엔드포인트는 Bearer 토큰이 필요합니다. `token` 필드는 JWT `sub=login_id`, `hospital_id`, `role` 클레임을 포함합니다.

## Streamlit 프로토타입 실행
```bash
streamlit run app.py
```
시행과별 검사 건수 입력 및 합계/마크다운 테이블 생성을 지원합니다. 백엔드와 분리되어 있으니 UI 스켈레톤 정도로 활용하세요.

## 다음 단계 제안
- React/Next.js 기반 정식 프론트엔드 구축, JWT 인증 연동
- 역할/권한 세분화 및 어드민 페이지에서 병원/코드/의사 관리
- CSV/OCR 업로드 API 추가 및 대량 삽입 시 비동기 처리
- 병원별 인계장 포맷 설정을 `hospital_settings` 키로 확장
