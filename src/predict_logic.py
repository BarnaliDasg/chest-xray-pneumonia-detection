import sys
import os
import numpy as np

# This hides the messy "Loaded TensorFlow" messages so PHP only sees the result
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
except ImportError:
    print("Error: TensorFlow not installed in this Python environment.")
    sys.exit(1)

# --- CONFIGURATION ---
# Using absolute paths is safer when running from XAMPP
MODEL_PATH = r"C:\xampp\htdocs\pneumonia_detection\model\pneumonia_detection_model.h5"

def predict(img_path):
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return

    # Load and Preprocess
    model = load_model(MODEL_PATH)
    img = image.load_img(img_path, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0

    # Predict
    prediction = model.predict(x, verbose=0)
    prob = prediction[0][0]
    label = "PNEUMONIA" if prob > 0.5 else "NORMAL"
    
    # This is the ONLY line PHP will look for
    print(f"{label}|{prob:.2f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        predict(sys.argv[1])
    else:
        print("Error: No image path provided to Python script.")