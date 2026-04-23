import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the model
model = load_model("../model/pneumonia_detection_model.h5")

# Function to make prediction
def predict_image(img_path):
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    x = cv2.resize(img_rgb, (150, 150))
    x = np.expand_dims(x, axis=0) / 255.0
    prediction = model.predict(x)[0][0]
    label = "PNEUMONIA" if prediction > 0.5 else "NORMAL"
    return img_rgb, label, prediction

# Function to upload image and show result
def upload_image():
    # Open file dialog for image selection
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    
    # Check if user canceled
    if not file_path:
        tk.messagebox.showwarning("No file selected", "Please select an image to proceed.")
        return

    # Check for valid image extension
    valid_extensions = (".jpg", ".jpeg", ".png")
    if not file_path.lower().endswith(valid_extensions):
        tk.messagebox.showerror("Invalid file", "Please select a valid image file (jpg, jpeg, png).")
        return

    # Try to load and process the image
    try:
        img, label, prob = predict_image(file_path)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Cannot process this image.\nDetails: {e}")
        return

    # Resize image for display
    max_width = 400
    scale = max_width / img.shape[1]
    new_height = int(img.shape[0] * scale)
    img_resized = cv2.resize(img, (max_width, new_height))

    # Convert to ImageTk format
    img_pil = Image.fromarray(img_resized)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Update image panel
    panel.config(image=img_tk)
    panel.image = img_tk

    # Update prediction label
    result_label.config(
        text=f"Prediction: {label} ({prob*100:.1f}%)",
        fg="green" if label == "NORMAL" else "red"
    )

# Create main window
root = tk.Tk()
root.title("Pneumonia Detector")
root.geometry("500x600")
root.config(bg="black")

# Header
header = tk.Label(root, text="Pneumonia Detector", font=("Arial", 20, "bold"), bg="#8b4513", fg="white")
header.pack(pady=10)

# Image panel
panel = tk.Label(root, bg="white", bd=2, relief="sunken")
panel.pack(padx=10, pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 16), bg="#f0f0f0")
result_label.pack(pady=10)

# Upload button
btn = tk.Button(root, text="Upload Image", command=upload_image, font=("Arial", 14), bg="#bc8f8f", fg="white")
btn.pack(pady=10)

root.mainloop()
