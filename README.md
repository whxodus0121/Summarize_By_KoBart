# Summarize_By_KoBart

## 📌 프로젝트 소개
**Summarize_By_KoBart**는 FastAPI를 이용하여 입력된 텍스트를 **KoBART** 모델을 사용해 요약하는 서버 애플리케이션입니다. 또한, GPT API를 활용한 요약 기능도 포함되어 있습니다.

## 🚀 주요 기능
- **KoBART 기반 요약**: KoBART 모델을 이용하여 입력된 텍스트를 요약
- **GPT API 기반 요약**: OpenAI GPT API를 이용한 대체 요약 기능
- **FastAPI 서버 구현**: RESTful API 형태로 요약 기능 제공
- **Docker 지원**: 컨테이너 환경에서 실행 가능

## 🛠️ 기술 스택
- **언어**: Python
- **프레임워크**: FastAPI
- **모델**: KoBART, GPT API
- **기타**: Pydantic, Uvicorn, Docker

## 📂 프로젝트 구조
```
Summarize_By_KoBart/
│── .gitattributes              # Git LFS 설정 파일
│── .gitignore                  # Git 무시할 파일 목록
│── Dockerfile                  # Docker 컨테이너 설정 파일
│── Summarize_By_Gpt.py         # GPT API 기반 요약 코드
│── Summarize_By_KoBart.py      # KoBART 기반 요약 코드
│── requirements.txt            # 필요한 패키지 목록
│── summarize-by-kobart.tar     # Docker 이미지 파일
```

## 🔧 설치 및 실행 방법
### 1️⃣ 환경 설정
```bash
pip install -r requirements.txt
```

### 2️⃣ 서버 실행
```bash
uvicorn Summarize_By_KoBart:app --host 0.0.0.0 --port 8000
```

### 3️⃣ API 테스트 (예제)
#### KoBART 요약 요청
```bash
curl -X POST "http://localhost:8000/summarize/kobart" \
     -H "Content-Type: application/json" \
     -d '{"text": "요약할 긴 텍스트 내용"}'
```

#### GPT API 요약 요청
```bash
curl -X POST "http://localhost:8000/summarize/gpt" \
     -H "Content-Type: application/json" \
     -d '{"text": "요약할 긴 텍스트 내용"}'
```

## 📦 Docker 사용법
### 1️⃣ 빌드
```bash
docker build -t summarize-kobart .
```

### 2️⃣ 실행
```bash
docker run -p 8000:8000 summarize-kobart
```

## 📜 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.
