import pandas as pd
import re
from datetime import datetime, timedelta
import concurrent.futures
from typing import List, Dict, Tuple, Optional
import time
from .conversation_pattern import parse_kakao_chat


# OpenAI 클라이언트 설정
from openai import OpenAI
from app.utils.openai_utils import get_openai_client

# 주제 분류를 위한 키워드 사전 정의
TOPIC_KEYWORDS = {
    '일상/감정': [
        '안녕', '잘', '주말', '고생', '감사', '반가', '기분', '날씨', '수고', '행복', '좋은', '감동', 
        '기쁘', '슬프', '화나', '졸리', '피곤', '안부', '보내', '보내셨', '인사', '잘가', '좋아요',
        '신경써', '걱정', '기뻐', '즐거', '웃', '울', '행운', '사랑', '하루', '아침', '저녁', '오전',
        '오후', '잤', '자', '일어났', '피곤', '괜찮', '멘탈', '체력', '상태', '감기', '아프', '병원',
        '추워', '더워', '대단', '감사합니다', '감사해요', '모야', '뭐야', '잉', '이잉'
    ],
    '음식/여행': [
        '식사', '맛집', '먹', '여행', '카페', '치즈', '빵', '케이크', '식당', '맛있', '배고프', '배부르',
        '점심', '저녁', '아침', '메뉴', '음식', '커피', '디저트', '술', '맥주', '소주', '와인', '요리',
        '반찬', '김치', '고기', '삼겹살', '회', '라면', '떡볶이', '피자', '햄버거', '치킨', '삼계탕',
        '여행', '관광', '휴가', '숙소', '호텔', '리조트', '펜션', '에어비앤비', '비행기', '기차', '버스',
        '택시', '여행지', '명소', '가볼', '구경', '보러', '방문', '제주', '해외', '국내', '바다', '산',
        '계곡', '케익', '디저트', '한식', '중식', '일식', '양식'
    ],
    '취미/콘텐츠': [
        '영화', '드라마', '게임', '운동', '취미', '사진', '음악', '공연', '전시', '콘서트', '노래', '앨범',
        '책', '소설', '작가', '뮤지컬', '연극', '공연', '예매', '티켓', '보러', '들었', '감상', '재밌',
        '재미있', '스포츠', '축구', '야구', '농구', '골프', '테니스', '러닝', '조깅', '헬스', '필라테스',
        '요가', '등산', '수영', '자전거', '넷플릭스', '유튜브', '틱톡', '인스타', '페이스북', '트위터',
        '웹툰', '만화', '애니', '팟캐스트', '그림', '스케치', '페인팅', '춤', '댄스', '공예', '뜨개질'
    ],
    '인간관계/연애': [
        '친구', '가족', '연애', '결혼', '아내', '와이프', '남편', '부모', '아버지', '어머니', '할머니',
        '할아버지', '동생', '형', '오빠', '누나', '언니', '아들', '딸', '자녀', '커플', '남친', '여친',
        '남자친구', '여자친구', '썸', '고백', '선물', '데이트', '사귀', '좋아', '사랑', '헤어', '이별',
        '그리워', '보고싶', '축하', '축원', '생일', '기념일', '행복', '싸웠', '사이', '관계', '외롭',
        '친척', '이모', '삼촌', '조카', '생질', '사돈', '연인', '애인', '신혼', '약혼', '청첩장'
    ],
    '일/학업': [
        '회사', '업무', '회의', '사무실', '프로젝트', '세미나', '재택', '차장', '사원', '부장', '과장',
        '대리', '인턴', '팀장', '팀원', '동료', '상사', '부하', '부서', '메일', '이메일', '문서', '보고서',
        '발표', '프레젠', '제안', '기획', '전략', '마케팅', '영업', '개발', '연구', '디자인', '고객',
        '거래처', '거래', '계약', '납품', '수주', '출장', '휴가', '휴직', '사직', '퇴사', '입사', '연봉',
        '월급', '급여', '성과', '평가', '실적', '매출', '이익', '전화', '문의', '택배', '면접'
    ],
    '계획/미래': [
        '계획', '미래', '목표', '취업', '이직', '승진', '진급', '진로', '진학', '유학', '자격증', '공부',
        '시험', '준비', '졸업', '학위', '논문', '석사', '박사', '학사', '장학금', '학교', '대학', '대학원',
        '고시', '공무원', '취준', '면접', '이력서', '자소서', '채용', '스펙', '경력', '인재', '역량',
        '개발', '성장', '진출', '도전', '변화', '성공', '실패', '기회', '가능성', '잠재력', '전망',
        '전략', '방향', '방향성', '의향', '예정', '결심', '결정', '고민', '선택', '선택지'
    ]
}

# 문맥을 고려한 키워드 가중치
KEYWORD_WEIGHTS = {
    '일상/감정': {
        '주말': 2.0, '감사': 1.5, '고생': 1.5, '안녕': 1.2, '보내셨': 2.0,
        '안부': 2.0, '날씨': 1.8, '아프': 1.5, '병원': 1.5, '괜찮': 1.2
    },
    '음식/여행': {
        '식사': 2.0, '맛집': 2.0, '먹': 1.2, '여행': 2.0, '카페': 1.5,
        '치즈': 1.8, '빵': 1.5, '케이크': 1.8, '메뉴': 1.5
    },
    '취미/콘텐츠': {
        '영화': 2.0, '드라마': 2.0, '게임': 2.0, '운동': 1.5, '취미': 2.0,
        '사진': 1.5, '음악': 1.5, '공연': 1.8, '책': 1.5
    },
    '인간관계/연애': {
        '결혼': 2.0, '아내': 2.0, '와이프': 2.0, '남편': 2.0, '가족': 1.8,
        '친구': 1.5, '연애': 2.0, '썸': 1.8, '데이트': 1.8, '신혼': 2.0
    },
    '일/학업': {
        '회사': 1.8, '업무': 2.0, '회의': 2.0, '사무실': 1.8, '프로젝트': 2.0,
        '세미나': 2.0, '재택': 2.0, '차장': 1.5, '사원': 1.5, '이메일': 1.8
    },
    '계획/미래': {
        '계획': 2.0, '미래': 2.0, '목표': 2.0, '취업': 2.0, '이직': 2.0,
        '진로': 2.0, '준비': 1.5, '예정': 1.8, '결정': 1.8
    }
}

# 기본 가중치 값 (위 사전에 없는 키워드에 적용)
DEFAULT_WEIGHT = 1.0

def get_conversation_context(df: pd.DataFrame, idx: int, window_size: int = 2) -> str:
    """
    대화 문맥을 추출하는 함수
    
    Args:
        df: 대화 데이터프레임
        idx: 현재 메시지의 인덱스
        window_size: 앞뒤로 고려할 메시지 수
        
    Returns:
        문맥 정보 문자열
    """
    start_idx = max(0, idx - window_size)
    end_idx = min(len(df), idx + window_size + 1)
    
    # 현재 메시지를 제외한 주변 메시지만 가져오기
    context_msgs = []
    for i in range(start_idx, end_idx):
        if i != idx:  # 현재 메시지는 제외
            context_msgs.append(df.iloc[i]['content'])
    
    return ' '.join(context_msgs)

def keyword_classify_topic_with_confidence(text: str, context: Optional[str] = None) -> Tuple[str, float]:
    """
    키워드 기반 주제 분류 함수 (신뢰도 점수 반환)
    
    Args:
        text: 분류할 텍스트
        context: 추가적인 문맥 정보 (이전/이후 메시지 등)
        
    Returns:
        분류된 주제와 신뢰도의 튜플
    """
    if not text:
        return '미분류', 0.0
    
    # 텍스트 전처리
    combined_text = text
    if context:
        combined_text = f"{text} {context}"
    
    # 각 주제별 점수 계산
    scores = {topic: 0.0 for topic in TOPIC_KEYWORDS.keys()}
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined_text:
                # 키워드 가중치 적용
                weight = KEYWORD_WEIGHTS.get(topic, {}).get(keyword, DEFAULT_WEIGHT)
                # 키워드가 전체 텍스트에 등장하는 횟수 계산
                count = combined_text.count(keyword)
                # 점수 가산
                scores[topic] += count * weight
    
    # 최고 점수 주제와 신뢰도 계산
    max_score = max(scores.values()) if scores.values() else 0
    total_score = sum(scores.values())
    
    if max_score > 0:
        best_topic = max(scores.items(), key=lambda x: x[1])[0]
        # 신뢰도는 최고 점수 / 전체 점수의 비율로 계산
        confidence = max_score / total_score if total_score > 0 else 0
        return best_topic, confidence
    else:
        return '미분류', 0.0

prompt = f"""주어진 대화 내용을 다음 주제 중 하나로 분류해 주세요:
                    - 일상/감정(하루 일과, 날씨, 기분, 안부 인사 등)
                    - 음식/여행(식사 이야기, 맛집, 카페, 여행 계획 등)
                    - 취미/콘텐츠(여가활동, 영화, 드라마, 유튜브, 게임 등)
                    - 인간관계/연애(친구, 연애, 썸, 가족 등 대인 관계 전반)
                    - 일/학업(직장/학교 이야기, 업무, 과제, 시험 등)
                    - 계획/미래(진로, 취업, 이직, 목표 설정, 장기 계획 등)
                    
                    카테고리명만 출력해 주세요. 예: '일상/감정' """

def classify_chat_via_gpt(chat_text: str) -> str:
    client = get_openai_client()
    """
    GPT API를 사용한 주제 분류 함수
    
    Args:
        chat_text: 분류할 텍스트
        
    Returns:
        분류된 주제
    """
    try:
        # OpenAI API 호출
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=prompt,
            input=chat_text,
            max_output_tokens=20,  # 짧은 응답만 필요
            temperature=0.3  # 일관된 분류를 위해 낮은 온도 설정
        )
        
        # 응답 처리
        result = response.output_text.strip()
        
        # 응답이 주제 목록 중 하나인지 확인
        valid_topics = ["일상/감정", "음식/여행", "취미/콘텐츠", "인간관계/연애", "일/학업", "계획/미래"]
        
        for topic in valid_topics:
            if topic in result:
                return topic
        
        # 유효하지 않은 응답인 경우 기본값 반환
        # 키워드 기반 백업 분류 결과를 얻기 위해 신뢰도 0으로 설정
        topic, _ = keyword_classify_topic_with_confidence(chat_text)
        return topic
        
    except Exception as e:
        print(f"GPT API 호출 중 오류 발생: {e}")
        # 오류 발생 시 키워드 기반 분류로 대체
        topic, _ = keyword_classify_topic_with_confidence(chat_text)
        return topic

def hybrid_classify_topic(text: str, context: str = None, confidence_threshold: float = 0.6) -> str:
    """
    키워드 분류와 GPT 분류를 결합한 하이브리드 분류 함수
    
    Args:
        text: 분류할 텍스트
        context: 문맥 정보
        confidence_threshold: GPT 사용 결정 임계값
        
    Returns:
        분류된 주제
    """
    # 1단계: 키워드 기반 분류 시도
    topic, confidence = keyword_classify_topic_with_confidence(text, context)
    
    # 신뢰도가 높으면 키워드 기반 결과 사용
    if confidence >= confidence_threshold:
        return topic
    
    # 2단계: 신뢰도가 낮으면 GPT 사용
    return classify_chat_via_gpt(text)

def process_single_message_hybrid(idx: int, df: pd.DataFrame, use_context: bool = True, 
                                context_window: int = 2, confidence_threshold: float = 0.6) -> str:
    """
    하이브리드 방식으로 단일 메시지 주제 분류 처리 함수 (병렬 처리용)
    
    Args:
        idx: 처리할 메시지 인덱스
        df: 전체 대화 데이터프레임
        use_context: 문맥 사용 여부
        context_window: 문맥 윈도우 크기
        confidence_threshold: 하이브리드 분류 신뢰도 임계값
        
    Returns:
        분류된 주제
    """
    text = df.iloc[idx]['content']
    
    # 문맥 정보 추출 (필요한 경우)
    context = None
    if use_context:
        context = get_conversation_context(df, idx, context_window)
    
    # 하이브리드 주제 분류
    return hybrid_classify_topic(text, context, confidence_threshold)

def classify_topics_hybrid_parallel(df: pd.DataFrame, max_workers: int = 4, use_context: bool = True, 
                                  context_window: int = 2, confidence_threshold: float = 0.6,
                                  batch_size: int = 10) -> pd.DataFrame:
    """
    병렬 처리를 통해 하이브리드 방식으로 데이터프레임의 모든 메시지에 주제를 분류하는 함수
    
    Args:
        df: 대화 데이터프레임
        max_workers: 병렬 처리 워커 수
        use_context: 문맥 사용 여부
        context_window: 문맥 윈도우 크기
        confidence_threshold: 하이브리드 분류 신뢰도 임계값
        batch_size: GPT API 호출을 위한 배치 크기
        
    Returns:
        주제가 추가된 데이터프레임
    """
    result_df = df.copy()
    result_df['topic'] = None
    result_df['confidence'] = None
    
    # 데이터프레임이 비어있는 경우
    if len(df) == 0:
        return result_df
    
    # 1단계: 모든 메시지에 대해 키워드 기반 분류 및 신뢰도 계산
    for idx in range(len(df)):
        text = df.iloc[idx]['content']
        context = get_conversation_context(df, idx, context_window) if use_context else None
        topic, confidence = keyword_classify_topic_with_confidence(text, context)
        
        result_df.loc[idx, 'topic'] = topic
        result_df.loc[idx, 'confidence'] = confidence
    
    # 2단계: 신뢰도가 낮은 메시지만 선별하여 GPT 분류 수행
    low_confidence_indices = result_df[result_df['confidence'] < confidence_threshold].index.tolist()
    
    print(f"총 {len(df)}개 메시지 중 {len(low_confidence_indices)}개 메시지가 신뢰도 낮음 (GPT 분류 필요)")
    
    if low_confidence_indices:
        # 배치 단위로 처리
        batches = [low_confidence_indices[i:i + batch_size] for i in range(0, len(low_confidence_indices), batch_size)]
        
        for batch_idx, batch in enumerate(batches):
            print(f"배치 {batch_idx+1}/{len(batches)} 처리 중 ({len(batch)}개 메시지)")
            
            # 병렬 처리 실행
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 함수에 필요한 인자를 부분 적용
                fn = lambda idx: process_single_message_hybrid(idx, df, use_context, context_window, confidence_threshold)
                
                # 병렬 실행
                topics = list(executor.map(fn, batch))
                
                # 결과 데이터프레임 업데이트
                for i, idx in enumerate(batch):
                    result_df.loc[idx, 'topic'] = topics[i]
            
            # API 속도 제한을 방지하기 위한 짧은 대기
            if batch_idx < len(batches) - 1:
                time.sleep(1)
    
    # 신뢰도 컬럼 제거 (필요하지 않은 경우)
    result_df = result_df.drop('confidence', axis=1)
    
    return result_df

def add_topics_to_kakao_chat_hybrid(df: pd.DataFrame, use_context: bool = True, max_workers: int = 4, 
                                 confidence_threshold: float = 0.6, batch_size: int = 10) -> pd.DataFrame:
    """
    카카오톡 대화 데이터프레임에 하이브리드 방식으로 주제를 추가하는 메인 함수
    
    Args:
        df: 카카오톡 대화 데이터프레임 (parse_kakao_chat 함수의 결과)
        use_context: 문맥 사용 여부
        max_workers: 병렬 처리 워커 수
        confidence_threshold: 하이브리드 분류 신뢰도 임계값
        batch_size: GPT API 호출을 위한 배치 크기
        
    Returns:
        주제가 추가된 데이터프레임
    """
    print(f"메시지 주제 분류 시작 (총 {len(df)}개 메시지)")
    start_time = time.time()
    
    # 병렬 처리로 하이브리드 주제 분류
    result_df = classify_topics_hybrid_parallel(
        df, 
        max_workers=max_workers, 
        use_context=use_context,
        confidence_threshold=confidence_threshold,
        batch_size=batch_size
    )
    
    # 주제별 메시지 수 계산
    topic_counts = result_df['topic'].value_counts()
    
    # # print("\n주제별 메시지 분포:")
    # for topic, count in topic_counts.items():
    #     print(f"  {topic}: {count}개 ({count/len(result_df)*100:.1f}%)")
    
    return result_df

# 새로 추가한 함수들 - 주차별 토픽 분석을 위한 함수들
def get_overall_topic_distribution(df: pd.DataFrame) -> Dict[str, float]:
    """
    전체 대화의 주제별 비율을 계산하는 함수
    
    Args:
        df: 주제가 추가된 대화 데이터프레임
        
    Returns:
        주제별 비율을 담은 딕셔너리 (퍼센트 값)
    """
    if 'topic' not in df.columns:
        raise ValueError("데이터프레임에 'topic' 컬럼이 없습니다. 먼저 주제 분류를 수행해주세요.")
    
    # 주제별 메시지 수 계산
    topic_counts = df['topic'].value_counts()
    total_messages = len(df)
    
    # 주제별 비율 계산 (퍼센트 값)
    topic_distribution = {topic: round((count / total_messages) * 100, 1) for topic, count in topic_counts.items()}
    
    return topic_distribution

def divide_conversations_by_week(df: pd.DataFrame, max_weeks: int = 6) -> List[pd.DataFrame]:
    """
    대화를 주차별로 나누는 함수
    
    Args:
        df: 날짜가 포함된 대화 데이터프레임
        max_weeks: 최대 주 수 (기본값: 6)
        
    Returns:
        주차별로 나눈 데이터프레임 리스트
    """
    if 'date' not in df.columns:
        raise ValueError("데이터프레임에 'date' 컬럼이 없습니다.")
    
    # datetime 형식으로 변환
    df = df.copy()
    if not isinstance(df['date'].iloc[0], datetime):
        df['date'] = pd.to_datetime(df['date'])
    
    # 첫 번째 메시지와 마지막 메시지 사이의 날짜 차이 계산
    start_date = df['date'].min().date()
    end_date = df['date'].max().date()
    
    # 전체 기간 (일) 계산
    total_days = (end_date - start_date).days + 1
    
    # 주 단위로 나누기
    weeks_count = min(max_weeks, (total_days + 6) // 7)  # 최대 max_weeks주까지
    
    weekly_dfs = []
    
    for week in range(weeks_count):
        # 주의 시작일과 종료일 계산
        week_start = start_date + timedelta(days=week * 7)
        week_end = min(start_date + timedelta(days=(week + 1) * 7 - 1), end_date)
        
        # 해당 주의 메시지 필터링
        mask = (df['date'].dt.date >= week_start) & (df['date'].dt.date <= week_end)
        weekly_df = df[mask]
        
        if not weekly_df.empty:
            weekly_dfs.append(weekly_df)
    
    return weekly_dfs

def get_weekly_topic_distributions(df: pd.DataFrame, max_weeks: int = 6) -> Dict[str, Dict[str, float]]:
    """
    주차별 대화 주제 비율을 계산하는 함수
    
    Args:
        df: 주제와 날짜가 포함된 대화 데이터프레임
        max_weeks: 최대 주 수 (기본값: 6)
        
    Returns:
        주차별 주제 비율을 담은 딕셔너리
    """
    if 'topic' not in df.columns or 'date' not in df.columns:
        raise ValueError("데이터프레임에 'topic' 또는 'date' 컬럼이 없습니다.")
    
    # 주차별로 대화 나누기
    weekly_dfs = divide_conversations_by_week(df, max_weeks)
    
    # 주차별 주제 비율 계산
    weekly_distributions = {}
    
    for i, weekly_df in enumerate(weekly_dfs):
        # 주차 이름 생성 (Week 1, Week 2, ...)
        week_name = f"Week {i+1}"
        
        # 해당 주차의 주제 분포 계산
        topic_counts = weekly_df['topic'].value_counts()
        total_messages = len(weekly_df)
        
        # 주제별 비율을 퍼센트로 계산
        # 주제별 비율을 퍼센트로 계산하고 소수점 첫번째 자리까지만 표시
        distribution = {topic: round((count / total_messages) * 100, 1) for topic, count in topic_counts.items()}
        
        weekly_distributions[week_name] = distribution
    
    return weekly_distributions

def analyze_chat_topic_distribution(df: pd.DataFrame, use_context: bool = True,
                                    max_workers: int = 4, confidence_threshold: float = 0.6,
                                    batch_size: int = 10, max_weeks: int = 6) -> Dict[str, Dict]:
    """
    대화 데이터에서 전체 및 주차별 토픽 분포를 분석하는 메인 함수
    
    Args:
        df: 대화 데이터프레임 (날짜 컬럼 필요)
        use_context: 문맥 사용 여부
        max_workers: 병렬 처리 워커 수
        confidence_threshold: 하이브리드 분류 신뢰도 임계값
        batch_size: GPT API 호출을 위한 배치 크기
        max_weeks: 분석할 최대 주 수
        
    Returns:
        전체 및 주차별 토픽 분포를 담은 딕셔너리
    """
    # 1. 주제 분류
    df_with_topics = add_topics_to_kakao_chat_hybrid(
        df,
        use_context=use_context,
        max_workers=max_workers,
        confidence_threshold=confidence_threshold,
        batch_size=batch_size
    )
    
    # 2. 전체 주제 분포 계산
    overall_distribution = get_overall_topic_distribution(df_with_topics)
    
    # 3. 주차별 주제 분포 계산
    weekly_distributions = get_weekly_topic_distributions(df_with_topics, max_weeks)
    
    # 4. 결과 딕셔너리 생성
    result = {
        "overall_distribution": overall_distribution,
        "weekly_distributions": weekly_distributions
    }
    
    return result


# 메인 실행 함수
def extract_topic_metrics(chat_file_path: str, max_weeks: int = 6):
    """
    카카오톡 대화 파일에서 주제 분석을 실행하는 메인 함수
    
    Args:
        chat_file_path: 카카오톡 채팅 내보내기 텍스트 파일 경로
        max_weeks: 분석할 최대 주 수
    
    Returns:
        전체 및 주차별 토픽 분포를 담은 딕셔너리
    """
    # 1. 카카오톡 채팅 파싱
    print(f"카카오톡 채팅 파일 파싱 중: {chat_file_path}")
    df = parse_kakao_chat(chat_file_path)
    
    if df.empty:
        print("파싱된 메시지가 없습니다.")
        return {"overall_distribution": {}, "weekly_distributions": {}}
    
    print(f"총 {len(df)}개 메시지 파싱 완료")
    
    # 2. 주제 분석 실행
    result = analyze_chat_topic_distribution(
        df,
        use_context=True,
        max_workers=4,
        confidence_threshold=0.35,
        batch_size=10,
        max_weeks=max_weeks
    )
    
    # 3. 결과 출력
    # print("\n전체 대화 주제 분포:")
    # for topic, percentage in result["overall_distribution"].items():
    #     print(f"  {topic}: {percentage:.1f}%")
    
    # print("\n주차별 대화 주제 분포:")
    # for week, distribution in result["weekly_distributions"].items():
    #     print(f"\n{week}:")
    #     for topic, percentage in distribution.items():
    #         print(f"  {topic}: {percentage:.1f}%")
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("사용법: python topic_analysis.py <카카오톡_채팅파일> [최대_주_수(기본값=6)]")
        sys.exit(1)
    
    chat_file_path = sys.argv[1]
    max_weeks = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    
    result = main(chat_file_path, max_weeks)
    
    # 결과를 딕셔너리 형태로 반환
    print("\n분석 결과 딕셔너리:")
    print(result)