import re
def extract_speaker(file_path, recent_chat_nums=1000):
    """
    카카오톡 대화 파일을 분석하여 기본 필드를 추출하는 함수
    두 가지 형식(모바일, PC)의 카카오톡 대화 파일을 모두 지원합니다.
    """
    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 결과를 저장할 리스트
    data = []
    
    # 현재 날짜를 저장할 변수
    current_date = None
    
    # 파일 형식 확인 (PC 포맷 또는 모바일 포맷)
    is_pc_format = False
    for line in lines[:20]:  # 처음 20줄만 확인
        if '[' in line and ']' in line and ('[오전' in line or '[오후' in line):
            is_pc_format = True
            break
    
    if is_pc_format:
        # PC 포맷: [발화자] [오전/오후 HH:MM] 메시지
        message_pattern = re.compile(r'^\[(.+?)\] \[(오전|오후) (\d{1,2}):(\d{2})\] (.+)')
    else:
        # 모바일 포맷: YYYY. MM. DD. 오전/오후 HH:MM, 발화자 : 메시지
        message_pattern = re.compile(r'^(\d{4})\. (\d{1,2})\. (\d{1,2})\. (오전|오후) (\d{1,2}):(\d{2}), (.+?) : (.+)')

    speakers = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = message_pattern.match(line)
        if match:
            if is_pc_format:
                speaker = match.group(1)
            else:
                speaker = match.group(7)
            speakers.add(speaker)

    return list(speakers)