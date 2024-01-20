import aiohttp
from fastapi import FastAPI

import uvicorn
from data_parser import ResponseParser
from grass_getter import GrassGetter
from date_pattern import DatePatternFactory
from blog_filter import FilterChain, ExpiredDateFilter, DatePatternFilter, AlreadyHaveFilter

DOMAINS = {
    'tistory': 'tistory.com'
}

# TODO: AsyncGenerator 사용 시, 너무 느림. 아마 ClientSession 쪽의 I/O 문제인 듯.
# I/O는 가급적이면 제네레이터 안 쓰는 방향으로?

async def execute(url, /, short=None):
    pattern = await DatePatternFactory.create(url)

    filters = FilterChain()
    if short:
        filters.add_filter(ExpiredDateFilter(pattern))
    filters.add_filter(DatePatternFilter(pattern))

    async with aiohttp.ClientSession() as s:
        generator = await GrassGetter.create(filters, s).execute(url)

        # TODO: Use http2 Stream if needed.
        parser = ResponseParser(pattern, generator)
        result = await parser.aggregate_count()
    print(result)
    print(sum(result.values()))

    return result


app = FastAPI()


# curl "localhost:8000/blog?name=ojt90902&domain=tistory"
# https://ojt90902.tistory.com
@app.get("/blog/short")
async def read_items(name, domain):
    url = f'https://{name}.{DOMAINS.get(domain)}'
    result = await execute(url, short=True)
    return {"result": result}

# curl "localhost:8000/blog/total?name=ojt90902&domain=tistory"
@app.get("/blog/total")
async def read_items(name, domain):
    url = f'https://{name}.{DOMAINS.get(domain)}'
    result = await execute(url, short=False)
    return {"result": result}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
