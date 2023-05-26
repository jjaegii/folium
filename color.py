from PIL import Image
from itertools import islice
import os, natsort

# (242, 239, 233) = 공백
keywords = {(255,255,255):"도로", (249,178,156):"큰도로", (252, 214, 164):"큰도로", (247, 250, 191):"큰도로", (173, 209, 158):"숲",
                (200, 250, 204):"공원", (170, 224, 203):"운동장", (224, 223, 223):"주거지역", (170, 211, 223):"물", (217, 208, 201):"건물", (255, 255, 229):"학교"}

def select_img(image_path):
    color_count = count_pixel_colors(image_path)
    color_ratio_measure(color_count)

# 각 rgb 값 세는 함수
def count_pixel_colors(image_path):
    image = Image.open(image_path)
    image = image.convert('RGBA')  # 이미지를 RGBA 형식으로 변환
    image_data = image.getdata()

    color_count = {}

    for pixel in image_data:
        r, g, b, a = pixel
        if (r, g, b) not in keywords:
            continue
        index = keywords[(r, g, b)]
        if a == 255:
            if index in color_count:
                color_count[index] += 1
            else:
                color_count[index] = 1
    # del color_count[(242, 239, 233)]  # 공백 컬러 삭제

    return color_count

# 비율 측정
def color_ratio_measure(color_count):
    indexes = {"도로":0, "큰도로":0, "숲":0, "공원":0, "운동장":0, "주거지역":0, "물":0, "건물":0, "학교":0}

    total_pixels = sum(color_count.values())
    color_ratio = {color: count / total_pixels for color,
                count in color_count.items()}
    for color, ratio in color_ratio.items():
        print(f"{color}: {ratio * 100:.2f}%")
        indexes[color] = round(ratio*100, 2)

    # csv 파일로 저장
    keys_list = list(indexes.keys())
    file = open('test2.csv', 'a')

    for i in range(len(keys_list)):
        file.write(str(indexes[keys_list[i]]))
        file.write(",")
    file.write("()\n") # 키워드는 수동 설정

images = natsort.natsorted(os.listdir('imgs'))

for img in images:
    select_img(os.path.join('imgs', img))

'''
추후 계획은 지도에서 색깔로 구분할 수 있는 index들을 (10개 정도?) 설정할 예정.
그 후 index들의 비율로 학습시켜 clustering할지, classification할지 고민해봐야할듯..
'''

'''
test2.csv에서 볼 수 있듯,
input data로는 설정된 rgb 값들의 백분율
output data로는 해당 지도의 특징(ex. 작은도로(골목), 큰도로, 풀or나무 등)
으로 설정하여 classification을 사용하는 것이 맞다고 봄.
'''
