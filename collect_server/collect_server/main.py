from fastapi import FastAPI

import uvicorn
from data_parser import ResponseParser
from grass_getter import GrassGetter
from date_pattern import DatePatternFactory
from blog_filter import FilterChain, ExpiredDateFilter, DatePatternFilter, AlreadyHaveFilter

DOMAINS = {
    'tistory': 'tistory.com'
}


async def execute(url, /, short=None):
    pattern = await DatePatternFactory.create(url)

    filters = FilterChain()
    if short:
        filters.add_filter(ExpiredDateFilter(pattern))
    filters.add_filter(DatePatternFilter(pattern))

    result = await GrassGetter.create(filters).execute(url)

    return ResponseParser(pattern).aggregate_count(result)


app = FastAPI()


# curl "localhost:8000/blog?name=ojt90902&domain=tistory"
# https://ojt90902.tistory.com
@app.get("/blog/short")
async def read_items(name, domain):
    url = f'https://{name}.{DOMAINS.get(domain)}'
    result = await execute(url, short=True)
    return {"result": result}


@app.get("/blog/total")
async def read_items(name, domain):
    url = f'https://{name}.{DOMAINS.get(domain)}'
    result = await execute(url, short=False)
    return {"result": result}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
