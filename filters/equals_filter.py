import re
from filter import Filter


class EqualsFilter(Filter):
    def __init__(self, patterns: list[tuple[str, str]]) -> None:
        self.patterns = patterns

    def matches(self, province) -> bool:
        for pattern in self.patterns:
            if re.search(rf'^{pattern[0]}\s*=\s*{pattern[1]}', province.content, re.MULTILINE):
                return True
            
        return False
