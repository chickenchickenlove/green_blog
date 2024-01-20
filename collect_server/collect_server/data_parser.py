import dateparser
from collections import defaultdict
from date_pattern import DatePattern
from collections.abc import AsyncGenerator


class ResponseParser:

    def __init__(self, pattern: DatePattern, source_generator: AsyncGenerator):
        self.pattern = pattern
        self.sources = source_generator

    async def aggregate_count(self):
        records = defaultdict(int)
        async for parsed in self._aggregate_internal():
            for p in parsed:
                records[p] += 1
        return records

    async def _aggregate_internal(self):
        async for source in self.sources:
            for texts in self._aggregate_each(source):
                yield [dateparser.parse(t).strftime('%Y-%m-%d') for t in texts]

    def _aggregate_each(self, source):
        for texts in [self.pattern.find_all(s) for s in source]:
            yield texts


