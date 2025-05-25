from app.utils.openai_utils import get_openai_client
import re
import json
# MBTI별 궁합 매칭표
good_matches = {
    "INTJ": ["ENFP", "ENTP"],
    "INTP": ["ENTJ", "ENFJ"],
    "ENTJ": ["INFP", "INTP"],
    "ENTP": ["INFJ", "INTJ"],
    "INFJ": ["ENFP", "ENTP"],
    "INFP": ["ENFJ", "ENTJ"],
    "ENFJ": ["INFP", "ISFP"],
    "ENFP": ["INFJ", "INTJ"],
    "ISTJ": ["ESFP", "ESTP"],
    "ISFJ": ["ESFP", "ESTP"],
    "ESTJ": ["ISFP", "ISTP"],
    "ESFJ": ["ISFP", "ISTP"],
    "ISTP": ["ESFJ", "ESTJ"],
    "ISFP": ["ESFJ", "ENFJ"],
    "ESTP": ["ISFJ", "ISTJ"],
    "ESFP": ["ISFJ", "ISTJ"],
}

bad_matches = {
    "INTJ": ["ESFP", "ISFP"],
    "INTP": ["ESFJ", "ISFJ"],
    "ENTJ": ["ISFP", "INFP"],
    "ENTP": ["ISFJ", "ESFJ"],
    "INFJ": ["ESTP", "ISTP"],
    "INFP": ["ESTJ", "ISTJ"],
    "ENFJ": ["ISTP", "ESTP"],
    "ENFP": ["ISTJ", "ISFJ"],
    "ISTJ": ["ENFP", "INFP"],
    "ISFJ": ["ENTP", "ENFP"],
    "ESTJ": ["INFP", "INFJ"],
    "ESFJ": ["INTP", "ENTP"],
    "ISTP": ["ENFJ", "ESFJ"],
    "ISFP": ["ENTJ", "ESTJ"],
    "ESTP": ["INFJ", "ENFJ"],
    "ESFP": ["INTJ", "INFJ"],
}

def result2json(gpt_result):
    match = re.search(r'({[\s\S]+})', gpt_result)
    if match:
        json_str = match.group(1)
        
    def fix_newlines_in_json(s):
        # 쌍따옴표 안에서만 실제 줄바꿈(\n)을 \n 문자로 치환
        def replacer(match):
            return match.group(0).replace('\n', '\\n')
        
        return re.sub(r'"(.*?)"', replacer, s, flags=re.DOTALL)
    
    r = fix_newlines_in_json(json_str)
    try:
        result = json.loads(r)
        return result
    except json.JSONDecodeError:
        # JSON 파싱에 실패하면 원본 반환
        return gpt_result

def analyze_mbti(result):
    user_mbti = result.get('user_profile', {}).get('mbti')
    partner_mbti = result.get('mbti_prediction', {}).get('type')
    
    match_result = {
        "user": {},
        "partner": {}
    }
    
    if user_mbti and user_mbti in good_matches:
        match_result["user"] = {
            "good": good_matches.get(user_mbti, []),
            "bad": bad_matches.get(user_mbti, [])
        }
    
    if partner_mbti and partner_mbti in good_matches:
        match_result["partner"] = {
            "good": good_matches.get(partner_mbti, []),
            "bad": bad_matches.get(partner_mbti, [])
        }
    
    return match_result

def analyze_mbti_personality(profile, file_path):
    client = get_openai_client()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prompt = f"""
    사용자에 대한 프로필입니다.
    {profile}
    다음은 사용자와의 카카오톡 대화입니다.
    상대방의 성격을 분석하고, MBTI 성격유형을 추정해 주세요.

    요구사항:
    1. MBTI를 추정해 주세요.
    2. 최종 조합(예: ENFP 가능성 70%)을 제시해 주세요.
    3. 상대방의 대화 스타일을 요약해 주세요.
    4. 상대방과 나의 서로간의 호감도 점수를 나타내주세요 (예: 75%).
    5. 상대방과 나의 대화 말투 톤을 리스트안에서 1갸 제시해 주세요. [친근함, 유머러스, 솔직함, 공감적, 논리적]
    6. 호감도 점수에 대한 핵심 인사이트를 주제와 해석을 제목과 함께 3개 제시해주세요. 제목과 내용은 \n으로 구분해주세요.
    7. 대화 내용을 기반으로 상대방과 더 나은 대화를 위한 조언을 4개 씩 제시해 주세요. 이것 역시 제목과 같이 제시해주세요.
    8. 맞춤형 액션 플랜도 제시해주세요. 위와 겹치지 않게 조심해주시요. 이것도 역시 제목과 같이 제시해 주세요.

    추가 요청사항:
    - 모든 설명은 너무 딱딱하거나 로봇처럼 들리지 않게 해 주세요.
    - 말투는 가볍고 친근하면서도 분석적이어야 합니다. (예: 친구에게 설명하듯)
    - 예: "상대방이 자주 웃는 표현을 쓰고, 대화를 긍정적으로 받아줘요. 이건 꽤 호감의 신호일 수 있어요."
        "‘같이 가자’, ‘나중에 또 보자’ 같은 표현이 자주 보이네요. 친밀감을 표현하는 성향이 뚜렷해요!"
    - 대화 조언도 실제 대화에 쓸 수 있는 말투로 써 주세요.
    - 제목과 함께 제시하는 경우는 \n으로 구분해주세요.

    출력은 다음 JSON 형식으로 제공해 주세요:

    {{
      "user_profile": {{
          "name" : "..."
          "mbti": "..."
      }}
      "mbti_prediction": {{
          "type": "ESTJ",
          "confidence": "75%",
          "mbti_commemts": "이재관 님은 상대방의 말에 따뜻하게 반응하고, 관심을 지속적으로 표현하는 성격의 ENFP 유형일 가능성이 높아요. 감정에 진심을 담아 소통하려는 태도가 돋보여요!"
        }}
      }},
      "likability_score": {{
        "user" : "...",
        "partner": "..."
      }}
      "conversational_tone": {{
        "user" : "...",
        "partner": "..."
      }},
      "likability_comments": [
        "상대방은 질문 왕🤴\n
        상대방이 질문(‘너 뭐해?’)을 5번 던졌어요. 당신에게 관심이 많다는 뜻이에요!",
        "웃음이 많아요ㅋㅋㅋ\n
        웃음 이모티콘(ㅋㅋ)이 15번 등장했어요. 유머가 잘 통하는 관계로 보입니다!",
        "긍정 지수⬆️\
        n상대방이 긍정적 반응(‘멋지다’, ‘좋아’)을 8번 보였어요. 호감도가 점차 쌓이고 있어요!"
      ],
      solutions:{{
      "conversation_advice": [
        "대화 리마인드🧐\n
        2024년 5월 31일 금요일에 만나신걸로 보여요! 그때 대화를 잘 기억해주세요.",
        "...",
        "...",
        "..."
      ],
      "action_plan": [
        "관심사 알아내기🔍\n
        다음 만남을 계획하기 위해 관심사를 끌어내보세요!",
        "...",
        "...",
        "..."
      ]
      }}
    }}

    분석 대상 대화:
    \"\"\"{content}\"\"\"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 사용 중인 모델명에 맞게 수정
        messages=[
            {"role": "system", "content": "너는 MBTI 성격 분석 전문가야. 그리고 대화 내용을 기반으로 상대방의 성격을 추론해."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
    )

    # GPT 응답을 JSON으로 변환하고 매칭 결과 추가
    gpt_result = response.choices[0].message.content
    try:
        result = result2json(gpt_result)
        
        # 결과가 딕셔너리인 경우에만 매칭 정보 추가
        if isinstance(result, dict):
            match_result = analyze_mbti(result)
            
            # mbti_prediction이 없으면 생성
            if 'mbti_prediction' not in result:
                result['mbti_prediction'] = {}
                
            result['mbti_prediction']['match_result'] = match_result
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        return gpt_result
    except Exception as e:
        # 오류 발생시 원본 응답 반환
        print(f"Error processing result: {e}")
        return gpt_result
