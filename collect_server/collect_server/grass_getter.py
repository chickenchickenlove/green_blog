import aiohttp
import asyncio
import logging

from blog_filter import FilterChain


class GrassGetter:

    filter_chain: FilterChain

    @staticmethod
    def create(filter_chain: FilterChain):
        self = object.__new__(GrassGetter)
        self.filter_chain = filter_chain
        return self

    async def execute(self, url: str) -> list:
        async with aiohttp.ClientSession() as s:
            return await self._pages(s, 1, 10, url)

    async def _pages(self,
                     session,
                     start_page: int,
                     interval: int,
                     url: str):

        ret = []
        for s in range(start_page, 1000, interval):
            result = await self._page(session, s, interval, url)
            filtered = self.filter_chain.apply(result)
            if not filtered:
                break
            ret.extend(filtered)
        return ret

    async def _page(self,
                    s: aiohttp.ClientSession,
                    start_page: int,
                    interval: int,
                    url: str):

        coros = [s.get(url=f'{url}/category/?page={page}')
                 for page in range(start_page, start_page + interval)]
        responses = await asyncio.gather(*coros)
        texts_coros = [response.text() for response in responses]

        try:
            return await asyncio.gather(*texts_coros)
        except Exception as _:
            logging.warning('fail to collect page from blog.')
            return []