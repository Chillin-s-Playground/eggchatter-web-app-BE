# 🥚 EggChatter Backend

EggChatter의 백엔드 서버는 FastAPI를 기반으로 개발되었으며, 채팅 및 이스터에그 기능을 제공하는 REST API를 구현합니다. 이 프로젝트는 Poetry로 패키지를 관리하며, MongoDB와 함께 동작합니다.

## 🛠️ 프로젝트 구조

```
app
│── core               # 설정 및 핵심 로직
│   ├── base.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   └── security.py
│── models             # 데이터베이스 모델
│   ├── base.py
│   ├── chats.py
│   ├── easter_eggs.py
│   ├── friends.py
│   └── users.py
│── routers            # API 엔드포인트 라우터
│   ├── auth.py
│   ├── easter_egg.py
│   └── users.py
│── schemas            # Pydantic 스키마 정의
│   ├── auth.py
│   ├── easter_egg.py
│   └── users.py
│── services           # 서비스 로직
│   ├── auth.py
│   ├── easter_egg.py
│   └── users.py
│── tests              # 테스트 코드
│   └── test_users.py
│── main.py            # FastAPI 실행 진입점
```

## 🚀 실행 방법

### 1️⃣ 환경 설정

```bash
# 가상 환경 생성 및 활성화 (Poetry 사용)
poetry install
poetry shell
```

### 2️⃣ 환경 변수 설정

`.env` 파일을 생성하고 아래 내용을 추가하세요.

```env
DATABASE_URL=mongodb://localhost:27017/mydatabase
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3️⃣ 애플리케이션 실행

```bash
uvicorn app.main:app --port 8080 --reload
```

## 🧪 테스트 실행

```bash
pytest
```

## 📌 주요 기능

- **사용자 인증**: JWT를 활용한 로그인/회원가입
- **채팅 기능**: 실시간 메시지 전송 지원
- **이스터에그**: 특정 단어 입력 시 GIF 출력
- **RESTful API**: FastAPI 기반으로 설계

## 📜 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
