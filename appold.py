from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def process_image(image_path):
    """Processes the image and returns metal identification results."""
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply blur and thresholding
    gray_blur = cv2.medianBlur(gray, 5)
    _, thresh = cv2.threshold(gray_blur, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Extract average color (for simplicity)
    avg_color = np.mean(image_rgb, axis=(0, 1)).astype(int)
    
    # Determine predominant metal (example logic)
    predominant_metal = "Unknown Metal"
    if avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:
        predominant_metal = "Copper"
    elif avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:
        predominant_metal = "Nickel"
    elif avg_color[2] > avg_color[0] and avg_color[2] > avg_color[1]:
        predominant_metal = "Aluminum"

    return predominant_metal, avg_color

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            
            # Process image
            metal, color = process_image(file_path)
            
            return render_template("index.html", metal=metal, color=color)
    
    return render_template("index.html", metal=None, color=None)

if __name__ == "__main__":
    app.run(debug=True)
