"""JSON 처리 유틸리티"""

import re
import json

def result2json(gpt_result):
    """GPT 결과를 JSON으로 변환"""
    match = re.search(r'({[\s\S]+})', gpt_result)
    if match:
        json_str = match.group(1)
        
        def fix_newlines_in_json(s):
            def replacer(match):
                return match.group(0).replace('\n', '\\n')
            return re.sub(r'"(.*?)"', replacer, s, flags=re.DOTALL)
        
        r = fix_newlines_in_json(json_str)
        try:
            result = json.loads(r)
            return result
        except json.JSONDecodeError:
            return gpt_result
    return gpt_result