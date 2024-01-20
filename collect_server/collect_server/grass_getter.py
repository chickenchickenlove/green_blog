import aiohttp
import asyncio
import logging
from collections.abc import AsyncGenerator

from blog_filter import FilterChain


class GrassGetter:

    filter_chain: FilterChain
    session: aiohttp.ClientSession
    @staticmethod
    def create(filter_chain: FilterChain,
               session: aiohttp.ClientSession):
        self = object.__new__(GrassGetter)
        self.filter_chain = filter_chain
        self.session = session
        return self

    async def execute(self, url: str) -> AsyncGenerator:
        return self._pages(start_page=1, interval=10, url=url)
            # async for result in self._pages(session, start_page=1, interval=10, url=url):
                # return result

    async def _pages(self,
                     *,
                     start_page: int,
                     interval: int,
                     url: str):
        # TODO : Use Async Generator
        # 제네레이터 이용하도록 리팩토링
        for s in range(start_page, 1000, interval):
            result = await self._page(s, interval, url)
            if not (filtered := self.filter_chain.apply(result)):
                break
            yield filtered

    async def _page(self,
                    start_page: int,
                    interval: int,
                    url: str):

        coros = [self.session.get(url=f'{url}/category/?page={page}')
                 for page in range(start_page, start_page + interval)]
        responses = await asyncio.gather(*coros)
        texts_coros = [response.text() for response in responses]

        try:
            return await asyncio.gather(*texts_coros)
        except Exception as _:
            logging.warning('fail to collect page from blog.')
            return []

    # 차라리 async_generator를 제공하는게 나을 듯?
