# Installs

# !pip install paddlepaddle
# !pip install paddleocr

# Imports

from PIL import Image
from paddleocr import PaddleOCR


def extract_text_and_coordinates(image_path):
    """
    Extracts word-level text and bounding boxes from an image using PaddleOCR.

    :param image_path: Path to the image
    :return: List of tuples (word, (x_min, y_min, x_max, y_max)), image width, image height
    """
    image = Image.open(image_path)
    width, height = image.size

    # Initialize PaddleOCR model
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize PaddleOCR, use appropriate language setting

    # Use PaddleOCR to extract word-level text and bounding boxes
    result = ocr.ocr(image_path, cls=True)  # cls=True enables text direction classification

    text_data = []
    for line in result:
        for word_info in line:
            word = word_info[1][0]  # Extract the text
            x_min, y_min = word_info[0][0]  # Top-left corner
            x_max, y_max = word_info[0][2]  # Bottom-right corner

            # Do not flip y_min and y_max; they already follow the top-left origin system
            text_data.append((word, (int(x_min), int(y_min), int(x_max), int(y_max))))

    return text_data, width, height

def scale_coordinates(x, y, original_width, original_height, target_width, target_height):
    """
    Scales the coordinates from the image's size to the target text file size.

    :param x: Original x coordinate
    :param y: Original y coordinate
    :param original_width: Width of the image
    :param original_height: Height of the image
    :param target_width: Width of the text grid (e.g., 80 or 120 characters)
    :param target_height: Height of the text grid
    :return: Scaled x, y coordinates
    """
    scaled_x = int(x * target_width / original_width)
    scaled_y = int(y * target_height / original_height)
    return scaled_x, scaled_y

def map_text_to_file(text_data, output_file, image_width, image_height, target_width=120, target_height=60):
    """
    Maps extracted text and coordinates to a text file with reduced spacing.

    :param text_data: List of tuples (text, (x_min, y_min, x_max, y_max))
    :param output_file: Path to the output text file
    :param image_width: Width of the original image
    :param image_height: Height of the original image
    :param target_width: Width of the text grid (default is 120)
    :param target_height: Height of the text grid (default is 60)
    """
    # Initialize an empty grid with spaces
    grid = [[" " for _ in range(target_width)] for _ in range(target_height)]

    for text, (x_min, y_min, x_max, y_max) in text_data:
        # Scale the coordinates to fit within the text grid
        scaled_x_min, scaled_y_min = scale_coordinates(x_min, y_max, image_width, image_height, target_width, target_height)

        # Map the text into the grid
        for i, char in enumerate(text):
            if scaled_x_min + i < target_width and scaled_y_min < target_height:
                grid[scaled_y_min][scaled_x_min + i] = char

    # Write the grid to the output file
    with open(output_file, 'w') as file:
        for row in grid:
            file.write("".join(row).rstrip() + "\n")
            
def extract_text(image_path,output_file):
    text_data, width, height = extract_text_and_coordinates(image_path)
    map_text_to_file(text_data, output_file, width, height)
    
image_path ='image_path'
output_file = 'outputfile.txt'
extract_text(image_path,output_file)