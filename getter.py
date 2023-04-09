import json
import asyncio
import aiohttp
import dateparser
import my_constant

from collections import defaultdict
from secret import ACCESS_TOKEN, BLOG_NAME, OUTPUT

BASE_URL = f'https://www.tistory.com/apis/post/list?access_token={ACCESS_TOKEN}&blogName={BLOG_NAME}&output={OUTPUT}&count=30'
URL_WITH_PAGE = BASE_URL + '&page={}'


async def parse_data(history_dict: defaultdict,
                     res: aiohttp.ClientResponse) -> bool:
    if res.status != 200:
        return False

    text = await res.text()
    contents = json.loads(text)

    # in case of having not 'posts'
    items = contents['tistory']['item']
    if 'posts' not in items:
        return False

    for post in items['posts']:
        parsed_date = dateparser.parse(post['date']).date().strftime(my_constant.DATE_FORMAT)
        history_dict[parsed_date] += 1
    return True


async def get_post_data(session: aiohttp.ClientSession,
                        history_dict: defaultdict,
                        start_page: int) -> None:
    do_continue = True

    futures = [session.request(
        method='get',
        url=URL_WITH_PAGE.format(page_number)) for page_number in range(start_page, start_page + 5)]

    for response in [await f for f in futures]:
        do_continue = await parse_data(history_dict, response)

    if do_continue:
        await get_post_data(session, history_dict, start_page + 5)


async def do_request() -> defaultdict:
    history_dict = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        await get_post_data(session, history_dict, 1)

    return history_dict




# post_history = asyncio.run(do_request())
# print(post_history)
