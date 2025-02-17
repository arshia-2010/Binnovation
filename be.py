import cv2
import numpy as np

def classify_material(avg_color):
    # Convert average color to HSV for better classification
    avg_color_hsv = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_RGB2HSV)[0][0]
    h, s, v = avg_color_hsv
    
    if (h >= 20 and h <= 35) or (h >= 170 and h <= 180) or (h >= 35 and h <= 85):  # Yellow, Red, Green, Pink, Purple, Orange
        return "Plastic"
    elif ((h >= 0 and h <= 180) and (s < 30 and v > 200)) or (90 <= avg_color_hsv[0] <= 130):  # Hue range for blue):  # White, Light Gray, Silver
        return "Glass"
    elif (h >= 0 and h <= 180) and (s < 50 and v > 100 and v < 200):  # Silver, Dark Gray
        return "Metal"
    elif (h >= 10 and h <= 30) and (s > 50 and v < 150):  # Brown shades
        return "Organic Material"
    else:
        return "Unknown"

def detect_objects(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur and thresholding for better object detection
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray_blur, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Morphological operations to remove small noise
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 500  # Adjust based on image size to remove small noise
    height, width = image.shape[:2]
    border_margin = 20  # Avoid detecting objects near the edges
    
    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) < min_area:
            continue
        
        x, y, w, h = cv2.boundingRect(contour)
        
        # Skip objects too close to the border
        if x < border_margin or y < border_margin or x + w > width - border_margin or y + h > height - border_margin:
            continue
        
        roi = image_rgb[y:y+h, x:x+w]
        avg_color = np.mean(roi, axis=(0, 1))  # Calculate average color in RGB
        material_type = classify_material(avg_color)
        
        # Draw bounding box and label
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, material_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        print(f"Object {i + 1}: Material = {material_type}, Avg RGB = {avg_color.astype(int)}")
    
    # Show the output image
    cv2.imshow("Detected Materials", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path=r"C:\Users\ahana\OneDrive\Desktop\Hackathons\YANTRA\sample3.jpg"
image = cv2.imread(image_path)
detect_objects(image_path)