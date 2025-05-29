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
        "result": "{\n  \"profile\": {\n    \"user_name\": \"Ami\",\n    \"user_mbti\": \"ISTP\",\n    \"partner_name\": \"김경민\",\n    \"partner_mbti\": \"ESTP\"\n  },\n  \"mbti_prediction\": {\n    \"original\": {\n      \"type\": \"ESTP\",\n      \"confidence\": \"100%\",\n      \"mbti_comments\": \"김경민 님은 활동적이고 즉각적인 반응을 중시하는 ESTP 유형으로, 주변 상황에 민감하게 반응하며 대화에서 유머와 친근함을 잘 전달하는 모습이 보입니다.\"\n    },\n    \"predict\": {\n      \"type\": \"ENTP\",\n      \"confidence\": \"70%\",\n      \"mbti_comments\": \"김경민 님은 대화에서 창의적이고 도전적인 접근을 보이며, 변화와 새로운 아이디어를 좋아하는 ENTP 유형일 가능성도 있어요. 유머와 활력을 통해 소통하는 모습이 인상적입니다.\"\n    }\n  },\n  \"likability_score\": {\n    \"user\": \"80%\",\n    \"partner\": \"80%\"\n  },\n  \"conversational_tone\": {\n    \"user\": \"친근함\",\n    \"partner\": \"유머러스\"\n  },\n  \"likability_comments\": [\n    \"상대방의 질문에 적극적이에요❓\\n김경민 님이 여러 번 질문을 던지며 대화에 흥미를 보였어요. 이는 아미 님에게 많은 관심이 있다는 신호에요!\",\n    \"웃음이 넘쳐요😄\\n대화 중 웃음 이모티콘(ㅋㅋ) 사용이 많아, 서로 유머가 잘 통하는 관계라는 느낌이네요!\",\n    \"긍정적인 에너지가 느껴져요✨\\n김경민 님이 긍정적인 표현을 자주 사용하며, 아미 님과의 대화를 즐기는 듯해요!\"\n  ],\n  \"solutions\": {\n    \"conversation_advice\": [\n      \"가벼운 농담 던져보세요😄\\n김경민 님은 유머를 좋아하니, 대화 중 가벼운 농담을 해보면 더욱 친밀감이 높아질 거예요.\",\n      \"상대방의 관심사에 대해 물어보세요🤔\\n김경민 님의 대화 스타일을 고려할 때, 그의 관심사에 대해 물어보면 대화가 더욱 풍부해질 수 있어요.\",\n      \"자주 소통해보세요📱\\n김경민 님이 질문을 많이 하니, 자주 대화하며 그 관심에 반응해 보세요.\",\n      \"공통의 관심사 발견하기🧐\\n서로의 관심사를 비교해보며 공통점을 찾으면 더 많은 대화 주제가 생길 것 같아요.\"\n    ],\n    \"action_plan\": [\n      \"함께 할 활동 제안하기🥳\\n다음 만남에 어떤 활동을 함께 할지 아이디어를 내보세요! 예를 들어, 노래방이나 스포츠 활동 등의 계획이요.\",\n      \"소소한 일상 공유하기📝\\n서로의 일상적인 이야기를 자주 나누면 친밀감이 더 쌓일 것 같아요.\",\n      \"정기적인 만남 계획하기📅\\n정기적으로 만나서 대화할 수 있는 시간을 만드는 것도 좋겠어요.\",\n      \"서로의 취미 공유하기🎨\\n각자의 취미를 소개하며 대화의 폭을 넓혀보세요!\"\n    ]\n  },\n  \"chemistry_analysis\": [\n    {\n      \"analysis_type\": \"original\",\n      \"partner_mbti\": \"ESTP\",\n      \"chemistry_score\": 75,\n      \"chemistry_description\": \"**Ami과 김경민은 카멜레온와 치타 – 카멜레온과 치타의 독특한 케미**\",\n      \"score_summary\": \"**우리의 케미 점수: 75점! (균형잡힌 관계! ⚖️)**\",\n      \"warning_signal\": \"⚠️ **위험 신호:** 서로 다른 매력 때문에 새로운 세계를 발견하게 될 위험!\",\n      \"character_info\": {\n        \"user\": {\n          \"animal\": \"카멜레온\",\n          \"type\": \"쿨한 기술자\",\n          \"traits\": [\n            \"실용적인\",\n            \"독립적인\",\n            \"논리적인\",\n            \"적응력 있는\"\n          ],\n          \"keywords\": [\n            \"실용\",\n            \"독립\",\n            \"기술\",\n            \"논리\"\n          ]\n        },\n        \"partner\": {\n          \"animal\": \"치타\",\n          \"type\": \"액션형 모험가\",\n          \"traits\": [\n            \"활동적인\",\n            \"현실적인\",\n            \"적응력 있는\",\n            \"사교적인\"\n          ],\n          \"keywords\": [\n            \"행동\",\n            \"현실\",\n            \"모험\",\n            \"즉흥\"\n          ]\n        }\n      },\n      \"title\": \"원래 MBTI (ESTP)와의 케미\"\n    },\n    {\n      \"analysis_type\": \"predicted\",\n      \"partner_mbti\": \"ENTP\",\n      \"chemistry_score\": 75,\n      \"chemistry_description\": \"**Ami과 김경민은 카멜레온와 돌고래 – 카멜레온과 돌고래의 독특한 케미**\",\n      \"score_summary\": \"**우리의 케미 점수: 75점! (좋은 케미! 😊)**\",\n      \"warning_signal\": \"⚠️ **위험 신호:** 균형 잡힌 케미로 안정적인 관계가 지속될 위험!\",\n      \"character_info\": {\n        \"user\": {\n          \"animal\": \"카멜레온\",\n          \"type\": \"쿨한 기술자\",\n          \"traits\": [\n            \"실용적인\",\n            \"독립적인\",\n            \"논리적인\",\n            \"적응력 있는\"\n          ],\n          \"keywords\": [\n            \"실용\",\n            \"독립\",\n            \"기술\",\n            \"논리\"\n          ]\n        },\n        \"partner\": {\n          \"animal\": \"돌고래\",\n          \"type\": \"아이디어 폭발형 창의가\",\n          \"traits\": [\n            \"호기심 많은\",\n            \"유연한\",\n            \"혁신적인\",\n            \"토론 좋아하는\"\n          ],\n          \"keywords\": [\n            \"창의성\",\n            \"가능성\",\n            \"변화\",\n            \"토론\"\n          ]\n        }\n      },\n      \"title\": \"예측 MBTI (ENTP)와의 케미\"\n    }\n  ]\n}"
    }

    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )