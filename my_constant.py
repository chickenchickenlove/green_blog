
DATE_FORMAT = '%Y-%m-%d'
TEMPLATE = """\n
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
      <text id="handle" transform="translate(23 32)" fill="{color}" font-size="14" font-family="NotoSansKR-Black, Noto Sans KR" font-weight="800" style="animation-delay:100ms">{handle}</text>""".lstrip("\n").rstrip("\n")


END_FORMAT = """\
  </g>
</svg>"""

# NEMO_TEMPLATE = '\n<rect class="zandi"\
#                   width="15" height="15" rx="4"\
#                   transform="translate({x} {y})" \
#                   fill="{color}"\
#                   style="animation-delay:{delay}ms"/>\
#                   '


NEMO_TEMPLATE = '''      <rect class="zandi" \
width="15" height="15" rx="4"\
transform="translate({x} {y})" \
fill="{color}"\
style="animation-delay:{delay}ms"/>
'''

# NEMO_TEMPLATE = ' ' * 14 + NEMO_BASE_TEMPLATE
print(NEMO_TEMPLATE)