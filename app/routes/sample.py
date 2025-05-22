from flask import Blueprint, Response
import json

sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/nlp/sample', methods=['GET'])
def nlpSample():
    result = {
        "model_name": "KCElectra",
        "analysis_timestamp": "20240522_110000",
        "total_messages": 15,
        "sentiment_distribution": {
            "좋아하는": 4,
            "신나는": 5,
            "당황스러운": 3,
            "민망한": 3
        },
        "average_confidence": {
            "좋아하는": 0.9132,
            "신나는": 0.8914,
            "당황스러운": 0.9021,
            "민망한": 0.8795
        },
        "messages": [
            {
            "text": "오늘 하루도 수고했어~ ☺️",
            "sentiment": "좋아하는",
            "confidence": 0.95,
            "timestamp": "2024-03-11 21:30:00",
            "sender": "A"
            },
            {
            "text": "아 이거 진짜 웃겨ㅋㅋㅋㅋ",
            "sentiment": "신나는",
            "confidence": 0.88,
            "timestamp": "2024-03-11 22:00:00",
            "sender": "B"
            },
            {
            "text": "그 얘기는 왜 갑자기 꺼낸 거야?",
            "sentiment": "당황스러운",
            "confidence": 0.91,
            "timestamp": "2024-03-11 22:15:00",
            "sender": "A"
            },
            {
            "text": "우리 다음 주에 영화 보러 갈래?",
            "sentiment": "좋아하는",
            "confidence": 0.93,
            "timestamp": "2024-03-12 18:40:00",
            "sender": "B"
            },
            {
            "text": "헐 대박 나도 그거 좋아해!",
            "sentiment": "신나는",
            "confidence": 0.89,
            "timestamp": "2024-03-12 18:41:00",
            "sender": "A"
            },
            {
            "text": "어제 그 말은 그냥 실수였어...",
            "sentiment": "민망한",
            "confidence": 0.87,
            "timestamp": "2024-03-12 21:10:00",
            "sender": "B"
            },
            {
            "text": "오늘 하늘 진짜 예쁘다🌅",
            "sentiment": "좋아하는",
            "confidence": 0.89,
            "timestamp": "2024-03-13 09:00:00",
            "sender": "A"
            },
            {
            "text": "오랜만에 신나게 웃었다ㅋㅋ",
            "sentiment": "신나는",
            "confidence": 0.91,
            "timestamp": "2024-03-13 10:30:00",
            "sender": "B"
            },
            {
            "text": "어..? 그거 말한 적 없는데?",
            "sentiment": "당황스러운",
            "confidence": 0.90,
            "timestamp": "2024-03-13 14:00:00",
            "sender": "A"
            },
            {
            "text": "왜 그걸 이제 말해줘ㅠㅠ",
            "sentiment": "당황스러운",
            "confidence": 0.90,
            "timestamp": "2024-03-14 13:40:00",
            "sender": "B"
            },
            {
            "text": "이거 좀 민망하긴 한데ㅎㅎ",
            "sentiment": "민망한",
            "confidence": 0.88,
            "timestamp": "2024-03-14 14:00:00",
            "sender": "A"
            },
            {
            "text": "너랑 얘기하는 게 제일 즐거워",
            "sentiment": "좋아하는",
            "confidence": 0.89,
            "timestamp": "2024-03-14 21:30:00",
            "sender": "B"
            },
            {
            "text": "헐 헐 진짜?! 와 완전 기대된다!!",
            "sentiment": "신나는",
            "confidence": 0.92,
            "timestamp": "2024-03-15 11:10:00",
            "sender": "A"
            },
            {
            "text": "이건 좀... 내가 괜히 꺼냈나봐",
            "sentiment": "민망한",
            "confidence": 0.89,
            "timestamp": "2024-03-15 13:00:00",
            "sender": "B"
            },
            {
            "text": "오늘 진짜 신났어! 고마워~",
            "sentiment": "신나는",
            "confidence": 0.88,
            "timestamp": "2024-03-15 22:10:00",
            "sender": "A"
            }
        ]
    }
    
    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )

@sample_bp.route('/llm/sample', methods=['GET'])
def llmSample():
    result = {
        "result": "```json\n{\n  \"mbti_prediction\": {\n    \"type\": \"ISFJ\",\n    \"confidence\": \"70%\",\n    \"mbti_comments\": \"김경민 님은 상대방과의 대화에서 감정적인 반응과 배려가 보이는 성격의 ISFJ 유형일 가능성이 높아요. 자신의 일상적인 상황과 감정에 대해 솔직하게 표현하면서 상대방에게도 관심을 가집니다.\"\n  },\n  \"likability_score\": \"80%\",\n  \"convalsational_tone\": {\n    \"user\": \"친근함\",\n    \"partener\": \"친근함\"\n  },\n  \"likability_comments\": [\n    \"상대방은 유머가 풍부해요😄\\n상대방이 웃음 이모티콘(ㅎ, ㅋㅋㅋ 등)을 자주 사용하며, 대화가 편안하고 유머러스한 분위기를 만들어요!\",\n    \"상대방의 배려가 느껴져요🤗\\n상대방이 관심을 가지고 질문을 던지고, 소소한 일상에 대해 이야기하며 서로의 감정을 공유하고 있어요.\",\n    \"긍정적인 반응이 많아요⬆️\\n상대방은 자주 긍정적인 표현을 사용하며, 대화에서 좋은 기분을 유지하려는 노력이 돋보여요!\"\n  ],\n  \"solutions\": {\n    \"conversation_advice\": [\n      \"자신의 감정을 표현해보세요😊\\n상대방이 자신의 일상적인 고민이나 기분을 공유하고 있으니, 더 솔직하게 자신의 감정을 이야기해보세요.\",\n      \"더 많은 질문을 던져보세요🧐\\n상대방이 관심을 가지고 질문하는 경향이 강하니, 대화의 흐름을 이어갈 수 있도록 질문을 던져보세요.\",\n      \"함께하는 취미를 제안해보세요🎨\\n상대방이 좋아하는 것들을 알려주면, 함께 새로운 경험을 만들어갈 수 있어요.\",\n      \"대화를 정리해보세요📝\\n대화가 길어질 경우, 서로의 이야기를 간단히 요약해주면 이해가 더 쉬워질 수 있어요.\"\n    ],\n    \"action_plan\": [\n      \"공통의 관심사를 기반으로 대화하기🔍\\n상대방의 관심사와 본인의 관심사를 연결해보면 자연스러운 대화가 이어질 거예요.\",\n      \"주기적으로 안부를 물어보세요📱\\n상대방의 일상에 대해 자주 물어보면 더 많은 이야기를 나눌 수 있어요.\",\n      \"소소한 일상 공유하기📅\\n자신의 일상적인 일이나 경험을 공유하며 친밀감을 높여보세요.\",\n      \"다음 만남을 계획하면서 이야기하기🌟\\n어떤 활동을 함께 할 수 있을지 생각해보고 미리 논의해보세요.\"\n    ]\n  }\n}\n```"
    }

    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )