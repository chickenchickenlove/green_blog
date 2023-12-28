import logging
import re
import asyncio
import aiohttp


from enum import Enum
from typing import Optional
from blog_filter import BaseFilter, AlreadyHaveFilter, DatePatternFilter, FilterChain, ExpiredDateFilter
from collections import defaultdict
from domain import *


class DatePattern(Enum):
    # pattern1 = r'(\d{4})\.(\d{2})\.(\d{2})' # 2023.01.06
    # pattern2 = r'(\d{4})\. (\d{1,2})\. (\d{1,2})'  # 2023. 1. 6, 2023. 10. 19

    pattern1 = r'\d{4}\.\d{2}\.\d{2}'  # 2023.01.06
    pattern2 = r'\d{4}\. \d{1,2}\. \d{1,2}'  # 2023. 1. 6, 2023. 10. 19

    def __new__(cls, reg_pattern):
        obj = object.__new__(cls)
        obj.reg_pattern = re.compile(reg_pattern)
        return obj

    def find_all(self, text: str):
        return self.reg_pattern.findall(text)

    def is_match(self, text: str) -> bool:
        return bool(self.reg_pattern.search(text))


async def get_proper_pattern(session: aiohttp.ClientSession) -> Optional[DatePattern]:
    result = await session.request(method='GET',
                                   url=f'https://ojt90902.tistory.com/category/?page={1}')

    text = await result.text()
    for pattern in DatePattern:
        if pattern.is_match(text):
            return pattern

    return None


async def get_page(session: aiohttp.ClientSession,
                    start_page: int,
                    interval: int,
                    url: str):

    coros = [session.request(method='GET',
                             url=f'{url}/category/?page={page}')
             for page in range(start_page, start_page + interval)]
    responses = await asyncio.gather(*coros)
    texts_coros = [response.text() for response in responses]

    try:
        return await asyncio.gather(*texts_coros)
    except Exception as _:
        logging.warning("fail error")
        return []


async def get_pages(session: aiohttp.ClientSession,
                    start_page: int,
                    interval: int,
                    url: str,
                    filter_chain: FilterChain) -> list[str]:
    ret = []
    for s in range(start_page, 10, interval):
        result = await get_page(session, s, interval, url)
        filtered = filter_chain.apply(result)
        if not filtered:
            break
        ret.extend(filtered)
    return ret



def aggregate_count(sources: list[str], pattern):
    parsed = []
    for source in sources:
        parsed.extend(pattern.find_all(source))

    records = defaultdict(int)
    for p in parsed:
        records[p] += 1

    return records

def insert_db(records, url):


    user, created = User.get_or_create(url=url)

    for posted_date, count in records.items():
        query = UserPost.select().where((UserPost.user == user) & (UserPost.posted_date == posted_date))
        try:
            ret = query.get()
        except Exception as _:
            ret = UserPost.create(user=user, posted_date=posted_date, posted_count=0)

        ret.posted_date = posted_date
        ret.posted_count = count

        ret.save()


async def amain():
    async with aiohttp.ClientSession() as session:
        pattern = await get_proper_pattern(session)
        if pattern is None:
            raise ValueError('Unsupported DateTime or No Posting at all.')

        url = 'https://ojt90902.tistory.com'

        # result = await get_pages(session, 0, 10, 'https://yeonyeon.tistory.com')
        filter_chain = FilterChain()
        filter_chain.add_filter(DatePatternFilter(pattern))
        filter_chain.add_filter(ExpiredDateFilter(pattern))

        result = await get_pages(session, 0, 10, url, filter_chain)

        records = aggregate_count(result, pattern)

        insert_db(records, url)




        print(records)

        # 데이터를 가져온 후, DB Record로 만든다.




        print(len(result))

asyncio.run(amain())
