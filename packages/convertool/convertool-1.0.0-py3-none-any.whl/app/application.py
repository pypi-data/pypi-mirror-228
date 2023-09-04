import os
import cv2


# cooltool --input /Users/geolchoi/Downloads/cars.jpeg --output ./output/gray.jpg
def convert_to_grayscale(input_path, output_path):
    input_img = cv2.imread(input_path)
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(output_path, gray)
    return
