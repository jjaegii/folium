from PIL import Image

# (242, 239, 233) = None
# (224, 233, 233) = 큰 건물
# (255, 255, 255) = 도로
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

sorted_color_count = sorted(color_count.items(), key=lambda x: x[1], reverse=True) # 내림차순 정렬

print(sorted_color_count[:40]) # 픽셀 갯수 상위 40개인 RGB 값 딕셔너리만 출력