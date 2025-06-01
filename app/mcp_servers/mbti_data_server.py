# mcp_servers/mbti_data_server.py
from typing import Dict, List

class MBTIDataServer:
    """현재 app/data/ 폴더의 데이터를 MCP 서버로 제공"""
    
    def __init__(self):
        # 기존 데이터 import
        from app.data.mbti_characters import MBTI_CHARACTERS
        from app.data.compatibility_matrix import COMPATIBILITY_MATRIX
        from app.data.warning_patterns import WARNING_PATTERNS, SPECIAL_WARNINGS
        
        self.mbti_characters = MBTI_CHARACTERS
        self.compatibility_matrix = COMPATIBILITY_MATRIX
        self.warning_patterns = WARNING_PATTERNS
        self.special_warnings = SPECIAL_WARNINGS
    
    async def get_character_info(self, mbti: str) -> Dict:
        """MBTI 캐릭터 정보 조회"""
        return self.mbti_characters.get(mbti, {})
    
    async def get_compatibility_score(self, mbti1: str, mbti2: str) -> Dict:
        """케미 점수 조회"""
        key1 = f"{mbti1}-{mbti2}"
        key2 = f"{mbti2}-{mbti1}"
        return self.compatibility_matrix.get(key1) or self.compatibility_matrix.get(key2) or {}
    
    async def get_warning_patterns(self, category: str) -> List[str]:
        """위험 신호 패턴 조회"""
        return self.warning_patterns.get(category, [])
    
    async def get_special_warning(self, mbti1: str, mbti2: str) -> str:
        """특별 위험 신호 조회"""
        key1 = f"{mbti1}-{mbti2}"
        key2 = f"{mbti2}-{mbti1}"
        return self.special_warnings.get(key1) or self.special_warnings.get(key2) or ""

# 테스트용 클라이언트
class MBTIDataClient:
    """MCP 서버 역할을 하는 클라이언트 (실제로는 같은 프로세스에서 동작)"""
    
    def __init__(self):
        self.server = MBTIDataServer()
    
    async def get_character_info(self, mbti: str) -> Dict:
        return await self.server.get_character_info(mbti)
    
    async def get_compatibility_score(self, mbti1: str, mbti2: str) -> Dict:
        return await self.server.get_compatibility_score(mbti1, mbti2)
    
    async def get_warning_patterns(self, category: str) -> List[str]:
        return await self.server.get_warning_patterns(category)
    
    async def get_special_warning(self, mbti1: str, mbti2: str) -> str:
        return await self.server.get_special_warning(mbti1, mbti2)