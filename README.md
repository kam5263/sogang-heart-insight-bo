# MBTI 분석 API

## 프로젝트 소개
이 프로젝트는 카카오톡 대화 내용을 기반으로 상대방의 MBTI 성격유형을 분석하는 REST API를 제공합니다. 
OpenAI의 GPT 모델을 활용하여 대화 내용을 분석하고 상대방의 성격, 대화 스타일, 감정 표현 방식 등을 추론합니다.

## 주요 기능
- 카카오톡 대화 내용 분석
- MBTI 성격유형 추정 (각 지표별 확률 포함)
- 대화 스타일 요약
- 감정 표현 패턴 분석
- 대화 주제 및 공통 관심사 분석
- 효과적인 대화를 위한 조언 제공

## 기술 스택
- Python 3.8+
- Flask (RESTful API 프레임워크)
- OpenAI API (GPT 모델)

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/kam5263/sogang-heart-insight-bo.git
cd sogang-heart-insight-bo
```

### 2. 가상환경 설정 및 의존성 설치
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 환경 변수 설정
.env 파일을 생성하고 OpenAI API 키를 설정합니다:
```
OPENAI_API_KEY=your-api-key-here
```

## 사용 방법

### 1. 서버 실행
```bash
python run.py
```
서버는 기본적으로 `http://0.0.0.0:5000`에서 실행됩니다.

### 2. API 호출 예시
#### cURL을 이용한 호출:
```bash
curl -X POST http://localhost:5000/analyze-mbti \
  -H "Content-Type: application/json" \
  -d '{
    "target_name": "상대방이름",
    "content": "대화 내용..."
  }'
```

#### Python 코드 예시:
```python
import requests
import json

url = "http://localhost:5000/analyze-mbti"
headers = {"Content-Type": "application/json"}
payload = {
    "target_name": "수현",
    "content": "대화 내용..."
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## API 응답 형식
```json
{
  "result": {
    "mbti_prediction": {
      "E": "60%", "I": "40%",
      "S": "70%", "N": "30%",
      "T": "80%", "F": "20%",
      "J": "65%", "P": "35%",
      "final": {
        "type": "ESTJ",
        "confidence": "75%",
        "mbti_commemts": "상대방은 ..."
      }
    },
    "personality_summary": "...",
    "emotion_keywords_top3": ["...", "...", "..."],
    "topic_analysis": {
      "personal_topics": [...],
      "shared_topics": [...],
      "frequency_ranking": [...],
      "topic_comments": [...]
    },
    "conversation_advice": [
      "...",
      "...",
      "..."
    ]
  }
}
```

## 프로젝트 구조
```
d:\study\sai\
├── app/
│   ├── __init__.py       # Flask 앱 초기화
│   ├── config.py         # API 키 등 설정
│   ├── db.py             # sqlite 설정
│   ├── config.py         # schema 정의
│   ├── uploads/          # 사용자 업로드 파일 보관소
│   ├── routes/           # API 라우트
│   │   ├── __init__.py
│   │   └── routes.py
│   │   └── sample.py
│   ├── services/         # 서비스 로직
│   │   ├── __init__.py
│   │   └── mbti_service.py
│   │   └── topic_analysis.py
│   │   └── conversation_pattern.py
│   │   └── basic.py
│   └── utils/
│       ├── __init__.py
│       └── openai_utils.py
├── .env                  # 환경변수(API 키)
├── requirements.txt      # 의존성 패키지
├── run.py               # 앱 실행 파일
└── data.sqlite          # DB
```

## 주의사항
- OpenAI API 사용에는 비용이 발생할 수 있으니 API 호출 빈도와 사용량에 주의하세요.
- 대화 내용 분석 시 개인정보를 포함하지 않도록 주의하세요.
- API 키는 절대 공개 저장소에 업로드하지 마세요.