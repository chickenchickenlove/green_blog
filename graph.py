import collections
import mapping
import datetime
import dateparser
import my_constant

# Reference : https://github.com/mazassumnida/mazandi/blob/main/main.py
# I completed this code by modifying the code shown in the reference, using it as a base.


def get_tomorrow(timestamp) -> str:
    timedata = datetime.datetime.strptime(timestamp, my_constant.DATE_FORMAT)
    tomorrow = timedata + datetime.timedelta(days=1)

    return tomorrow.strftime(my_constant.DATE_FORMAT)


def get_end_day() -> str:
    today = dateparser.parse('Today').strftime(my_constant.DATE_FORMAT)
    return get_tomorrow(today)


def get_starting_day() -> str:
    today = dateparser.parse('Today')
    weekday = today.isoweekday() & 7
    # Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6
    return (today - datetime.timedelta(days=weekday + 119)).strftime(my_constant.DATE_FORMAT)


def normalize_article_num(max_count: int, now_count: int) -> int:
    normalized_num = int((now_count / max_count) * 100)
    if normalized_num == 0:
        return 0
    elif normalized_num == 100:
        return 4
    else:
        return (normalized_num // 25) + 1


def get_svg(max_count: int,
            box_name: str,
            record: collections.defaultdict) -> str:

    # get Color Theme
    color_theme = mapping.BLOG_THEMES

    # get SVG Template
    svg = my_constant.TEMPLATE.format(
        border=color_theme['border'],
        bgcolor=color_theme['background'],
        color=color_theme['rect'][5],
        handle=box_name
    )

    # get NemoBlock from Blog Posting.
    nemo_list = get_nemo_svg_list([],
                                  record,
                                  color_theme,
                                  get_starting_day(),
                                  max_count,
                                  0,
                                  get_end_day())

    # Complete Nemo
    nemo_svg = ''.join(nemo_list)
    svg = ''.join([svg, nemo_svg])
    svg += """
          </g>
      </svg>
      """
    return svg


def get_position(idx: int, color: str):
    return {
        'x': 23 + (idx // 7) * 17,
        'y': 44 + (idx % 7) * 16,
        'color': color,
        'delay': 500 + (idx % 7) * 50 + idx * 4
    }


def get_nemo_svg_list(nemo_list: list,
                      record: collections.defaultdict,
                      color_theme: dict,
                      now_in_loop: str,
                      max_count: int,
                      idx: int,
                      end: str):
    if end == now_in_loop:
        return nemo_list

    article_count = record[now_in_loop]
    normalize_article_count = normalize_article_num(max_count, article_count)
    color = color_theme['rect'][normalize_article_count]

    nemo = my_constant.NEMO_TEMPLATE.format(
        **get_position(idx, color))

    nemo_list.append(nemo)

    get_nemo_svg_list(nemo_list,
                      record,
                      color_theme,
                      get_tomorrow(now_in_loop),
                      max_count,
                      idx + 1,
                      end)
    return nemo_list
