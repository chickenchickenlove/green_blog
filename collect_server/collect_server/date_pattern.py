import re
import aiohttp

# pattern1 = r'\d{4}\.\d{2}\.\d{2}'  # 2023.01.06
# pattern2 = r'\d{4}\. \d{1,2}\. \d{1,2}'  # 2023. 1. 6, 2023. 10. 19

PATTERNS = [
    r'\d{4}\.\d{2}\.\d{2}', # 2023.01.06
    r'\d{4}\. \d{1,2}\. \d{1,2}', # 2023. 1. 6, 2023. 10. 19
]

COMPILED_PATTERN = [re.compile(p) for p in PATTERNS]

class DatePatternFactory:

    @staticmethod
    async def create(url: str):
        patterns = [DatePattern.create(cp) for cp in COMPILED_PATTERN]

        pattern_chain = PatternParseChain.create()
        for pattern in patterns:
            pattern_chain.add(pattern)

        async with aiohttp.ClientSession() as s:
            return await DatePatternFactory.matched_pattern(s, url, pattern_chain)

    @staticmethod
    async def matched_pattern(session: aiohttp.ClientSession, url, pattern_chain):
        formatted_url = f'{url}/category/?page={1}'
        async with session.get(url=formatted_url) as res:
            text = await res.text()
            return pattern_chain.get_matched_pattern(text)


class DatePattern:

    pattern: re.Pattern

    @staticmethod
    def create(reg):
        self = object.__new__(DatePattern)
        self.pattern = reg
        return self

    def find_all(self, text: str):
        return self.pattern.findall(text)

    def is_match(self, text: str) -> bool:
        return bool(self.pattern.search(text))


class PatternParseChain:

    patterns: list[DatePattern]

    @staticmethod
    def create():
        self = object.__new__(PatternParseChain)
        self.patterns = []
        return self

    def add(self, pattern: DatePattern):
        self.patterns.append(pattern)

    def get_matched_pattern(self, text):
        for pattern in self.patterns:
            if pattern.is_match(text):
                return pattern
        return None


class NoMatchedPattern(Exception):
    def __init__(self, message="My custom error has occurred"):
        self.message = message
        super().__init__(self.message)