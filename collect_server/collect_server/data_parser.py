import dateparser
from collections import defaultdict
from date_pattern import DatePattern


class ResponseParser:

    def __init__(self, pattern: DatePattern):
        self.pattern = pattern

    def aggregate_count(self, sources: list[str]):
        parsed = []
        for source in sources:
            texts = self.pattern.find_all(source)
            parsed_texts = [dateparser.parse(t).strftime('%Y-%m-%d') for t in texts]
            parsed.extend(parsed_texts)

        records = defaultdict(int)
        for p in parsed:
            records[p] += 1

        return records
