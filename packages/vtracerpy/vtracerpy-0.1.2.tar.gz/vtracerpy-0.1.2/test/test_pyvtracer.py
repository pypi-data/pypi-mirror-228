from vtracerpy import image_to_svg
import cv2

def test_bw_image_to_svg():
    img = cv2.imread('test/mask.png')
    result = image_to_svg(img)
    with open("test/mask_bw.svg", encoding="UTF-8") as f:
        svg = f.read()
    assert result == svg

def test_color_image_to_svg():
    img = cv2.imread('test/mask.png')
    result = image_to_svg(img,colormode='color')
    with open("test/mask_color.svg", encoding="UTF-8") as f:
        svg = f.read()
    assert result == svg