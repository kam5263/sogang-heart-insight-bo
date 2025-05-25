import pandas as pd
import re
import os
from datetime import datetime

def parse_kakao_chat(file_path, recent_chat_nums=1000):
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
    
    # 날짜 패턴 정의
    if is_pc_format:
        # PC 포맷 날짜 패턴 (--------------- YYYY년 MM월 DD일 요일 ---------------)
        date_pattern = re.compile(r'-+ (\d{4})년 (\d{1,2})월 (\d{1,2})일 [월화수목금토일]요일 -+')
        # PC 포맷 메시지 패턴 ([발화자] [오전/오후 HH:MM] 내용)
        message_pattern = re.compile(r'^\[(.+)\] \[(오전|오후) (\d{1,2}):(\d{2})\] (.+)')
    else:
        # 모바일 포맷 날짜 패턴 (YYYY년 MM월 DD일 요일)
        date_pattern = re.compile(r'^(\d{4})년 (\d{1,2})월 (\d{1,2})일 [월화수목금토일]요일')
        # 모바일 포맷 메시지 패턴 (YYYY. MM. DD. 시간, 발화자 : 내용)
        message_pattern = re.compile(r'^(\d{4})\. (\d{1,2})\. (\d{1,2})\. (오전|오후) (\d{1,2}):(\d{2}), (.+) : (.+)')
    
    # 물음표 포함 여부를 확인하는 간단한 함수
    def has_question_mark(text):
        return '?' in text or '？' in text
    
    # 각 라인 분석
    for line in lines:
        line = line.strip()
        
        # 빈 라인은 무시
        if not line:
            continue
        
        # 날짜 라인 확인
        date_match = date_pattern.match(line)
        if date_match:
            year, month, day = date_match.groups()
            current_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            continue
        
        # 메시지 라인 확인
        message_match = message_pattern.match(line)
        if message_match and current_date:
            if is_pc_format:
                # PC 포맷 메시지 파싱
                speaker, am_pm, hour, minute, content = message_match.groups()
                # 날짜 정보는 current_date에서 가져옴
                year, month, day = current_date.split('-')
            else:
                # 모바일 포맷 메시지 파싱
                year, month, day, am_pm, hour, minute, speaker, content = message_match.groups()
            
            # 12시간제 -> 24시간제 변환
            hour = int(hour)
            if am_pm == '오후' and hour < 12:
                hour += 12
            elif am_pm == '오전' and hour == 12:
                hour = 0
            
            # 시간 포맷팅
            time_str = f"{hour:02d}:{minute}"
            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            datetime_str = f"{date_str} {time_str}"
            
            # datetime 객체 생성
            dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            # 물음표 포함 여부 확인
            has_question = has_question_mark(content)
            
            # 글자수 계산
            char_count = len(content)
            
            # 데이터 추가
            data.append({
                'date': date_str,
                'time': time_str,
                'datetime': dt_obj,  # datetime 객체로 저장
                'speaker': speaker,
                'content': content,
                'has_question_mark': has_question,
                'char_count': char_count
            })
    
    # 데이터프레임 생성
    df = pd.DataFrame(data)
    
    # 최근 메시지만 선택
    if len(df) > 0:
        df = df.tail(recent_chat_nums).reset_index(drop=True)
    
    return df

def add_session_features(df, session_timeout_minutes=120, max_session_hours=12):
    """
    세션 분석을 위한 feature들을 추가하는 함수
    
    Parameters:
    df (pd.DataFrame): 기본 필드가 추출된 데이터프레임
    session_timeout_minutes (int): 일반 세션 구분을 위한 타임아웃 시간(분)
    max_session_hours (int): 절대적인 최대 세션 길이(시간)
    
    Returns:
    pd.DataFrame: 세션 분석 feature가 추가된 데이터프레임
    """
    # 최대 세션 시간을 분으로 변환
    max_session_minutes = max_session_hours * 60
    
    # 시간순으로 정렬
    df = df.sort_values(by='datetime')
    
    # 이전 메시지 정보를 저장할 새 컬럼 추가
    df['previous_msg_time'] = df['datetime'].shift(1)
    df['previous_speaker'] = df['speaker'].shift(1)
    df['previous_msg_has_question'] = df['has_question_mark'].shift(1)
    
    # 메시지 간 시간 차이 계산 (분 단위)
    df['time_since_last_msg'] = (df['datetime'] - df['previous_msg_time']).dt.total_seconds() / 60
    
    # 첫 메시지의 경우 NaN 대신 0으로 설정
    df['time_since_last_msg'] = df['time_since_last_msg'].fillna(0)
    
    # 경고 메시지 수정: previous_msg_has_question 을 명시적으로 Boolean 타입으로 변환
    # NaN 값을 False로 처리하여 fillna 대신 명시적 변환 사용
    previous_question_bool = df['previous_msg_has_question'].notna() & df['previous_msg_has_question']
    
    # 세션 시작 여부 결정 (하이브리드 접근법)
    # 1. 첫 번째 메시지는 항상 세션 시작
    # 2. 기존 로직: 이전 메시지로부터 session_timeout_minutes 이상 경과했고, 이전 메시지가 질문이 아닌 경우
    # 3. 최대 임계값: 이전 메시지로부터 max_session_minutes(12시간) 이상 경과하면 무조건 새 세션으로 간주
    df['is_session_start'] = (
        (df.index == 0) |  # 첫 번째 메시지
        ((df['time_since_last_msg'] > session_timeout_minutes) & (~previous_question_bool)) |  # 기존 로직
        (df['time_since_last_msg'] > max_session_minutes)  # 최대 임계값 12시간(720분) 이상 경과
    )
    
    # 세션 ID 할당
    df['session_id'] = df['is_session_start'].cumsum()
    
    # 답장 여부 확인 (발화자가 이전 메시지의 발화자와 다른 경우)
    df['is_reply'] = (df['speaker'] != df['previous_speaker']) & (~df['is_session_start'])
    
    # 답장 시간 계산 (분 단위)
    df['reply_time'] = df.apply(
        lambda row: row['time_since_last_msg'] if row['is_reply'] else None, 
        axis=1
    )
    
    return df


def calculate_conversation_metrics(df):
    """
    대화 분석 지표를 계산하는 함수
    
    Parameters:
    df (pd.DataFrame): 세션 분석 feature가 추가된 데이터프레임
    
    Returns:
    dict: 각종 대화 분석 지표를 담은 딕셔너리
    """
    # 결과를 저장할 딕셔너리
    metrics = {}
    
    # 0. 발화자별 메시지 비율 (전체 메시지 중)
    # 전체 메시지 수
    total_messages = len(df)
    
    # 발화자별 메시지 수 계산
    message_count_by_speaker = df['speaker'].value_counts()
    
    # 전체 메시지 중 발화자별 비율 계산 (%)
    if total_messages > 0:
        message_ratio_by_speaker = (message_count_by_speaker / total_messages) * 100
    else:
        message_ratio_by_speaker = pd.Series(0, index=df['speaker'].unique())
    
    metrics['message_ratio'] = message_ratio_by_speaker
    
    # 1. 발화자별 질문 비율 (전체 질문 중)
    # 전체 질문 메시지 추출
    question_messages = df[df['has_question_mark'] == True]
    
    # 발화자별 질문 수 계산
    question_count_by_speaker = question_messages['speaker'].value_counts()
    
    # 전체 질문 중 발화자별 비율 계산 (%)
    if len(question_messages) > 0:  # 질문이 하나 이상 있는 경우
        question_ratio_by_speaker = (question_count_by_speaker / len(question_messages)) * 100
    else:
        question_ratio_by_speaker = pd.Series(0, index=df['speaker'].unique())
    
    metrics['question_ratio'] = question_ratio_by_speaker
    
    # 2. 발화자별 평균 답장 시간 (분)
    # 답장 메시지만 추출 (is_reply가 True인 메시지)
    reply_messages = df[df['is_reply'] == True]
    
    # 발화자별 평균 답장 시간 계산
    reply_time_by_speaker = reply_messages.groupby('speaker')['reply_time'].mean()
    
    metrics['avg_reply_time'] = reply_time_by_speaker
    
    # 3. 발화자별 평균 메시지 길이 (글자 수)
    # 발화자별 평균 메시지 길이 계산
    message_length_by_speaker = df.groupby('speaker')['char_count'].mean()
    
    metrics['avg_message_length'] = message_length_by_speaker
    
    # 4. 발화자별 대화 시작 비율 (전체 대화 시작 중)
    # 세션 시작 메시지만 추출
    session_start_messages = df[df['is_session_start'] == True]
    
    # 발화자별 대화 시작 횟수 계산
    session_start_by_speaker = session_start_messages['speaker'].value_counts()
    
    # 전체 대화 시작 중 발화자별 비율 계산 (%)
    if len(session_start_messages) > 0:  # 세션 시작이 하나 이상 있는 경우
        session_start_ratio_by_speaker = (session_start_by_speaker / len(session_start_messages)) * 100
    else:
        session_start_ratio_by_speaker = pd.Series(0, index=df['speaker'].unique())
    
    metrics['session_start_ratio'] = session_start_ratio_by_speaker
    
    # 5. 종합 밀당 지수 계산
    # 발화자 목록 추출
    speakers = df['speaker'].unique()
    
    # 지표별 가중치 설정 (모든 지표에 동일한 가중치 부여)
    weight = 0.2  # 5개 지표에 각각 20%씩 할당
    
    # 발화자별 밀당 지수를 저장할 Series 초기화 (float 타입으로 명시)
    mildang_index = pd.Series(0.0, index=speakers, dtype=float)
    
    # 1) 메시지 비율 - 이미 0-100 사이 값
    for speaker in speakers:
        if speaker in message_ratio_by_speaker.index:
            mildang_index[speaker] += message_ratio_by_speaker[speaker] * weight
    
    # 2) 질문 비율 - 이미 0-100 사이 값
    for speaker in speakers:
        if speaker in question_ratio_by_speaker.index:
            mildang_index[speaker] += question_ratio_by_speaker[speaker] * weight
    
    # 3) 평균 답장 시간 - 정규화 필요 (0-100 사이로 변환)
    # 답장 시간이 짧을수록 적극적이므로, 역으로 계산 (100에서 뺌)
    if len(reply_time_by_speaker) > 0:
        max_reply_time = reply_time_by_speaker.max() if not reply_time_by_speaker.empty else 1
        min_reply_time = reply_time_by_speaker.min() if not reply_time_by_speaker.empty else 0
        
        # 최대값과 최소값이 같으면 나눗셈 오류 방지
        reply_time_range = max(max_reply_time - min_reply_time, 1)
        
        for speaker in speakers:
            if speaker in reply_time_by_speaker.index:
                # 0-100 사이로 정규화하고 역으로 계산 (빠른 답장일수록 높은 점수)
                normalized_reply_time = 100 - ((reply_time_by_speaker[speaker] - min_reply_time) / reply_time_range * 100)
                mildang_index[speaker] += normalized_reply_time * weight
    
    # 4) 평균 메시지 길이 - 정규화 필요 (0-100 사이로 변환)
    if len(message_length_by_speaker) > 0:
        max_length = message_length_by_speaker.max() if not message_length_by_speaker.empty else 1
        min_length = message_length_by_speaker.min() if not message_length_by_speaker.empty else 0
        
        # 최대값과 최소값이 같으면 나눗셈 오류 방지
        length_range = max(max_length - min_length, 1)
        
        for speaker in speakers:
            if speaker in message_length_by_speaker.index:
                # 0-100 사이로 정규화
                normalized_length = ((message_length_by_speaker[speaker] - min_length) / length_range * 100)
                mildang_index[speaker] += normalized_length * weight
    
    # 5) 대화 시작 비율 - 이미 0-100 사이 값
    for speaker in speakers:
        if speaker in session_start_ratio_by_speaker.index:
            mildang_index[speaker] += session_start_ratio_by_speaker[speaker] * weight
    
    # 최종 밀당 지수를 저장
    metrics['mildang_index'] = mildang_index
    
    return metrics


def extract_pattern_metrics(file_path, recent_chat_nums=1000):
    """
    카카오톡 대화 파일을 분석하여 패턴 지표를 추출하는 함수
    
    Parameters:
    file_path (str): 카카오톡 대화 파일 경로
    recent_chat_nums (int): 최근 대화 수
    
    Returns:
    dict: 대화 분석 지표를 담은 Python 딕셔너리 (JSON 직렬화 가능한 형태)
    """
    # 카카오톡 대화 파일 파싱
    df = parse_kakao_chat(file_path, recent_chat_nums)
    
    # 세션 분석 feature 추가
    df = add_session_features(df)
    
    # 대화 분석 지표 계산
    metrics = calculate_conversation_metrics(df)
    
    # 결과를 담을 딕셔너리 생성
    result = {}
    
    # 각 지표를 순회하며 JSON 직렬화가 가능한 형태로 변환
    for metric_name, metric_values in metrics.items():
        # pandas Series를 딕셔너리로 변환
        # 실제 발화자 이름을 키로 사용하고 값은 소수점 첫째자리까지만 반올림
        result[metric_name] = {speaker: round(float(value), 1) for speaker, value in metric_values.items()}
    
    # Python 딕셔너리 반환 (이미 JSON 직렬화 가능한 형태)
    return result