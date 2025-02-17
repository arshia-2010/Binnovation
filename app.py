from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

def classify_material(avg_color):
    avg_color_hsv = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_RGB2HSV)[0][0]
    h, s, v = avg_color_hsv
    
    if (h >= 20 and h <= 35) or (h >= 170 and h <= 180) or (h >= 35 and h <= 85):
        return "Plastic"
    elif ((h >= 0 and h <= 180) and (s < 30 and v > 200)) or (90 <= avg_color_hsv[0] <= 130):
        return "Glass"
    elif (h >= 0 and h <= 180) and (s < 50 and v > 100 and v < 200):
        return "Metal"
    elif (h >= 10 and h <= 30) and (s > 50 and v < 150):
        return "Organic Material"
    else:
        return "Unknown"

def detect_objects(image_path, output_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray_blur, 150, 255, cv2.THRESH_BINARY_INV)
    
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 500
    height, width = image.shape[:2]
    border_margin = 20
    
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        
        x, y, w, h = cv2.boundingRect(contour)
        if x < border_margin or y < border_margin or x + w > width - border_margin or y + h > height - border_margin:
            continue
        
        roi = image_rgb[y:y+h, x:x+w]
        avg_color = np.mean(roi, axis=(0, 1))
        material_type = classify_material(avg_color)
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, material_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    cv2.imwrite(output_path, image)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            processed_path = os.path.join(app.config["PROCESSED_FOLDER"], file.filename)
            file.save(file_path)
            detect_objects(file_path, processed_path)
            return render_template("index.html", processed_image=file.filename)
    return render_template("index.html", processed_image=None)

@app.route("/processed/<filename>")
def processed_image(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)


'''
from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

def classify_material(avg_color):
    avg_color_hsv = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_RGB2HSV)[0][0]
    h, s, v = avg_color_hsv
    
    if (20 <= h <= 35) or (170 <= h <= 180) or (35 <= h <= 85 and s > 50):  # Yellow, Red, Green, Pink, Orange
        return "Plastic"
    elif (0 <= h <= 180 and s < 25 and v > 190) or (90 <= h <= 130 and s > 40 and v > 100):  # White/Silver & Blue (common in glass)
        return "Glass"
    elif (h < 180 and s < 50 and 120 < v < 200):  # Metal (excluding very light/silver tones)
        return "Metal"
    elif (10 <= h <= 30 and s > 40 and v < 160):  # Brown shades for organic
        return "Organic Material"
    else:
        return "Unknown"

def detect_objects(image_path, output_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Adaptive threshold
    
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 700  # Increased to remove small specks
    height, width = image.shape[:2]
    border_margin = 25  # Avoid detecting objects near edges
    
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        
        x, y, w, h = cv2.boundingRect(contour)
        if x < border_margin or y < border_margin or x + w > width - border_margin or y + h > height - border_margin:
            continue
        
        roi = image_rgb[y:y+h, x:x+w]
        avg_color = np.mean(roi, axis=(0, 1))
        material_type = classify_material(avg_color)
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, material_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imwrite(output_path, image)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            processed_path = os.path.join(app.config["PROCESSED_FOLDER"], file.filename)
            file.save(file_path)
            detect_objects(file_path, processed_path)
            return render_template("index.html", processed_image=file.filename)
    return render_template("index.html", processed_image=None)

@app.route("/processed/<filename>")
def processed_image(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
'''
    