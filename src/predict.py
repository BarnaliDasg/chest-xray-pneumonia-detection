import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the saved model
model = load_model("pneumonia_detection_model.h5")

# Path to test images
test_dir = "chest_xray/test"

# Loop through NORMAL and PNEUMONIA folders
for folder in ["NORMAL", "PNEUMONIA"]:
    path = os.path.join(test_dir, folder)
    for img_file in os.listdir(path):
        img_path = os.path.join(path, img_file)

        # Load and preprocess image
        img = image.load_img(img_path, target_size=(150, 150))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0) / 255.0

        # Make prediction
        prediction = model.predict(x)
        label = "PNEUMONIA" if prediction[0][0] > 0.5 else "NORMAL"

        print(f"Image: {img_file}, Prediction: {label}, Probability: {prediction[0][0]:.2f}")
