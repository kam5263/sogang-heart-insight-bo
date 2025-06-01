def _get_josa(name: str, josa_type: str) -> str:
    """한국어 조사 자동 선택"""
    if not name:
        return ""
    
    last_char = name[-1]
    last_char_code = ord(last_char)
    
    # 한글인지 확인
    if 0xAC00 <= last_char_code <= 0xD7A3:
        # 받침 있는지 확인 (한글 유니코드 계산)
        has_batchim = (last_char_code - 0xAC00) % 28 != 0
    else:
        # 영어나 숫자인 경우 받침 있다고 가정
        has_batchim = True
    
    if josa_type == "subject":  # 주어 (은/는)
        return "은" if has_batchim else "는"
    elif josa_type == "and":  # 연결 (과/와)
        return "과" if has_batchim else "와"
    else:
        return ""