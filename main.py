import collections

import getter
import graph
import asyncio
from functools import reduce


def get_max_post_per_day(post_history: collections.defaultdict) -> int:
    return reduce(lambda x, y: max(x, y), post_history.values())


def main():
    post_history = asyncio.run(getter.do_request())
    svg = graph.get_svg(get_max_post_per_day(post_history),
                        "Chicken Blog",
                        post_history)

    with open("result1.html", "w") as f:
        f.write(svg)


if __name__ == '__main__':
    main()
