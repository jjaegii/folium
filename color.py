from PIL import Image
from itertools import islice

# (242, 239, 233) = None
# (224, 233, 233) = 큰 건물
# (255, 255, 255) = 도로
# 추가 예정
def count_pixel_colors(image_path):
    image = Image.open(image_path)
    image = image.convert('RGBA') # 이미지를 RGBA 형식으로 변환
    image_data = image.getdata()

    color_count = {}

    for pixel in image_data:
        r, g, b, a = pixel
        if a == 255:
            if (r, g, b) in color_count:
                color_count[(r, g, b)] += 1
            else:
                color_count[(r, g, b)] = 1
    del color_count[(242, 239, 233)] # 공백 컬러 삭제
    
    return color_count

image_path = 'image.png'
color_count = count_pixel_colors(image_path)

sorted_color_count = dict(sorted(color_count.items(), key=lambda x: x[1], reverse=True)) # 내림차순 정렬

sorted_color_count = dict(islice(sorted_color_count.items(), 40))
print(sorted_color_count) # 픽셀 갯수 상위 40개인 RGB 값 딕셔너리만 출력

print()
# 비율 측정
total_pixels = sum(sorted_color_count.values())
color_ratio = {color: count / total_pixels for color, count in sorted_color_count.items()}
for color, ratio in color_ratio.items():
    print(f"{color}: {ratio * 100:.2f}%")

'''
추후 계획은 지도에서 색깔로 구분할 수 있는 index들을 설정할 예정.
그 후 index들의 비율로 학습시켜 clustering할지, classification할지 고민해봐야할듯..
'''