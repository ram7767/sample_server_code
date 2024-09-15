import cv2
import pytesseract

# Set up Tesseract path (change if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if needed

def extract_table(image_path):
    """
    This function takes the path to an image, processes it, and extracts table data using OCR.
    """
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale for easier processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding to detect the table structure
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours that represent table cells
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract data from the contours (potential table cells)
    table_data = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 50 and h > 20:  # Filter based on reasonable table cell size
            cell = image[y:y+h, x:x+w]
            cell_text = pytesseract.image_to_string(cell, config='--psm 6')
            table_data.append(cell_text.strip())

    return table_data
