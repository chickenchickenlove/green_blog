import imgkit

# HTML 파일의 경로
html_file_path = "result1.html"

# 이미지로 저장할 파일의 경로
image_file_path = "example.png"

# imgkit을 사용하여 HTML 파일을 이미지로 변환
imgkit.from_file(html_file_path, image_file_path)