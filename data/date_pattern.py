import re


# pattern1 = r'\d{4}\.\d{2}\.\d{2}'  # 2023.01.06
# pattern2 = r'\d{4}\. \d{1,2}\. \d{1,2}'  # 2023. 1. 6, 2023. 10. 19

class DatePattern:

    pattern: re.Pattern

    @staticmethod
    def create(reg):
        self = object.__new__(DatePattern)
        self.pattern = re.compile(reg)
        return self

    def find_all(self, text: str):
        return self.pattern.findall(text)

    def is_match(self, text: str) -> bool:
        return bool(self.pattern.search(text))


class PatternParseChain:

    patterns: list[DatePattern]

    @staticmethod
    def create():
        return object.__new__(PatternParseChain)

    def add(self, pattern: DatePattern):
        self.patterns.append(pattern)

    def get_matched_pattern(self, text):
        for pattern in self.patterns:
            if pattern.is_match(text):
                return pattern
        raise NoProperPattern(f'There is no proper pattern for {text}')


class NoProperPattern(Exception):
    def __init__(self, message="My custom error has occurred"):
        self.message = message
        super().__init__(self.message)