# app/agents/mbti_analyzer_agent.py
import json
import asyncio
from typing import Dict
from app.utils.openai_utils import get_openai_client
from app.templates.prompts import PROMPT, SYSTEM_MESSAGE
from app.utils.json_utils import result2json
from app.agents.chemistry_agent import ChemistryAgent

class MBTIAnalyzerAgent:
    """메인 MBTI 분석 Agent - 기존 analyze_mbti_personality 함수를 Agent로 전환"""
    
    def __init__(self):
        self.name = "MBTI 분석 전문가"
        self.chemistry_agent = ChemistryAgent()
    
    async def analyze_personality(self, profile: str, content: str) -> str:
        """
        현재 analyze_mbti_personality와 완전히 동일한 기능
        OpenAI 호출 -> JSON 파싱 -> 케미 분석 추가
        """
        
        # 1. OpenAI 클라이언트 가져오기 (기존과 동일)
        client = get_openai_client()
        
        # 2. 프롬프트 생성 (기존과 동일)
        prompt = PROMPT.format(profile=profile, content=content)
        
        # 3. OpenAI API 호출 (기존과 완전히 동일)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        
        gpt_result = response.choices[0].message.content
        
        try:
            # 4. JSON 파싱 (기존과 동일)
            result = result2json(gpt_result)
            
            if isinstance(result, dict):
                # 5. Original 섹션 제거 로직 (기존과 동일)
                result = await self._handle_original_section(result)
                
                # 6. 케미 분석 추가 (Agent를 통해 처리)
                result = await self._add_chemistry_analysis_with_agent(result)
                
                return json.dumps(result, ensure_ascii=False, indent=2)
            
            return gpt_result
            
        except Exception as e:
            print(f"Error processing result: {e}")
            return gpt_result
    
    async def _handle_original_section(self, result: Dict) -> Dict:
        """Original 섹션 처리 로직 - 기존과 동일"""
        profile_data = result.get('profile', {})
        partner_mbti_from_profile = profile_data.get('partner_mbti', '').strip()
        
        if not partner_mbti_from_profile:
            mbti_prediction = result.get('mbti_prediction', {})
            if 'original' in mbti_prediction:
                print("⚠️ 상대방 MBTI가 프로필에 없으므로 original 섹션을 제거합니다.")
                del mbti_prediction['original']
        
        return result
    
    async def _add_chemistry_analysis_with_agent(self, result: Dict) -> Dict:
        """Chemistry Agent를 통한 케미 분석 추가"""
        
        # Chemistry Agent에게 여러 케미 분석 요청
        chemistry_analyses = await self.chemistry_agent.analyze_multiple_chemistry(result)
        
        if chemistry_analyses:
            result['chemistry_analysis'] = chemistry_analyses
        
        return result

# 현재 코드와의 호환성을 위한 래퍼 함수
def analyze_mbti_personality_with_agent(profile: str, content: str) -> str:
    """기존 함수와 동일한 인터페이스를 제공하는 래퍼"""
    async def run_analysis():
        agent = MBTIAnalyzerAgent()
        return await agent.analyze_personality(profile, content)
    
    # asyncio를 사용해서 동기 함수처럼 실행
    return asyncio.run(run_analysis())