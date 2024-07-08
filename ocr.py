
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

def getText(imagePath):
    input_image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    # Reduce noise using Gaussian blur
    blurred_image = cv2.GaussianBlur(input_image, (5, 5), 0)

    # Apply thresholding to create a binary image
    _, thresholded_image = cv2.threshold(blurred_image, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the detected contours
    for contour in contours:
        # Approximate the contour to reduce the number of vertices
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # Determine the shape based on the number of vertices
        num_vertices = len(approx)
        if num_vertices == 3:
            shape = "Triangle"
        elif num_vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                shape = "Square"
            else:
                shape = "Rectangle"
        elif num_vertices == 5:
            shape = "Pentagon"
        elif num_vertices == 6:
            shape = "Hexagon"
        else:
            shape = "Circle"

        # Draw the detected shape on the original image
        cv2.drawContours(input_image, [approx], -1, (0, 255, 0), 2)
        cv2.putText(input_image, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imwrite(imagePath, input_image)
    myconfig=('-l eng --oem 3 --psm 6')
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(imagePath)
    image = image.resize((1200, 1000))
    text = pytesseract.image_to_string(image, config=myconfig)
    print("Extracted Numbers:\n", text)
    lines = text.split('\n')
    lines_without_spaces = [line.replace(" ", "") for line in lines]
    combined_text = ','.join(lines_without_spaces)[:-1].replace("x", "X")
    print("OCR text: ", combined_text)
    return combined_text
