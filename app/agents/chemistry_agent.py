# app/agents/chemistry_agent.py
import random
from typing import Dict, List
from app.mcp_servers.mbti_data_server import MBTIDataClient
from app.utils.josa_utils import _get_josa
from app.utils.validata_mbti_type import validate_mbti_type

class ChemistryAgent:
    """케미 분석 전문 Agent"""
    
    def __init__(self):
        self.mcp_client = MBTIDataClient()
        self.name = "케미 분석 전문가"
    
    async def analyze_chemistry(self, user_mbti: str, partner_mbti: str, 
                              user_name: str = "OO", partner_name: str = "OO", 
                              analysis_type: str = "predicted") -> Dict:
        """케미 분석 수행 - 기존 generate_chemistry_analysis와 동일한 기능"""
        
        # 1. MCP 서버에서 케미 점수 가져오기
        compatibility_info = await self.mcp_client.get_compatibility_score(user_mbti, partner_mbti)
        
        if compatibility_info:
            score = compatibility_info['base']
            description = compatibility_info['description']
        else:
            # 기본값 처리
            user_char = await self.mcp_client.get_character_info(user_mbti)
            partner_char = await self.mcp_client.get_character_info(partner_mbti)
            score = 75
            description = ""
        
        # 2. 점수 설명 생성
        score_desc = self._get_score_description(score)
        
        # 3. 위험 신호 생성
        warning = await self._generate_warning_signal(user_mbti, partner_mbti, score)
        
        # 4. 캐릭터 정보 가져오기
        user_char = await self.mcp_client.get_character_info(user_mbti)
        partner_char = await self.mcp_client.get_character_info(partner_mbti)
        
        user_animal = user_char.get('animal', '')
        partner_animal = partner_char.get('animal', '')
        
        # type_description = "실제 MBTI 기반" if analysis_type == 'original' else "대화 분석 기반 예측"
        
        user_josa = _get_josa(user_name, "and")
        user_animal_josa = _get_josa(user_animal, "and")
        partner_josa = _get_josa(partner_name, "subject")
        
        user_josa = _get_josa(user_name, "and")
        user_animal_josa = _get_josa(user_animal, "and")
        partner_josa = _get_josa(partner_name, "subject")
        
        chemistry_patterns = [
        f"**{user_animal}({user_name}){user_animal_josa} {partner_animal}({partner_name})의 특별한 만남**",
        f"**{user_name}{user_josa} {partner_name}: {user_animal}{user_animal_josa} {partner_animal}의 독특한 조합**",
        f"**{user_animal}{user_animal_josa} {partner_animal}가 만나면? {user_name}{user_josa} {partner_name}의 케미**",
        f"**{user_name}({user_animal}) ❤️ {partner_name}({partner_animal})의 궁합**"
    ]


        return {
            "analysis_type": analysis_type,
            "partner_mbti": partner_mbti,
            "chemistry_score": score,
            "chemistry_description": description if description else random.choice(chemistry_patterns),
            "score_summary": f"**우리의 케미 점수: {score}점! ({score_desc}) [{type_description}]**",
            "warning_signal": f"⚠️ **위험 신호:** {warning}",
            "character_info": {
                "user": user_char,
                "partner": partner_char
            }
        }
    
    def _get_score_description(self, score: int) -> str:
        """점수 기반 설명 생성 - 기존 get_score_description과 동일"""
        descriptions = {
            90: ['완벽한 밸런스 조합! ✨', '환상의 케미! 🔥', '운명적 만남! 💫'],
            80: ['훌륭한 파트너십! 🤝', '서로를 완성하는 케미! 🌟', '최고의 조합! 💝'],
            70: ['좋은 케미! 😊', '균형잡힌 관계! ⚖️', '서로 다른 매력! 🎭'],
            60: ['성장하는 케미! 🌱', '흥미로운 조합! 🎪', '도전적인 케미! 💪'],
            50: ['새로운 경험! 🚀', '배움의 기회! 📚', '특별한 만남! ⭐']
        }
        
        for threshold in sorted(descriptions.keys(), reverse=True):
            if score >= threshold:
                return random.choice(descriptions[threshold])
        return '새로운 경험! 🚀'
    
    async def _generate_warning_signal(self, mbti1: str, mbti2: str, score: int) -> str:
        """위험 신호 생성 - 기존 generate_warning_signal과 동일"""
        
        # 1. 특별 위험 신호 확인
        special_warning = await self.mcp_client.get_special_warning(mbti1, mbti2)
        if special_warning:
            return special_warning
        
        # 2. 점수 기반 카테고리 결정
        if score >= 85:
            category = 'high_score'
        elif score >= 70:
            category = 'medium_score'
        else:
            category = 'low_score'
        
        # 3. 해당 카테고리 패턴 가져오기
        patterns = await self.mcp_client.get_warning_patterns(category)
        return random.choice(patterns) if patterns else "특별한 주의사항이 없습니다"

    async def analyze_multiple_chemistry(self, result: Dict) -> List[Dict]:
        """여러 케미 분석 - 기존 _add_chemistry_analysis와 동일한 기능"""
        
        profile_data = result.get('profile', {})
        mbti_prediction = result.get('mbti_prediction', {})
        
        user_mbti = profile_data.get('user_mbti')
        user_name = profile_data.get('user_name', 'OO')
        partner_name = profile_data.get('partner_name', '상대방')
        partner_mbti_from_profile = profile_data.get('partner_mbti', '').strip()
        
        chemistry_analyses = []
        
        # Original 케미 분석
        if (partner_mbti_from_profile and 
            mbti_prediction.get('original') and 
            mbti_prediction['original'].get('type')):
            
            original_mbti = mbti_prediction['original']['type']
            original_mbti = validate_mbti_type(original_mbti)
            if user_mbti and original_mbti:
                original_chemistry = await self.analyze_chemistry(
                    user_mbti, original_mbti, user_name, partner_name, 'original'
                )
                original_chemistry['title'] = f"원래 MBTI ({original_mbti})와의 케미"
                chemistry_analyses.append(original_chemistry)
        
        # Predicted 케미 분석
        if (mbti_prediction.get('predict') and 
            mbti_prediction['predict'].get('type')):
            
            predicted_mbti = mbti_prediction['predict']['type']
            if user_mbti and predicted_mbti:
                predicted_chemistry = await self.analyze_chemistry(
                    user_mbti, predicted_mbti, user_name, partner_name, 'predicted'
                )
                predicted_chemistry['title'] = f"예측 MBTI ({predicted_mbti})와의 케미"
                chemistry_analyses.append(predicted_chemistry)
        
        return chemistry_analyses