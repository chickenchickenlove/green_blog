# 여기서 필요한 형태의 윤곽을 잡는다.
import collections

import mapping
import datetime
import dateparser

def get_tomorrow(timestamp):
    timedata = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
    tomorrow = timedata + datetime.timedelta(days=1)

    return tomorrow.strftime('%Y-%m-%d')

def get_starting_day():
    today = dateparser.parse('Today')
    weekday = today.isoweekday() & 7
    # Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6
    return today.strftime('%Y-%m-%d'), (today - datetime.timedelta(days=weekday + 119)).strftime('%Y-%m-%d')


# 0인 경우 존재. 이 경우는 전체를 네모나게 만들어야 함.
def normalize_article_num(max_count: int, now_count: int):
    normalized_num = int((now_count / max_count) * 100)
    if normalized_num == 0:
        return 0
    elif normalized_num == 100:
        return 4
    else:
        return (normalized_num//25) + 1


def get_svg(max_count: int,
            record: collections.defaultdict) -> str:
    color_theme = mapping.BLOG_THEMES
    # color_theme = mapping.THEMES['WARM']
    # color_theme = mapping.THEMES1
    svg = """
      <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="350" height="170" viewBox="0 0 350 170">
          <style type="text/css">
              <![CDATA[
                  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=block');
                  @keyframes fadeIn {{
                      0% {{ opacity: 0; }}
                      40% {{ opacity: 0; }}
                      100% {{ opacity: 1; }}
                  }}
                  .zandi {{
                      opacity: 0;
                      animation: fadeIn 0.5s ease-in-out forwards;
                  }}
                  #handle {{
                      opacity: 0;
                      animation: fadeIn 0.5s ease-in-out forwards;
                  }}
                  #tier {{
                      opacity: 0;
                      animation: fadeIn 0.5s ease-in-out forwards;
                  }}
              ]]>
          </style>
          <defs>
              <clipPath id="clip-Gold_-_1">
              <rect width="350" height="170"/>
              </clipPath>
          </defs>
          <g id="zandies">
              <rect id="background" width="349" height="169" rx="14" fill="{bgcolor}" style="stroke-width:0.5; stroke:{border};"/>
              <text id="handle" transform="translate(23 32)" fill="{color}" font-size="14" font-family="NotoSansKR-Black, Noto Sans KR" font-weight="800" style="animation-delay:100ms">{handle}</text>
      """.format(
        border=color_theme['border'],
        bgcolor=color_theme['background'],
        color=color_theme['rect'][5],
        handle="My Blog"
    )

    # 아래에서는 날짜를 돌면서 네모를 생성한다.
    idx = 0
    today, now_in_loop = get_starting_day()

    while True:
        article_num = record[now_in_loop]
        article_degree = normalize_article_num(max_count, article_num)
        color = color_theme['rect'][article_degree]

        nemo = '\n<rect class="zandi"\
                  width="15" height="15" rx="4"\
                  transform="translate({x} {y})" \
                  fill="{color}"\
                  style="animation-delay:{delay}ms"/>\
                  '.format(x=23 + (idx // 7) * 17,
                           y=44 + (idx % 7) * 16,
                           color=color,
                           delay=500 + (idx % 7) * 50 + idx * 4)
        svg += nemo
        idx += 1

        if now_in_loop == today:
            break
        now_in_loop = get_tomorrow(now_in_loop)

    svg += """
          </g>
      </svg>
      """
    return svg


# hello = collections.defaultdict(int)
# hello['2023-04-09'] = 99
# hello['2023-04-08'] = 20
# hello['2023-04-07'] = 30
# hello['2023-04-07'] = 50
# print(get_svg(100, hello))
#
# with open("result.html", "w") as f:
#     f.write(get_svg(100, hello))

