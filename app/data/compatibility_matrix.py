# 케미 점수 매트릭스
COMPATIBILITY_MATRIX = {
            # 분석가(NT) 그룹
            'ENTJ-ENFP': { 'base': 95, 'description': '직진형 리더와 감성형 꿈쟁이의 어긋날 듯 어울리는 케미' },
            'ENTJ-INFP': { 'base': 85, 'description': '불도저와 유니콘 – 강함과 부드러움의 완벽한 조화' },
            'ENTJ-ENFJ': { 'base': 90, 'description': '리더 vs 리더 – 서로를 인정하는 카리스마의 만남' },
            'ENTJ-ESFJ': { 'base': 78, 'description': '불도저와 판다 – 추진력과 배려심의 안정적 케미' },
            
            'ENTP-INFJ': { 'base': 92, 'description': '돌고래와 늑대 – 자유로운 상상력과 깊은 통찰력의 만남' },
            'ENTP-ENFJ': { 'base': 88, 'description': '아이디어 폭발형과 따뜻한 카리스마의 역동적 케미' },
            'ENTP-ISFJ': { 'base': 75, 'description': '돌고래와 토끼 – 활발함과 안정감의 서로 다른 매력' },
            
            'INTJ-ENFP': { 'base': 87, 'description': '올빼미와 꽃사슴 – 계획적 완벽주의자와 자유로운 영혼의 신비한 케미' },
            'INTJ-INFP': { 'base': 83, 'description': '올빼미와 유니콘 – 전략적 사고와 순수한 이상의 조화' },
            'INTJ-ENFJ': { 'base': 80, 'description': '마스터플래너와 카리스마 리더의 완벽한 전략적 파트너십' },
            
            'INTP-ENTP': { 'base': 85, 'description': '고양이와 돌고래 – 사색가와 아이디어 실험가의 지적 교감' },
            'INTP-INFJ': { 'base': 88, 'description': '고양이와 늑대 – 논리적 분석과 직관적 통찰의 깊은 만남' },
            'INTP-ENFJ': { 'base': 82, 'description': '사색형 분석가와 따뜻한 리더의 보완적 케미' },

            # 외교관(NF) 그룹
            'ENFJ-ISFP': { 'base': 85, 'description': '골든리트리버와 나비 – 따뜻한 리더십과 감성적 예술혼의 케미' },
            'ENFJ-ESFP': { 'base': 88, 'description': '카리스마 리더와 자유로운 엔터테이너의 에너지 넘치는 만남' },
            'ENFJ-INFP': { 'base': 90, 'description': '골든리트리버와 유니콘 – 따뜻한 격려와 순수한 꿈의 완벽한 조화' },
            
            'ENFP-ISFJ': { 'base': 82, 'description': '꽃사슴과 토끼 – 자유분방함과 안정감의 달콤한 케미' },
            'ENFP-ESFJ': { 'base': 85, 'description': '감성형 꿈쟁이와 따뜻한 케어베어의 서로를 챙기는 케미' },
            'ENFP-ISFP': { 'base': 88, 'description': '꽃사슴과 나비 – 두 자유로운 영혼의 감성적 교감' },
            
            'INFJ-ISFP': { 'base': 85, 'description': '늑대와 나비 – 신비로운 통찰력과 감성적 예술성의 만남' },
            'INFJ-ESFP': { 'base': 78, 'description': '신비로운 예언자와 자유로운 엔터테이너의 정반대 매력' },
            
            'INFP-ISFP': { 'base': 90, 'description': '유니콘과 나비 – 순수한 두 예술가의 감성적 공명' },

            # 관리자(SJ) 그룹
            'ESTJ-ESFP': { 'base': 72, 'description': '사자와 앵무새 – 체계적 관리자와 자유로운 엔터테이너의 균형' },
            'ESTJ-ISFP': { 'base': 68, 'description': '사자와 나비 – 강한 추진력과 섬세한 감성의 대조적 케미' },
            'ESTJ-ENFP': { 'base': 75, 'description': '체계적 관리자와 감성형 꿈쟁이의 서로를 완성하는 케미' },
            
            'ESFJ-ESTP': { 'base': 80, 'description': '판다와 치타 – 따뜻한 배려와 역동적 에너지의 활발한 케미' },
            'ESFJ-ISFP': { 'base': 88, 'description': '케어베어와 나비 – 따뜻한 보살핌과 감성적 예술성의 조화' },
            'ESFJ-ENFP': { 'base': 85, 'description': '판다와 꽃사슴 – 배려심과 자유로운 영혼의 따뜻한 케미' },
            
            'ISTJ-ESFP': { 'base': 70, 'description': '코끼리와 앵무새 – 신뢰할 수 있는 안정감과 자유로운 활발함의 대비' },
            'ISTJ-ENFP': { 'base': 72, 'description': '신뢰할 수 있는 실무자와 감성형 꿈쟁이의 현실과 이상의 만남' },
            
            'ISFJ-ESTP': { 'base': 75, 'description': '토끼와 치타 – 조용한 배려와 역동적 행동력의 보완적 케미' },
            'ISFJ-ESFP': { 'base': 82, 'description': '수호천사와 자유로운 엔터테이너의 따뜻하고 활발한 케미' },

            # 탐험가(SP) 그룹
            'ESTP-ISFP': { 'base': 80, 'description': '치타와 나비 – 역동적 모험가와 감성적 예술가의 활기찬 케미' },
            'ESTP-ESFP': { 'base': 88, 'description': '치타와 앵무새 – 두 자유로운 모험가의 에너지 폭발 케미' },
            'ESTP-ENFP': { 'base': 85, 'description': '액션형 모험가와 감성형 꿈쟁이의 즉흥적이고 활발한 만남' },
            
            'ESFP-ISFP': { 'base': 85, 'description': '앵무새와 나비 – 자유로운 표현과 감성적 예술성의 창의적 케미' },
            
            'ISTP-ENFP': { 'base': 78, 'description': '카멜레온과 꽃사슴 – 쿨한 기술자와 감성형 꿈쟁이의 신선한 대비' },
            'ISTP-ESFP': { 'base': 80, 'description': '카멜레온과 앵무새 – 쿨함과 활발함의 균형잡힌 케미' },
            
            'ISFP-ENFP': { 'base': 88, 'description': '나비와 꽃사슴 – 감성적 예술가와 감성형 꿈쟁이의 아름다운 공감대' }
        }