import re

_PATTERNS = [
    (re.compile(r'(token\s*=\s*)\S+', re.IGNORECASE), r'\1***'),
    (re.compile(r'(Authorization:\s*Bearer\s+)\S+', re.IGNORECASE), r'\1***'),
    (re.compile(r'(password\s*[=:]\s*)\S+', re.IGNORECASE), r'\1***'),
    (re.compile(r'(AI_API_KEY\s*=\s*)\S+', re.IGNORECASE), r'\1***'),
    (re.compile(r'(api_key\s*[=:]\s*)\S+', re.IGNORECASE), r'\1***'),
    (re.compile(r'(secret\s*[=:]\s*)\S+', re.IGNORECASE), r'\1***'),
]


def sanitize(line: str) -> str:
    for pattern, repl in _PATTERNS:
        line = pattern.sub(repl, line)
    return line
