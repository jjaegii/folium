from PIL import Image
from itertools import islice

# (242, 239, 233) = None
# (224, 233, 233) = 큰 건물
# (255, 255, 255) = 도로
# 추가 예정


def count_pixel_colors(image_path):
    image = Image.open(image_path)
    image = image.convert('RGBA')  # 이미지를 RGBA 형식으로 변환
    image_data = image.getdata()

    color_count = {}

    for pixel in image_data:
        r, g, b, a = pixel
        if a == 255:
            if (r, g, b) in color_count:
                color_count[(r, g, b)] += 1
            else:
                color_count[(r, g, b)] = 1
    del color_count[(242, 239, 233)]  # 공백 컬러 삭제

    return color_count


image_path = 'image.png'
color_count = count_pixel_colors(image_path)

sorted_color_count = dict(
    sorted(color_count.items(), key=lambda x: x[1], reverse=True))  # 내림차순 정렬

sorted_color_count = dict(islice(sorted_color_count.items(), 10))
print(sorted_color_count)  # 픽셀 갯수 상위 10개인 RGB 값 딕셔너리만 출력

print()
# 비율 측정
total_pixels = sum(sorted_color_count.values())
color_ratio = {color: count / total_pixels for color,
               count in sorted_color_count.items()}

# ''' value에 따른 오름차순 정렬 '''
# for color, ratio in color_ratio.items():
#     print(f"{color}: {ratio * 100:.2f}%")

# # csv 파일로 저장
# file = open('test.csv', 'w')
# for i in range(1, 10):
#     file.write(f"{i},")
# file.write("10\n")

# for color, ratio in color_ratio.items():
#     file.write(f"{color}:{ratio * 100:.2f},")
# file.write("\n")

''' rgb 값에 따른 오름차순 정렬 '''
file = open('test2.csv', 'w')

# 추후 각 rgb 값들에 대해 index(구분 이름) 설정할 예정
rgbs = [
    (170, 211, 223), (200, 250, 204), (217, 208, 201), (224, 223, 223), (238,
                                                                         238, 238), (242, 218, 217), (247, 250, 191), (247, 250, 191), (255, 255, 229), (255, 255, 255)
]
for i in range(0, 9):
    file.write(f"{rgbs[i]},")
file.write(f"{rgbs[9]}\n")

for color, ratio in sorted(color_ratio.items()):
    print(f"{color}: {ratio * 100:.2f}%")
    # csv 파일로 저장
    file.write(f"{ratio * 100:.2f},")
file.write("\n")


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
