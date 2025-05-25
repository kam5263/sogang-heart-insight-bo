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
    # result = {
    #     "result": "{\n  \"user_profile\": {\n    \"name\": \"안재원\",\n    \"mbti\": \"ENFP\"\n  },\n  \"mbti_prediction\": {\n    \"type\": \"ESFP\",\n    \"confidence\": \"70%\",\n    \"mbti_comments\": \"안재원 님은 대화에서 긍정적인 반응과 유머를 자주 사용하며, 실시간으로 반응을 주는 모습이 ESFP 유형의 특징을 보여줍니다. 다른 사람들과의 상호작용을 즐기며, 상황에 따라 유연하게 대처하는 성향이 돋보여요!\",\n    \"match_result\": {\n      \"user\": {\n        \"good\": [\n          \"INFJ\",\n          \"INTJ\"\n        ],\n        \"bad\": [\n          \"ISTJ\",\n          \"ISFJ\"\n        ]\n      },\n      \"partner\": {\n        \"good\": [\n          \"ISFJ\",\n          \"ISTJ\"\n        ],\n        \"bad\": [\n          \"INTJ\",\n          \"INFJ\"\n        ]\n      }\n    }\n  },\n  \"likability_score\": {\n    \"user\": \"80%\",\n    \"partner\": \"80%\"\n  },\n  \"convalsational_tone\": {\n    \"user\": \"친근함\",\n    \"partner\": \"친근함\"\n  },\n  \"likability_comments\": [\n    \"유머가 잘 통하는 관계🤣\\n안재원 님이 웃음 이모티콘을 자주 사용하며 대화에서 즐거움을 전해주고 있어요!\",\n    \"진솔한 대화😌\\n서로의 고민이나 상황에 대해 솔직하게 이야기하며 신뢰감을 쌓고 있는 모습이에요.\",\n    \"상호 관심👀\\n안재원 님이 상대방의 이야기에 적극적으로 반응하고 질문을 던지며 소통하고 있어요!\"\n  ],\n  \"solutions\": {\n    \"conversation_advice\": [\n      \"자주 물어보기❓\\n상대방의 취미나 관심사에 대해 더 많이 질문해보세요!\",\n      \"공통 관심사 찾기🔍\\n서로의 공통 관심사를 찾아 대화를 더욱 풍부하게 해보세요.\",\n      \"유머 활용하기😂\\n더 많은 유머와 재치 있는 대화를 시도해보면 좋겠어요!\",\n      \"상대방의 의견 존중하기🤝\\n서로의 의견을 존중하며 대화의 깊이를 더해보세요.\"\n    ],\n    \"action_plan\": [\n      \"다음 만남 계획하기📅\\n서로의 일정을 조율하고 만남의 기회를 만들어요!\",\n      \"공동 프로젝트 제안하기🤗\\n함께 할 수 있는 프로젝트나 활동을 제안해 보세요!\",\n      \"사회적 거리두기 풀리면 외출하기🌳\\n코로나가 끝난 후 함께 외출할 계획을 세워보세요!\",\n      \"자주 연락하기📱\\n소소한 일상이나 소식을 자주 공유해 친밀감을 높여보세요.\"\n    ]\n  }\n}"
    # }

    result = {
    "result": "{\n  \"user_profile\": {\n    \"name\": \"민바다\",\n    \"mbti\": \"ISFJ\"\n  },\n  \"mbti_prediction\": {\n    \"type\": \"ESFJ\",\n    \"confidence\": \"75%\",\n    \"mbti_comments\": \"상대방은 타인을 배려하고 공감하는 성향이 강하며, 대화 중에 상대에게 관심을 기울이고 따뜻한 반응을 보이는 모습이 돋보여요. ESFJ 유형일 가능성이 높아 보입니다!\",\n    \"match_result\": {\n      \"user\": {\n        \"good\": [\n          \"ESFP\",\n          \"ESTP\"\n        ],\n        \"bad\": [\n          \"ENTP\",\n          \"ENFP\"\n        ]\n      },\n      \"partner\": {\n        \"good\": [\n          \"ISFP\",\n          \"ISTP\"\n        ],\n        \"bad\": [\n          \"INTP\",\n          \"ENTP\"\n        ]\n      }\n    }\n  },\n  \"likability_score\": {\n    \"user\": \"80%\",\n    \"partner\": \"85%\"\n  },\n  \"conversational_tone\": {\n    \"user\": \"공감적\",\n    \"partner\": \"친근함\"\n  },\n  \"likability_comments\": [\n    \"상대방은 자주 긍정적인 반응을 보여줘요! 😊\",\n    \"상대방이 당신에게 관심을 많이 보이네요. 질문도 많이 던지고 적극적이에요!\",\n    \"유머를 섞어 대화하는 방식이 서로에게 친밀감을 주고 있어요. 😄\"\n  ],\n  \"solutions\": {\n    \"conversation_advice\": [\n      \"상대방의 관심사를 더 자세히 물어보세요! 예를 들어, '최근에 어떤 책을 읽었어요?'라고 질문해보세요.\",\n      \"자신의 일상적인 이야기들을 더 공유해보세요. 상대방이 공감할 수 있는 주제들로 소통하면 좋을 것 같아요!\",\n      \"상대방의 감정을 확인해보는 것도 좋습니다. '그때 어땠어요?' 같은 방식으로 대화를 이어가세요.\",\n      \"유머를 더 활용해 보세요. 상대방이 유머를 좋아하는 것 같으니, 가벼운 농담을 해보세요!\"\n    ],\n    \"action_plan\": [\n      \"다음 만남에서 서로의 취미에 대해 깊이 있는 대화를 나눠보세요.\",\n      \"상대방이 좋아하는 음악이나 영화를 물어보면서 대화의 폭을 넓혀보세요.\",\n      \"함께 할 수 있는 활동을 제안해 보세요. 예를 들어, '같이 영화 보러 갈까요?'와 같은 접근이 좋을 것 같아요.\",\n      \"상대방이 관심 있어 하는 주제에 대해 더 알아보고, 그에 대한 이야기를 준비해가세요.\"\n    ]\n  }\n}"
    }

    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )