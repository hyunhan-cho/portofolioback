# Portfolio Backend - JWT 인증 시스템

Django REST Framework와 JWT를 사용한 회원가입/로그인 및 챗봇 시스템입니다.

## 설치 및 실행

```bash
# 가상환경 활성화 (Windows)
.\myvenv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 마이그레이션 (이미 완료됨)
python manage.py migrate

# 서버 실행
python manage.py runserver
```

## API 엔드포인트

### 1. 회원가입
**POST** `/api/users/register/`

**요청 본문:**
```json
{
    "email": "user@example.com",
    "password": "your_password123!",
    "password_confirm": "your_password123!"
}
```

**응답:**
```json
{
    "message": "회원가입이 완료되었습니다.",
    "user": {
        "email": "user@example.com",
        "id": 1
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### 2. 로그인
**POST** `/api/users/login/`

**요청 본문:**
```json
{
    "email": "user@example.com",
    "password": "your_password123!"
}
```

**응답:**
```json
{
    "message": "로그인 성공",
    "user": {
        "email": "user@example.com",
        "id": 1
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### 3. 토큰 갱신
**POST** `/api/users/token/refresh/`

**요청 본문:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**응답:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. 사용자 정보 조회 (인증 필요)
**GET** `/api/users/me/`

**헤더:**
```
Authorization: Bearer {access_token}
```

**응답:**
```json
{
    "id": 1,
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 5. 챗봇 (인증 필요)
**POST** `/api/chatbot/chat/`

**헤더:**
```
Authorization: Bearer {access_token}
```

**요청 본문:**
```json
{
    "message": "안녕하세요!"
}
```

**응답:**
```json
{
    "user_message": "안녕하세요!",
    "bot_response": "안녕하세요 user@example.com님! 당신의 메시지: '안녕하세요!'를 받았습니다.",
    "user": "user@example.com"
}
```

## 테스트 방법

### Postman이나 Thunder Client 사용

1. **회원가입:**
   - POST http://localhost:8000/api/users/register/
   - Body (JSON): 이메일, 비밀번호, 비밀번호 확인

2. **로그인:**
   - POST http://localhost:8000/api/users/login/
   - Body (JSON): 이메일, 비밀번호
   - 응답에서 access token 복사

3. **챗봇 사용:**
   - POST http://localhost:8000/api/chatbot/chat/
   - Headers: Authorization: Bearer {access_token}
   - Body (JSON): {"message": "안녕하세요!"}

### curl 사용

```bash
# 회원가입
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"testpass123!\",\"password_confirm\":\"testpass123!\"}"

# 로그인
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"testpass123!\"}"

# 챗봇 (토큰 필요)
curl -X POST http://localhost:8000/api/chatbot/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {your_access_token}" \
  -d "{\"message\":\"안녕하세요!\"}"
```

## 주요 기능

- ✅ 이메일 기반 회원가입
- ✅ 비밀번호 확인 검증
- ✅ JWT 토큰 기반 인증
- ✅ 로그인
- ✅ 토큰 갱신
- ✅ 인증된 사용자만 챗봇 접근 가능
- ✅ 관리자 페이지 지원

## 관리자 계정 생성

```bash
python manage.py createsuperuser
```

관리자 페이지: http://localhost:8000/admin/

## 보안 설정

- 비밀번호는 Django의 기본 해시 알고리즘으로 암호화됩니다
- JWT 토큰은 1시간 후 만료됩니다
- Refresh 토큰은 7일 후 만료됩니다
- 인증이 필요한 API는 JWT 토큰 없이 접근할 수 없습니다

## 프로젝트 구조

```
portofoliobackend/
├── config/              # 프로젝트 설정
│   ├── settings.py     # JWT 및 REST Framework 설정
│   └── urls.py         # 메인 URL 라우팅
├── users/              # 사용자 앱
│   ├── models.py       # 커스텀 User 모델
│   ├── serializers.py  # 회원가입/로그인 시리얼라이저
│   ├── views.py        # 인증 관련 뷰
│   └── urls.py         # 사용자 관련 URL
└── chatbot/            # 챗봇 앱
    ├── serializers.py  # 챗봇 시리얼라이저
    ├── views.py        # 챗봇 뷰 (인증 필요)
    └── urls.py         # 챗봇 URL
```

