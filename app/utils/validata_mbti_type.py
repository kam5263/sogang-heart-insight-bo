# MBTI 타입이 올바른지 검증하는 함수 추가
def validate_mbti_type(mbti_type: str) -> str:
    """MBTI 타입 검증 및 정리"""
    if not mbti_type:
        return mbti_type
    
    # 중복 문자 제거 (예: ISTJJ → ISTJ)
    cleaned = ''.join(dict.fromkeys(mbti_type))
    
    # 4글자가 아니면 원본 반환
    if len(cleaned) != 4:
        return mbti_type
        
    return cleaned