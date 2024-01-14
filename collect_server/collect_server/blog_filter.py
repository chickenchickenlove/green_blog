import dateparser
from datetime import date, timedelta


class BaseFilter:
    def apply(self, texts):
        raise NotImplementedError('Not Implemented')


class AlreadyHaveFilter(BaseFilter):

    def __init__(self, date):
        self.date = date

    def apply(self, texts):
        raise NotImplementedError('Not Implemented yet.')


class DatePatternFilter(BaseFilter):

    def __init__(self, pattern):
        self.pattern = pattern

    def apply(self, texts):
        return [text for text in texts if self.pattern.is_match(text)]


class ExpiredDateFilter(BaseFilter):

    def __init__(self, pattern):
        self.expired_date = date.today() - timedelta(days=130)
        self.pattern = pattern

    def apply(self, texts):
        filtered = []
        for text in texts:
            date_strings = self.pattern.find_all(text)
            if self._not_expired(date_strings):
                filtered.append(text)
        return filtered

    def _not_expired(self, date_strings):
        return [date_str for date_str in date_strings if dateparser.parse(date_str).date() > self.expired_date]


class FilterChain:

    filters: list[BaseFilter]

    def __init__(self):
        self.filters = []

    def add_filter(self, custom_filter):
        self.filters.append(custom_filter)

    def apply(self, texts):
        for f in self.filters:
            texts = f.apply(texts)

        return texts