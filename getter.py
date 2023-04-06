import json
import asyncio
import aiohttp
import dateparser

from collections import defaultdict

from secret import ACCESS_TOKEN, BLOG_NAME, OUTPUT



base_url = f'https://www.tistory.com/apis/post/list?access_token={ACCESS_TOKEN}&blogName={BLOG_NAME}&output={OUTPUT}&count=30'
url_with_page = base_url + '&page={}'

async def get_post_data(post_history, start_index):

    async with aiohttp.ClientSession() as session:
        futures = [session.request(
                        method='get',
                        url=url_with_page.format(index)) for index in range(start_index, start_index + 5)]

        responses = [await f for f in futures]

        flag = True

        for res in responses:

            if res.status != 200:
                flag = False
                continue

            text = await res.text()
            contents = json.loads(text)

            #  post가 없을 수도 있음.
            items = contents['tistory']['item']
            if 'posts' not in items:
                flag = False
                continue

            posts = contents['tistory']['item']['posts']


            for post in posts:
                d = post['date']
                parsed_date = dateparser.parse(d)
                isoweekday = parsed_date.isoweekday()

                post_history[parsed_date.date()] += 1

        print(post_history)
        if flag :
            await get_post_data(post_history, start_index + 5)






async def do_request():
    post_history = defaultdict(int)
    await get_post_data(post_history, 1)
    print(post_history)
    print("ASH1")

asyncio.run(do_request())



print("ASH2")