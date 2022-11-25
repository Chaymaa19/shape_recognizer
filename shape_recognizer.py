import cv2
import matplotlib.pyplot as plt
import numpy as np
from color_ranges.color_dict import color_dictionary
import argparse


def extract_colour(image, function, color_range=None):
    new_image = np.empty_like(image)
    dim1, dim2, _ = new_image.shape
    for i in range(dim1):
        for j in range(dim2):
            elem = list(image[i,j])
            if function(elem, color_range) == True:
                new_image[i,j] = image[i,j]
            else:
                new_image[i,j] = [255,255,255]
    return new_image

def is_color(pixel, color_range):
    return pixel in color_range

def is_orange(pixel, color_range=None):
    return pixel == [48, 116, 255]

def detect_shapes(image):
    image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_thresh = cv2.threshold(image_bw, 250, 255, cv2.THRESH_BINARY_INV)[1]
    canny_img = cv2.Canny(image_bw, 85, 255)
    result = cv2.bitwise_xor(img_thresh, canny_img)
    contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

def count_shapes(contours):
    num_shapes = 0
    for contour in contours:
        shape_area = cv2.contourArea(contour)
        if shape_area > 250:
            num_shapes += 1
    return num_shapes

def count_logos(template, image):
    h, w = template.shape[:2]
    method = cv2.TM_CCOEFF_NORMED
    threshold = 0.187
    num_logos = 0
    max_val = 1
    while max_val > threshold:
        res = cv2.matchTemplate(image, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        num_logos +=1

        image[max_loc[1]:max_loc[1]+h+1:, max_loc[0]:max_loc[0]+w+1, 0] = 255    
        image[max_loc[1]:max_loc[1]+h+1:, max_loc[0]:max_loc[0]+w+1, 1] = 255  
        image[max_loc[1]:max_loc[1]+h+1:, max_loc[0]:max_loc[0]+w+1, 2] = 255

    return num_logos    


def show_results(colors, shapes, num_lleidahack_logos):
    print("Classificació:")
    print("----------- COLOR ------------")
    print("Vermelles:\t ", colors["red"])
    print("Verdes:\t\t ", colors["green"])
    print("Blaves:\t\t ",colors["blue"])

    print("----------- FORMES -----------")
    print("Triangles:\t ",shapes["triangle"])
    print("Quadrats:\t ",shapes["square"])
    print("Rectangles:\t ",shapes["rectangle"])
    print("Cercles:\t ",shapes["circle"])

    print("------ LOGOS LLEIDAHACK ------")
    print(f"Logos:\t\t ", num_lleidahack_logos)

def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("image_path", help="Path of a png file with shapes and logos to identify.")
    return parser.parse_args(args=argv)

def main(argv=None):
    args = parse_arguments(argv)
    image = cv2.imread(args.image_path)
    shapes = {"circle": 0, "square": 0, "rectangle": 0, "triangle":0}
    colors = {"red": 0, "green": 0, "blue": 0}
    for shape in shapes:
        for color in colors:
            possible_colors = color_dictionary[color][shape]
            colored_shapes = extract_colour(image, is_color, possible_colors)
            contours = detect_shapes(colored_shapes)
            num_shapes = count_shapes(contours)
            shapes[shape] += num_shapes
            colors[color] += num_shapes

    template = cv2.imread("./images/lleidahack_logo.png")
    logos_img = extract_colour(image, is_orange)
    num_lleidahack_logos = count_logos(template, logos_img)
    show_results(colors, shapes, num_lleidahack_logos)

if __name__ == "__main__":
    main()
